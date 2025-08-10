"""
Automated video creation script using Python libraries.
Creates a slideshow-style video from demo output.
"""

import subprocess
import sys
import os
import time
from pathlib import Path

def install_dependencies():
    """Install required video processing libraries."""
    try:
        import cv2
        import PIL
        print("✅ Video dependencies already installed")
    except ImportError:
        print("📦 Installing video processing dependencies...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "opencv-python", "pillow", "matplotlib"])
        print("✅ Dependencies installed successfully")

def create_title_slide():
    """Create title slide for the video."""
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    from matplotlib import font_manager
    
    fig, ax = plt.subplots(figsize=(16, 9), facecolor='#0f1419')
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    ax.axis('off')
    
    # Background gradient effect
    gradient = patches.Rectangle((0, 0), 16, 9, 
                               facecolor='#0f1419', alpha=0.9)
    ax.add_patch(gradient)
    
    # Title
    ax.text(8, 6.5, 'Medical Coding AI Assistant', 
            fontsize=48, weight='bold', ha='center', 
            color='#ffffff', family='monospace')
    
    # Subtitle
    ax.text(8, 5.5, 'AI-Powered Clinical NER + ICD Code Recommendations', 
            fontsize=24, ha='center', color='#64ffda', 
            family='monospace')
    
    # Features
    features = [
        '🏥 Extract Medical Entities with Biomedical NER',
        '🎯 Recommend Top 5 ICD Codes with Confidence Scores', 
        '⚡ Real-time Processing Under 1 Second',
        '📊 Multi-Algorithm Scoring & Batch Processing'
    ]
    
    y_pos = 4.2
    for feature in features:
        ax.text(8, y_pos, feature, fontsize=18, ha='center', 
                color='#ffffff', family='monospace')
        y_pos -= 0.6
    
    # Footer
    ax.text(8, 1, 'github.com/yourusername/medical-coding-ai', 
            fontsize=16, ha='center', color='#64ffda', 
            style='italic', family='monospace')
    
    plt.tight_layout()
    plt.savefig('demo/title_slide.png', dpi=150, bbox_inches='tight', 
                facecolor='#0f1419', edgecolor='none')
    plt.close()
    print("✅ Title slide created")

def create_demo_frames():
    """Create frames showing demo output."""
    import matplotlib.pyplot as plt
    
    # Demo output content
    demo_sections = [
        {
            "title": "Clinical NER - Medical Entity Extraction",
            "content": [
                "📝 MEDICAL TEXT:",
                "68-year-old female with acute chest pain, diabetes mellitus type 2,",
                "hypertension, taking metformin and lisinopril.",
                "",
                "✅ EXTRACTED 29 MEDICAL ENTITIES:",
                "🏷️  Age: 68-year-old",
                "🏷️  Sign_symptom: acute chest pain", 
                "🏷️  History: diabetes mellitus type 2, hypertension",
                "🏷️  Medication: metformin, lisinopril"
            ]
        },
        {
            "title": "ICD Code Recommendations - Top 5 Results",
            "content": [
                "📝 Diagnosis: Acute myocardial infarction with ST elevation",
                "",
                "🏆 TOP 3 ICD RECOMMENDATIONS:",
                "",
                "⭐⭐⭐ 1. I21.9 | 🟢 HIGH CONFIDENCE",
                "     📄 Acute myocardial infarction, unspecified",
                "     🏥 Cardiovascular | Score: 0.371",
                "",
                "⭐⭐ 2. I25.10 | 🟡 MEDIUM CONFIDENCE", 
                "     📄 Atherosclerotic heart disease...",
                "     🏥 Cardiovascular | Score: 0.185"
            ]
        },
        {
            "title": "Performance Metrics & Capabilities",
            "content": [
                "📊 SYSTEM PERFORMANCE:",
                "",
                "🎯 ICD Codes Supported: 20+ across major categories",
                "⚡ Processing Speed: < 1 second per case",
                "🧠 AI Models: Biomedical NER + Multi-algorithm scoring",
                "📦 Batch Processing: Unlimited cases",
                "",
                "⚡ LIVE PERFORMANCE TEST:",
                "   🔥 Processed in 401ms",
                "   🎯 Generated 3 recommendations", 
                "   🏆 Top match: I21.9 (0.371 confidence)"
            ]
        }
    ]
    
    for i, section in enumerate(demo_sections):
        fig, ax = plt.subplots(figsize=(16, 9), facecolor='#0f1419')
        ax.set_xlim(0, 16)
        ax.set_ylim(0, 9)
        ax.axis('off')
        
        # Title
        ax.text(8, 8.2, section["title"], fontsize=36, weight='bold', 
                ha='center', color='#64ffda', family='monospace')
        
        # Content
        y_pos = 7.2
        for line in section["content"]:
            if line.strip():
                # Color coding based on content
                if line.startswith('📝') or line.startswith('🏆'):
                    color = '#64ffda'
                    weight = 'bold'
                elif line.startswith('⭐') or line.startswith('🎯'):
                    color = '#ffffff'
                    weight = 'bold'
                elif line.startswith('     '):
                    color = '#b0bec5'
                    weight = 'normal'
                else:
                    color = '#ffffff' 
                    weight = 'normal'
                
                ax.text(0.5, y_pos, line, fontsize=16, ha='left',
                       color=color, weight=weight, family='monospace')
            y_pos -= 0.35
        
        plt.tight_layout()
        plt.savefig(f'demo/frame_{i+1}.png', dpi=150, bbox_inches='tight',
                   facecolor='#0f1419', edgecolor='none')
        plt.close()
    
    print(f"✅ Created {len(demo_sections)} demo frames")

def create_video_from_frames():
    """Create MP4 video from generated frames."""
    import cv2
    import numpy as np
    from PIL import Image
    
    # Video settings
    fps = 1  # 1 frame per second for slideshow effect
    width, height = 1920, 1080
    
    # Create video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter('demo/medical_coding_ai_demo.mp4', 
                                  fourcc, fps, (width, height))
    
    # Add title slide (5 seconds)
    title_img = cv2.imread('demo/title_slide.png')
    title_img = cv2.resize(title_img, (width, height))
    for _ in range(5):  # 5 seconds
        video_writer.write(title_img)
    
    # Add demo frames (3 seconds each)
    for i in range(1, 4):  # 3 demo frames
        frame_path = f'demo/frame_{i}.png'
        if os.path.exists(frame_path):
            frame_img = cv2.imread(frame_path)
            frame_img = cv2.resize(frame_img, (width, height))
            for _ in range(3):  # 3 seconds per frame
                video_writer.write(frame_img)
    
    # Add final title slide (3 seconds)
    for _ in range(3):
        video_writer.write(title_img)
    
    video_writer.release()
    cv2.destroyAllWindows()
    
    print("✅ Video created: demo/medical_coding_ai_demo.mp4")

def create_slideshow_video():
    """Main function to create slideshow video."""
    print("🎬 Creating Medical Coding AI Demo Video...")
    print("=" * 50)
    
    # Install dependencies
    install_dependencies()
    
    # Create demo directory if it doesn't exist
    os.makedirs('demo', exist_ok=True)
    
    # Create slides and video
    create_title_slide()
    create_demo_frames()  
    create_video_from_frames()
    
    print("\n🎉 Video creation complete!")
    print("📁 Output: demo/medical_coding_ai_demo.mp4")
    print("⏱️  Duration: ~14 seconds (slideshow format)")
    print("📺 Resolution: 1920x1080")
    
    # Clean up temporary files
    for file in ['demo/title_slide.png'] + [f'demo/frame_{i}.png' for i in range(1, 4)]:
        if os.path.exists(file):
            os.remove(file)
    
    print("🧹 Temporary files cleaned up")

if __name__ == "__main__":
    create_slideshow_video()