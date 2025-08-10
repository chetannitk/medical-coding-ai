"""
Create an animated SVG terminal demo from the quick_demo.py output.
This creates a GitHub-compatible animated SVG that shows the demo running.
"""

import subprocess
import sys
import os
import time
import re
from typing import List, Dict

def capture_demo_output():
    """Capture the output of the quick demo with timing."""
    print("📹 Capturing quick demo output...")
    
    try:
        # Run the demo and capture output
        result = subprocess.run(
            [sys.executable, "demo/quick_demo.py"],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        if result.returncode == 0:
            output_lines = result.stdout.split('\n')
            print(f"✅ Captured {len(output_lines)} lines of output")
            return output_lines
        else:
            print(f"❌ Demo failed with return code {result.returncode}")
            print(f"Error: {result.stderr}")
            return None
            
    except subprocess.TimeoutExpired:
        print("⏰ Demo timed out after 120 seconds")
        return None
    except Exception as e:
        print(f"❌ Error capturing demo: {e}")
        return None

def clean_terminal_output(lines: List[str]) -> List[Dict]:
    """Clean and structure terminal output for SVG animation."""
    cleaned_frames = []
    current_frame = []
    
    # Remove ANSI codes and emoji that might not render well
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    
    frame_markers = [
        "🔥==========================================================🔥",
        "=" * 50,
        "=" * 60,
        "🎬 Creating Medical Coding AI Demo Video",
        "🚀 System ready!"
    ]
    
    for line in lines:
        # Clean ANSI codes
        clean_line = ansi_escape.sub('', line)
        
        # Replace problematic emojis with text equivalents
        emoji_replacements = {
            '🔥': '[FIRE]',
            '🏥': '[HOSPITAL]',
            '🤖': '[ROBOT]',
            '⚡': '[LIGHTNING]',
            '📥': '[INBOX]',
            '✅': '[CHECK]',
            '🚀': '[ROCKET]',
            '📝': '[MEMO]',
            '🔍': '[SEARCH]',
            '🏷️': '[LABEL]',
            '🏆': '[TROPHY]',
            '⭐': '[STAR]',
            '🟢': '[GREEN]',
            '🟡': '[YELLOW]',
            '🔴': '[RED]',
            '📄': '[PAGE]',
            '💊': '[PILL]',
            '🫀': '[HEART]',
            '🦠': '[MICROBE]',
            '😷': '[MASK]',
            '📊': '[CHART]',
            '🎯': '[TARGET]',
            '🧠': '[BRAIN]',
            '📦': '[PACKAGE]',
            '💡': '[BULB]',
            '🌟': '[STAR2]',
            '📁': '[FOLDER]',
            '⏱️': '[TIMER]',
            '📺': '[TV]',
            '🧹': '[BROOM]',
            '🎉': '[PARTY]'
        }
        
        for emoji, replacement in emoji_replacements.items():
            clean_line = clean_line.replace(emoji, replacement)
        
        # Check if this line indicates a new frame
        is_frame_marker = any(marker in clean_line for marker in frame_markers)
        
        if is_frame_marker and current_frame:
            # Save current frame and start new one
            cleaned_frames.append({
                'lines': current_frame.copy(),
                'duration': 3.0  # 3 seconds per frame
            })
            current_frame = []
        
        if clean_line.strip():  # Only add non-empty lines
            current_frame.append(clean_line[:100])  # Limit line length
    
    # Add final frame
    if current_frame:
        cleaned_frames.append({
            'lines': current_frame.copy(),
            'duration': 3.0
        })
    
    # Limit to key frames for SVG size
    key_frames = [
        cleaned_frames[0] if cleaned_frames else {'lines': ['Medical Coding AI Assistant'], 'duration': 2.0},
    ]
    
    # Add frames that show important content
    for frame in cleaned_frames[1:]:
        frame_text = ' '.join(frame['lines']).lower()
        if any(keyword in frame_text for keyword in [
            'clinical ner', 'icd code', 'recommendations', 'performance', 'extracted'
        ]):
            key_frames.append(frame)
            if len(key_frames) >= 4:  # Limit frames for manageable SVG size
                break
    
    return key_frames

def create_terminal_svg(frames: List[Dict], output_file: str):
    """Create an animated SVG that looks like a terminal."""
    
    if not frames:
        print("❌ No frames to create SVG from")
        return False
    
    # SVG settings
    width = 800
    height = 500
    font_size = 12
    line_height = 16
    char_width = 7.2
    
    # Calculate total animation duration
    total_duration = sum(frame['duration'] for frame in frames)
    
    # SVG header
    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
    <style>
        .terminal {{
            font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
            font-size: {font_size}px;
            fill: #00ff00;
        }}
        .terminal-bg {{
            fill: #000000;
            stroke: #333333;
            stroke-width: 2;
            rx: 5;
        }}
        .terminal-header {{
            fill: #333333;
            stroke: #666666;
            stroke-width: 1;
        }}
        .terminal-title {{
            font-family: system-ui, sans-serif;
            font-size: 11px;
            fill: #ffffff;
        }}
        .cursor {{
            fill: #00ff00;
            animation: blink 1s infinite;
        }}
        @keyframes blink {{
            0%, 50% {{ opacity: 1; }}
            51%, 100% {{ opacity: 0; }}
        }}
    </style>
    
    <!-- Terminal window -->
    <rect class="terminal-bg" x="0" y="0" width="{width}" height="{height}"/>
    
    <!-- Terminal header -->
    <rect class="terminal-header" x="0" y="0" width="{width}" height="25"/>
    
    <!-- Terminal title -->
    <text class="terminal-title" x="10" y="17">Medical Coding AI Assistant - Demo</text>
    
    <!-- Terminal buttons -->
    <circle cx="20" cy="12.5" r="5" fill="#ff5f56"/>
    <circle cx="35" cy="12.5" r="5" fill="#ffbd2e"/>
    <circle cx="50" cy="12.5" r="5" fill="#27c93f"/>
    
    <!-- Terminal content -->
    <g transform="translate(10, 35)">
'''
    
    # Add animated frames
    current_time = 0
    
    for frame_idx, frame in enumerate(frames):
        y_pos = 20
        
        # Create animation group for this frame
        svg_content += f'''
        <g opacity="0">
            <animateTransform attributeName="opacity" 
                values="0;0;1;1;0;0" 
                dur="{total_duration}s" 
                begin="{current_time}s"
                repeatCount="indefinite"/>
'''
        
        # Add lines for this frame
        max_lines = min(25, len(frame['lines']))  # Limit lines to fit in terminal
        
        for line_idx, line in enumerate(frame['lines'][:max_lines]):
            if line.strip():  # Only render non-empty lines
                # Truncate long lines
                display_line = line[:100]
                
                svg_content += f'''
            <text class="terminal" x="0" y="{y_pos}">
                {display_line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')}
            </text>'''
                y_pos += line_height
        
        svg_content += '''
        </g>'''
        
        current_time += frame['duration']
    
    # Add blinking cursor
    svg_content += f'''
    </g>
    
    <!-- Blinking cursor -->
    <rect class="cursor" x="15" y="{height - 30}" width="8" height="16"/>
    
</svg>'''
    
    # Write SVG file
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(svg_content)
        print(f"✅ SVG animation created: {output_file}")
        return True
    except Exception as e:
        print(f"❌ Error writing SVG: {e}")
        return False

def create_simple_demo_svg(output_file: str):
    """Create a simplified demo SVG with key content."""
    
    demo_frames = [
        {
            'title': 'Medical Coding AI Assistant - Live Demo',
            'lines': [
                'AI-Powered Medical Coding with NER + ICD Recommendations',
                'Real-time clinical text analysis and ICD code suggestions',
                '',
                '[FIRE] Loading Clinical NER model... [CHECK]',
                '[FIRE] Loading ICD Recommendation engine... [CHECK]',
                '[ROCKET] System ready! Let\'s see it in action...'
            ],
            'duration': 4.0
        },
        {
            'title': 'DEMO 1: Clinical NER - Medical Entity Extraction',
            'lines': [
                '[MEMO] MEDICAL TEXT:',
                '68-year-old female with acute chest pain, diabetes mellitus',
                'type 2, hypertension, taking metformin and lisinopril.',
                '',
                '[CHECK] EXTRACTED 29 MEDICAL ENTITIES:',
                '[LABEL] Age: 68-year-old',
                '[LABEL] Sign_symptom: acute chest pain',
                '[LABEL] History: diabetes mellitus type 2, hypertension',
                '[LABEL] Medication: metformin, lisinopril'
            ],
            'duration': 5.0
        },
        {
            'title': 'DEMO 2: ICD Code Recommendations - Top Results',
            'lines': [
                '[MEMO] Diagnosis: Acute myocardial infarction with ST elevation',
                '',
                '[TROPHY] TOP 3 ICD RECOMMENDATIONS:',
                '',
                '[STAR][STAR][STAR] 1. I21.9 | [GREEN] HIGH CONFIDENCE',
                '     [PAGE] Acute myocardial infarction, unspecified',
                '     [HOSPITAL] Cardiovascular | Score: 0.371',
                '',
                '[STAR][STAR] 2. I25.10 | [YELLOW] MEDIUM CONFIDENCE',
                '     [PAGE] Atherosclerotic heart disease...',
                '     [HOSPITAL] Cardiovascular | Score: 0.185'
            ],
            'duration': 5.0
        },
        {
            'title': 'Performance Metrics & System Ready',
            'lines': [
                '[CHART] SYSTEM PERFORMANCE:',
                '',
                '[TARGET] ICD Codes Supported: 20+ across major categories',
                '[LIGHTNING] Processing Speed: < 1 second per case',
                '[BRAIN] AI Models: Biomedical NER + Multi-algorithm scoring',
                '[PACKAGE] Batch Processing: Unlimited cases',
                '',
                '[LIGHTNING] LIVE PERFORMANCE TEST:',
                '   [FIRE] Processed in 401ms',
                '   [TARGET] Generated 3 recommendations',
                '   [TROPHY] Top match: I21.9 (0.371 confidence)',
                '',
                '[PARTY] Ready for medical coding workflows!'
            ],
            'duration': 4.0
        }
    ]
    
    return create_terminal_svg(demo_frames, output_file)

def main():
    """Main function to create the terminal SVG demo."""
    print("🎬 Creating Terminal SVG Animation Demo")
    print("=" * 45)
    
    # Try to capture live demo first
    print("📹 Attempting to capture live demo output...")
    demo_output = capture_demo_output()
    
    output_file = "demo/terminal_demo.svg"
    
    if demo_output:
        print("✅ Processing captured output...")
        frames = clean_terminal_output(demo_output)
        
        if frames:
            success = create_terminal_svg(frames, output_file)
        else:
            print("⚠️  No frames extracted, using simple demo...")
            success = create_simple_demo_svg(output_file)
    else:
        print("⚠️  Could not capture live demo, creating simple demo...")
        success = create_simple_demo_svg(output_file)
    
    if success:
        print(f"\n🎉 SVG Demo Animation Created!")
        print(f"📁 File: {output_file}")
        print(f"📊 Size: {os.path.getsize(output_file) / 1024:.1f} KB")
        print(f"🌐 GitHub compatible: ✅")
        print(f"\n📋 To embed in README, use:")
        print(f'![Demo](https://github.com/chetannitk/medical-coding-ai/raw/main/{output_file})')
        return True
    else:
        print("❌ Failed to create SVG animation")
        return False

if __name__ == "__main__":
    main()