import streamlit as st
import sqlite3
from datetime import datetime
import pandas as pd
import uuid

# Page configuration
st.set_page_config(page_title="Surgical Procedure Review", layout="wide")

# Custom CSS for better styling and session cleanup
st.markdown("""
    <style>
    .main-header {
        font-size: 24px;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 10px;
    }
    .query-box {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 30px;
    }
    .choice-box {
        background-color: #ffffff;
        border: 2px solid #e0e0e0;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 15px;
    }
    .choice-header {
        font-size: 18px;
        font-weight: bold;
        color: #2c3e50;
    }
    div.stButton > button[kind="secondary"] {
        background-color: #28a745;
        color: white;
    }
    div.stButton > button[kind="secondary"]:hover {
        background-color: #218838;
        color: white;
    }
    </style>
    <script>
    // Cleanup session on page unload
    window.addEventListener('beforeunload', function(e) {
        // Send beacon to mark session as ended
        const sessionId = window.parent.document.querySelector('[data-testid="stSessionState"]')?.textContent;
        if (sessionId) {
            navigator.sendBeacon('/cleanup_session', JSON.stringify({session_id: sessionId}));
        }
    });
    </script>
""", unsafe_allow_html=True)

# Database functions
def init_database():
    """Initialize the SQLite database and create tables if not exists"""
    conn = sqlite3.connect('surgical_reviews.db')
    c = conn.cursor()
    
    # Query procedures table
    c.execute('''
        CREATE TABLE IF NOT EXISTS query_procedures (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query_procedure TEXT NOT NULL,
            status TEXT DEFAULT 'free',
            reviewer_session_id TEXT,
            session_timestamp TIMESTAMP
        )
    ''')
    
    # Matching choices table
    c.execute('''
        CREATE TABLE IF NOT EXISTS matching_choices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query_procedure_id INTEGER,
            choice_number INTEGER,
            procedure_name TEXT NOT NULL,
            reasoning TEXT,
            description TEXT,
            FOREIGN KEY (query_procedure_id) REFERENCES query_procedures(id)
        )
    ''')
    
    # Reviews table
    c.execute('''
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query_procedure_id INTEGER,
            query_procedure TEXT NOT NULL,
            selected_choice INTEGER,
            selected_procedure_name TEXT,
            decision TEXT NOT NULL,
            reviewer_comments TEXT,
            reviewer_session_id TEXT,
            review_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (query_procedure_id) REFERENCES query_procedures(id)
        )
    ''')
    
    conn.commit()
    conn.close()

def seed_sample_data():
    """Add sample data if tables are empty"""
    conn = sqlite3.connect('surgical_reviews.db')
    c = conn.cursor()
    
    # Check if data exists
    c.execute('SELECT COUNT(*) FROM query_procedures')
    if c.fetchone()[0] == 0:
        # Insert sample query procedures
        sample_queries = [
            "Laparoscopic Cholecystectomy",
            "Total Knee Replacement",
            "Coronary Artery Bypass Graft"
        ]
        
        for query in sample_queries:
            c.execute('INSERT INTO query_procedures (query_procedure, status) VALUES (?, ?)', (query, 'free'))
        
        # Insert matching choices for first query
        choices = [
            (1, 1, "Laparoscopic Cholecystectomy", 
             "Exact match - Same procedure name with identical surgical approach (laparoscopic) and target organ (gallbladder removal).",
             "A minimally invasive surgical procedure to remove the gallbladder using small incisions and a camera. Performed under general anesthesia with 3-4 small ports."),
            (1, 2, "Cholecystectomy, Laparoscopic Approach",
             "Strong match - Describes the same procedure with reversed terminology. Both refer to laparoscopic gallbladder removal.",
             "Surgical removal of the gallbladder performed laparoscopically. Standard treatment for symptomatic gallstones and cholecystitis."),
            (1, 3, "Open Cholecystectomy",
             "Partial match - Same target procedure (gallbladder removal) but different surgical approach (open vs laparoscopic).",
             "Traditional open surgery to remove the gallbladder through a larger abdominal incision. Used when laparoscopic approach is not feasible."),
            (1, 4, "Laparoscopic Appendectomy",
             "Weak match - Same surgical approach (laparoscopic) but different target organ (appendix vs gallbladder).",
             "Minimally invasive removal of the appendix using laparoscopic technique. Typically performed for acute appendicitis."),
            (1, 5, "Endoscopic Retrograde Cholangiopancreatography (ERCP)",
             "Low match - Related to biliary system but different procedure type. ERCP is diagnostic/therapeutic endoscopy, not surgical removal.",
             "Endoscopic procedure to examine and treat conditions of the bile ducts and pancreatic duct. Can remove stones but doesn't remove the gallbladder.")
        ]
        
        for choice in choices:
            c.execute('''INSERT INTO matching_choices 
                        (query_procedure_id, choice_number, procedure_name, reasoning, description) 
                        VALUES (?, ?, ?, ?, ?)''', choice)
        
        conn.commit()
    
    conn.close()

def get_next_free_query(session_id):
    """Get next available query and mark as pending for this session"""
    conn = sqlite3.connect('surgical_reviews.db')
    c = conn.cursor()
    
    # Free up stale sessions (older than 5 minutes of inactivity)
    c.execute('''UPDATE query_procedures 
                 SET status = 'free', reviewer_session_id = NULL 
                 WHERE status = 'pending' 
                 AND datetime(session_timestamp) < datetime('now', '-5 minutes')''')
    
    # Get next free query
    c.execute('''SELECT id, query_procedure FROM query_procedures 
                 WHERE status = 'free' LIMIT 1''')
    result = c.fetchone()
    
    if result:
        query_id, query_proc = result
        # Mark as pending for this session
        c.execute('''UPDATE query_procedures 
                     SET status = 'pending', reviewer_session_id = ?, session_timestamp = CURRENT_TIMESTAMP
                     WHERE id = ?''', (session_id, query_id))
        conn.commit()
        conn.close()
        return query_id, query_proc
    
    conn.close()
    return None, None

def get_matching_choices(query_id):
    """Get matching choices for a query"""
    conn = sqlite3.connect('surgical_reviews.db')
    c = conn.cursor()
    c.execute('''SELECT choice_number, procedure_name, reasoning, description 
                 FROM matching_choices WHERE query_procedure_id = ? 
                 ORDER BY choice_number''', (query_id,))
    choices = c.fetchall()
    conn.close()
    return choices

def save_review(query_id, query_proc, choice_num, choice_name, decision, comments, session_id):
    """Save review to database and mark query as completed"""
    conn = sqlite3.connect('surgical_reviews.db')
    c = conn.cursor()
    
    # Save review
    c.execute('''INSERT INTO reviews 
                 (query_procedure_id, query_procedure, selected_choice, selected_procedure_name, 
                  decision, reviewer_comments, reviewer_session_id)
                 VALUES (?, ?, ?, ?, ?, ?, ?)''',
              (query_id, query_proc, choice_num, choice_name, decision, comments, session_id))
    
    # Mark query as completed
    c.execute('''UPDATE query_procedures 
                 SET status = 'completed', reviewer_session_id = NULL 
                 WHERE id = ?''', (query_id,))
    
    conn.commit()
    conn.close()

def free_current_query(query_id):
    """Free up current query (for skip action)"""
    conn = sqlite3.connect('surgical_reviews.db')
    c = conn.cursor()
    c.execute('''UPDATE query_procedures 
                 SET status = 'free', reviewer_session_id = NULL 
                 WHERE id = ?''', (query_id,))
    conn.commit()
    conn.close()

def cleanup_session(session_id):
    """Free up any queries held by this session"""
    conn = sqlite3.connect('surgical_reviews.db')
    c = conn.cursor()
    c.execute('''UPDATE query_procedures 
                 SET status = 'free', reviewer_session_id = NULL 
                 WHERE reviewer_session_id = ? AND status = 'pending' ''', (session_id,))
    conn.commit()
    conn.close()

def update_session_heartbeat(session_id):
    """Update session timestamp to keep it alive"""
    conn = sqlite3.connect('surgical_reviews.db')
    c = conn.cursor()
    c.execute('''UPDATE query_procedures 
                 SET session_timestamp = CURRENT_TIMESTAMP
                 WHERE reviewer_session_id = ? AND status = 'pending' ''', (session_id,))
    conn.commit()
    conn.close()

# Initialize database
init_database()
seed_sample_data()

# Initialize session state
if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if 'current_query_id' not in st.session_state:
    st.session_state.current_query_id = None
if 'current_query_proc' not in st.session_state:
    st.session_state.current_query_proc = None
if 'matching_choices' not in st.session_state:
    st.session_state.matching_choices = []
if 'selected_choice' not in st.session_state:
    st.session_state.selected_choice = None
if 'last_heartbeat' not in st.session_state:
    st.session_state.last_heartbeat = datetime.now()

# Update heartbeat every 30 seconds to keep session alive
current_time = datetime.now()
if (current_time - st.session_state.last_heartbeat).seconds > 30:
    if st.session_state.current_query_id:
        update_session_heartbeat(st.session_state.session_id)
    st.session_state.last_heartbeat = current_time

# Register cleanup on session end
import atexit
atexit.register(cleanup_session, st.session_state.session_id)

# Load query if not loaded
if st.session_state.current_query_id is None:
    query_id, query_proc = get_next_free_query(st.session_state.session_id)
    if query_id:
        st.session_state.current_query_id = query_id
        st.session_state.current_query_proc = query_proc
        st.session_state.matching_choices = get_matching_choices(query_id)
    else:
        st.warning("No queries available for review at this time.")
        st.stop()

# App title
st.title("🏥 Surgical Procedure Matching Review")

# Display session info
st.caption(f"Session ID: {st.session_state.session_id[:8]}...")

# Query procedure display
st.markdown('<div class="main-header">Query Procedure:</div>', unsafe_allow_html=True)
st.markdown(f'<div class="query-box"><h2>{st.session_state.current_query_proc}</h2></div>', unsafe_allow_html=True)

# Display matching choices
st.markdown('<div class="main-header">Matching Choices:</div>', unsafe_allow_html=True)

for choice in st.session_state.matching_choices:
    choice_num, proc_name, reasoning, description = choice
    
    with st.container():
        st.markdown(f'<div class="choice-box">', unsafe_allow_html=True)
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f'<div class="choice-header">Choice {choice_num}: {proc_name}</div>', unsafe_allow_html=True)
        
        with col2:
            is_selected = st.session_state.selected_choice == choice_num
            button_type = "secondary" if is_selected else "primary"
            button_label = "✓ Selected" if is_selected else "Select"
            
            if st.button(button_label, key=f"select_{choice_num}", type=button_type):
                st.session_state.selected_choice = choice_num
                st.rerun()
        
        # Expandable sections for reasoning and description
        with st.expander("📋 Reasoning"):
            st.write(reasoning)
        
        with st.expander("📝 Description"):
            st.write(description)
        
        st.markdown('</div>', unsafe_allow_html=True)

# Display selected choice
if st.session_state.selected_choice:
    selected = [c for c in st.session_state.matching_choices if c[0] == st.session_state.selected_choice][0]
    st.info(f"✓ Currently selected: Choice {selected[0]} - {selected[1]}")

# Review section
st.markdown("---")
st.markdown('<div class="main-header">Review Decision:</div>', unsafe_allow_html=True)

# Review comments
review_comment = st.text_area(
    "Reviewer Comments:",
    height=100,
    placeholder="Enter any additional notes or feedback about this matching review...",
    key="review_comment_input"
)

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("✅ Submit", type="primary", use_container_width=True):
        if st.session_state.selected_choice:
            selected = [c for c in st.session_state.matching_choices if c[0] == st.session_state.selected_choice][0]
            save_review(
                st.session_state.current_query_id,
                st.session_state.current_query_proc,
                st.session_state.selected_choice,
                selected[1],
                "SUBMIT",
                review_comment,
                st.session_state.session_id
            )
            st.success("✓ Review submitted successfully!")
            # Reset for next query
            st.session_state.current_query_id = None
            st.session_state.current_query_proc = None
            st.session_state.matching_choices = []
            st.session_state.selected_choice = None
            st.rerun()
        else:
            st.warning("Please select a choice first")

with col2:
    if st.button("⏭️ Skip", use_container_width=True):
        free_current_query(st.session_state.current_query_id)
        st.info("Query skipped and returned to queue")
        # Reset for next query
        st.session_state.current_query_id = None
        st.session_state.current_query_proc = None
        st.session_state.matching_choices = []
        st.session_state.selected_choice = None
        st.rerun()

with col3:
    if st.button("🚫 None of These", use_container_width=True):
        save_review(
            st.session_state.current_query_id,
            st.session_state.current_query_proc,
            None,
            None,
            "NONE",
            review_comment,
            st.session_state.session_id
        )
        st.info("No suitable match recorded!")
        # Reset for next query
        st.session_state.current_query_id = None
        st.session_state.current_query_proc = None
        st.session_state.matching_choices = []
        st.session_state.selected_choice = None
        st.rerun()
