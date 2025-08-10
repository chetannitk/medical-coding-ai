# Demo Video Resources

This directory contains all resources needed to create a professional demo video for the Medical Coding AI Assistant project.

## 📁 Files Overview

### 🎬 `demo_video_script.md`
- **Complete video script** with narration and timing
- **10 structured scenes** covering all major features
- **Recording tips** and technical setup guidance
- **Pre-demo checklist** for smooth recording

### 🖥️ `interactive_demo.py`
- **Full interactive demo** with pause points for recording
- **Guided walkthrough** of all major features
- **Visual loading animations** and progress indicators
- **Perfect for screen recording** with presenter control

### ⚡ `quick_demo.py`
- **Condensed 5-minute demo** with visual effects
- **High-impact demonstrations** of key capabilities
- **Automated flow** with emojis and formatting
- **Great for social media** or quick presentations

### 📊 `demo_data.json`
- **Structured test cases** for consistent demonstrations
- **Expected results** for validation
- **Performance benchmarks** and talking points
- **Video segment timing** and content breakdown

## 🎯 Recommended Demo Flow

### For Full Demo Video (8-10 minutes):
```bash
python demo/interactive_demo.py
```

### For Quick Demo (5 minutes):
```bash
python demo/quick_demo.py
```

### For Custom Recording:
Use the cases from `demo_data.json` with your own script.

## 🎥 Video Recording Setup

### Screen Setup:
1. **Terminal size**: 120x30 minimum
2. **Font size**: 14pt+ for visibility
3. **Color scheme**: High contrast (dark background)
4. **Resolution**: 1080p minimum

### Audio Setup:
1. **Clear narration** following script
2. **Background music**: Optional, low volume
3. **Sound effects**: System sounds for authenticity

### Recording Software:
- **macOS**: QuickTime Player, ScreenFlow
- **Windows**: OBS Studio, Camtasia  
- **Linux**: OBS Studio, SimpleScreenRecorder

## 🚀 Quick Start for Recording

1. **Prepare environment:**
   ```bash
   cd medical_coding
   pip install -r requirements.txt
   python examples/ner_example.py  # Test run
   ```

2. **Choose demo script:**
   - Full demo: `python demo/interactive_demo.py`
   - Quick demo: `python demo/quick_demo.py`

3. **Record screen** while running demo

4. **Add narration** using provided script

## 📝 Key Demo Points to Highlight

### Clinical NER Features:
- ✅ Biomedical entity extraction
- ✅ Confidence scoring  
- ✅ Category classification
- ✅ Batch processing

### ICD Recommendations:
- ✅ Top 5 most probable codes
- ✅ Multi-algorithm scoring
- ✅ Keyword matching transparency
- ✅ Specialty categorization

### Workflow Integration:
- ✅ Real-time processing (< 1 second)
- ✅ Batch capabilities
- ✅ Medical coder workflow
- ✅ Quality assurance features

## 🎬 Video Segments Timing

| Segment | Duration | Content |
|---------|----------|---------|
| Intro | 30s | Project overview |
| Clinical NER | 90s | Entity extraction demo |
| ICD Recommendations | 120s | Code recommendation examples |
| Workflow Demo | 60s | Batch processing and real-time |
| Performance | 30s | Speed and accuracy metrics |
| Conclusion | 30s | Call to action and GitHub |

**Total: 6-8 minutes**

## 🔧 Troubleshooting

### Common Issues:
1. **Model download slow**: Pre-download models before recording
2. **Dependencies missing**: Run `pip install -r requirements.txt`
3. **Screen too small**: Increase terminal size and font
4. **Audio sync**: Record video and audio separately, sync in post

### Performance Tips:
1. **Close other applications** to ensure smooth demo
2. **Test run** all demos before recording
3. **Have backup scenarios** ready
4. **Check internet connection** for model downloads

## 📈 Success Metrics

A successful demo video should:
- ✅ Show real medical cases being processed
- ✅ Demonstrate accuracy of recommendations
- ✅ Highlight speed and efficiency
- ✅ Explain technical capabilities clearly
- ✅ Include call-to-action for GitHub

## 🎯 Target Audience

### Primary:
- Medical coding professionals
- Healthcare IT developers
- Medical AI researchers

### Secondary:
- Healthcare administrators
- Medical students
- Open source contributors

## 🔗 Post-Recording

After creating the video:
1. **Upload to YouTube** with proper title and description
2. **Add to README.md** with embedded player
3. **Share on social media** (Twitter, LinkedIn)
4. **Submit to relevant communities** (Reddit, Discord)
5. **Add to GitHub repository** as main showcase

---

**Ready to create an impressive demo video that showcases the power of AI in medical coding!** 🎬✨