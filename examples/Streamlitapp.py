import streamlit as st
import sqlite3
from datetime import datetime
import pandas as pd

# Page configuration
st.set_page_config(page_title="Surgical Procedure Review", layout="wide")

# Custom CSS for better styling
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
    </style>
""", unsafe_allow_html=True)

# Database functions
def init_database():
    """Initialize the SQLite database and create table if not exists"""
    conn = sqlite3.connect('surgical_reviews.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query_procedure TEXT NOT NULL,
            selected_choice INTEGER,
            selected_procedure_name TEXT,
            decision TEXT NOT NULL,
            reviewer_comments TEXT,
            review_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_review(query_proc, choice_num, choice_name, decision, comments):
    """Save review to database"""
    conn = sqlite3.connect('surgical_reviews.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO reviews (query_procedure, selected_choice, selected_procedure_name, decision, reviewer_comments)
        VALUES (?, ?, ?, ?, ?)
    ''', (query_proc, choice_num, choice_name, decision, comments))
    conn.commit()
    conn.close()

def get_recent_reviews(limit=10):
    """Retrieve recent reviews from database"""
    conn = sqlite3.connect('surgical_reviews.db')
    df = pd.read_sql_query(f'SELECT * FROM reviews ORDER BY review_timestamp DESC LIMIT {limit}', conn)
    conn.close()
    return df

# Initialize database
init_database()

# Initialize session state
if 'selected_choice' not in st.session_state:
    st.session_state.selected_choice = None
if 'review_submitted' not in st.session_state:
    st.session_state.review_submitted = False

# Sample data
query_procedure = "Laparoscopic Cholecystectomy"

matching_procedures = [
    {
        "name": "Laparoscopic Cholecystectomy",
        "reasoning": "Exact match - Same procedure name with identical surgical approach (laparoscopic) and target organ (gallbladder removal).",
        "description": "A minimally invasive surgical procedure to remove the gallbladder using small incisions and a camera. Performed under general anesthesia with 3-4 small ports."
    },
    {
        "name": "Cholecystectomy, Laparoscopic Approach",
        "reasoning": "Strong match - Describes the same procedure with reversed terminology. Both refer to laparoscopic gallbladder removal.",
        "description": "Surgical removal of the gallbladder performed laparoscopically. Standard treatment for symptomatic gallstones and cholecystitis."
    },
    {
        "name": "Open Cholecystectomy",
        "reasoning": "Partial match - Same target procedure (gallbladder removal) but different surgical approach (open vs laparoscopic). Different technique and recovery profile.",
        "description": "Traditional open surgery to remove the gallbladder through a larger abdominal incision. Used when laparoscopic approach is not feasible."
    },
    {
        "name": "Laparoscopic Appendectomy",
        "reasoning": "Weak match - Same surgical approach (laparoscopic) but different target organ (appendix vs gallbladder). Different indication and anatomical location.",
        "description": "Minimally invasive removal of the appendix using laparoscopic technique. Typically performed for acute appendicitis."
    },
    {
        "name": "Endoscopic Retrograde Cholangiopancreatography (ERCP)",
        "reasoning": "Low match - Related to biliary system but different procedure type. ERCP is diagnostic/therapeutic endoscopy, not surgical removal of gallbladder.",
        "description": "Endoscopic procedure to examine and treat conditions of the bile ducts and pancreatic duct. Can remove stones but doesn't remove the gallbladder."
    }
]

# App title
st.title("🏥 Surgical Procedure Matching Review")

# Sidebar for viewing past reviews
with st.sidebar:
    st.header("📊 Recent Reviews")
    if st.button("Refresh Reviews"):
        st.rerun()
    
    try:
        recent_reviews = get_recent_reviews(10)
        if not recent_reviews.empty:
            st.dataframe(recent_reviews[['query_procedure', 'decision', 'review_timestamp']], 
                        use_container_width=True, height=300)
        else:
            st.info("No reviews yet")
    except Exception as e:
        st.error(f"Error loading reviews: {e}")

# Query procedure display
st.markdown('<div class="main-header">Query Procedure:</div>', unsafe_allow_html=True)
st.markdown(f'<div class="query-box"><h2>{query_procedure}</h2></div>', unsafe_allow_html=True)

# Display matching choices
st.markdown('<div class="main-header">Matching Choices:</div>', unsafe_allow_html=True)

for idx, proc in enumerate(matching_procedures, 1):
    with st.container():
        st.markdown(f'<div class="choice-box">', unsafe_allow_html=True)
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f'<div class="choice-header">Choice {idx}: {proc["name"]}</div>', unsafe_allow_html=True)
        
        with col2:
            if st.button(f"Select", key=f"select_{idx}"):
                st.session_state.selected_choice = idx
        
        # Expandable sections for reasoning and description
        with st.expander("📋 Reasoning"):
            st.write(proc["reasoning"])
        
        with st.expander("📝 Description"):
            st.write(proc["description"])
        
        st.markdown('</div>', unsafe_allow_html=True)

# Display selected choice
if st.session_state.selected_choice:
    st.info(f"✓ Currently selected: Choice {st.session_state.selected_choice} - {matching_procedures[st.session_state.selected_choice - 1]['name']}")

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
    if st.button("✅ Accept", type="primary", use_container_width=True):
        if st.session_state.selected_choice:
            choice_idx = st.session_state.selected_choice - 1
            save_review(
                query_procedure,
                st.session_state.selected_choice,
                matching_procedures[choice_idx]['name'],
                "ACCEPT",
                review_comment
            )
            st.success(f"✓ Accepted Choice {st.session_state.selected_choice} and saved to database!")
            st.session_state.review_submitted = True
        else:
            st.warning("Please select a choice first")

with col2:
    if st.button("❌ Reject", type="secondary", use_container_width=True):
        if st.session_state.selected_choice:
            choice_idx = st.session_state.selected_choice - 1
            save_review(
                query_procedure,
                st.session_state.selected_choice,
                matching_procedures[choice_idx]['name'],
                "REJECT",
                review_comment
            )
            st.error(f"✗ Rejected Choice {st.session_state.selected_choice} and saved to database!")
            st.session_state.review_submitted = True
        else:
            st.warning("Please select a choice first")

with col3:
    if st.button("🚫 None of These", use_container_width=True):
        save_review(
            query_procedure,
            None,
            None,
            "NONE",
            review_comment
        )
        st.info("No suitable match selected and saved to database!")
        st.session_state.review_submitted = True

# Reset button
if st.session_state.review_submitted:
    if st.button("Start New Review"):
        st.session_state.selected_choice = None
        st.session_state.review_submitted = False
        st.rerun()
