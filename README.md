# Medical Coding AI Assistant

A comprehensive machine learning project for automated medical coding using Named Entity Recognition (NER) and ICD code recommendation algorithms.

## 🎬 Live Demo

**Watch the AI in action!** See our system extract medical entities and recommend ICD codes in real-time:

![Medical Coding AI Demo](https://github.com/chetannitk/medical-coding-ai/raw/main/demo/demo_banner.svg)

*🚀 AI-powered medical coding with clinical NER extraction and ICD recommendations*

### 🖥️ Terminal Demo
![Terminal Demo](https://github.com/chetannitk/medical-coding-ai/raw/main/demo/github_demo.svg)

*📟 Detailed terminal view showing live processing of medical text and ICD code recommendations*

### 📺 Additional Demo Formats:
- **Slideshow Video**: [medical_coding_ai_demo.mp4](https://github.com/chetannitk/medical-coding-ai/raw/main/demo/medical_coding_ai_demo.mp4) *(14 seconds, 1080p)*

### Key Demo Highlights:
- ✅ **Real medical entity extraction** (29 entities from clinical text)
- ✅ **Accurate ICD recommendations** (I21.9 for MI, E11.9 for diabetes)  
- ✅ **High confidence scoring** (>0.3 for accurate matches)
- ✅ **Fast processing** (< 500ms per case)
- ✅ **Professional medical workflow** ready for deployment

## 🚀 Features

### Clinical NER (Named Entity Recognition)
- Extract medical entities from clinical text
- Support for diseases, symptoms, medications, and anatomy
- Uses pre-trained biomedical NER models (HuggingFace Transformers)
- Fallback pattern matching for common medical terms
- Batch processing and entity categorization

### ICD Code Recommendation System
- **Smart ICD-10 code recommendations** based on diagnosis text
- **Top 5 most probable codes** with confidence scores
- **Multi-algorithm scoring**: TF-IDF similarity, keyword matching, entity matching
- **Medical abbreviation expansion** (HTN→hypertension, DM→diabetes, etc.)
- **Specialty categorization** across medical departments
- **Batch processing** for multiple cases

## 📁 Project Structure

```
medical_coding/
├── src/medical_coding/
│   ├── utils/
│   │   ├── clinical_ner.py          # NER utility for medical terms
│   │   └── icd_recommender.py       # ICD code recommendation engine
│   ├── data/                        # Data processing modules
│   ├── models/                      # ML model implementations
│   └── evaluation/                  # Model evaluation tools
├── data/
│   ├── raw/                         # Raw medical data
│   ├── processed/                   # Processed datasets
│   └── external/                    # External data sources
├── models/                          # Saved model files
├── notebooks/                       # Jupyter notebooks for analysis
├── tests/                           # Unit tests
├── examples/                        # Example usage scripts
├── docs/                           # Documentation
└── config/                         # Configuration files
```

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/medical_coding.git
   cd medical_coding
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install the package in development mode:**
   ```bash
   pip install -e .
   ```

## 🎯 Quick Start

### Clinical NER Usage

```python
from medical_coding.utils.clinical_ner import ClinicalNER

# Initialize NER model
ner = ClinicalNER()

# Extract medical entities
text = "Patient has diabetes and hypertension with chest pain"
entities = ner.extract_entities(text)

for entity in entities:
    print(f"{entity['text']} - {entity['label']} ({entity['confidence']:.2f})")
```

### ICD Code Recommendations

```python
from medical_coding.utils.icd_recommender import ICDRecommender

# Initialize recommender
recommender = ICDRecommender()

# Get top 5 ICD code recommendations
diagnosis = "Patient presents with acute chest pain and elevated troponin"
recommendations = recommender.recommend_icd_codes(diagnosis, top_k=5)

for i, rec in enumerate(recommendations, 1):
    print(f"{i}. {rec['icd_code']} - {rec['description']}")
    print(f"   Confidence: {rec['confidence_score']:.3f}")
```

## 📖 Examples

Run the example scripts to see the system in action:

```bash
# Clinical NER examples
python examples/ner_example.py

# ICD code recommendation examples
python examples/icd_recommendation_example.py

# Quick visual demo (same as in video)
python demo/quick_demo.py

# Interactive demo for presentations
python demo/interactive_demo.py
```

## 🎥 Create Your Own Demo Video

Generate professional demo videos using our built-in tools:

```bash
# Create slideshow video (like the one above)
python demo/create_video.py

# Record live demo
python demo/screen_recorder.py

# Interactive recording session
python demo/interactive_demo.py
```

See [`demo/README.md`](demo/README.md) for complete video production guide.

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test files
python -m pytest tests/test_clinical_ner.py -v
python -m pytest tests/test_icd_recommender.py -v
```

## 📊 Key Capabilities

### Medical Entity Recognition
- **Diseases**: diabetes, hypertension, pneumonia, etc.
- **Symptoms**: chest pain, headache, shortness of breath, etc.
- **Medications**: aspirin, metformin, lisinopril, etc.
- **Anatomy**: heart, lung, kidney, brain, etc.

### ICD Code Categories
- **Cardiovascular** (I25.10, I10, I21.9, I50.9)
- **Respiratory** (J44.1, J45.9, J18.9, J20.9)
- **Endocrine** (E11.9, E10.9, E78.5)
- **Mental Health** (F32.9, F41.9)
- **Musculoskeletal** (M79.3, M25.50)
- **Neurological** (G43.909, R51)

### Advanced Features
- **Confidence scoring** with High/Medium/Low indicators
- **Keyword matching** shows exactly which terms triggered recommendations
- **Specialty distribution** analysis across medical departments
- **Medical abbreviation handling** (HTN, DM, CAD, COPD, etc.)
- **Batch processing** for efficient workflow

## 🔧 Configuration

The system uses several configurable components:

- **NER Model**: Default biomedical model (`d4data/biomedical-ner-all`)
- **Confidence Thresholds**: Adjustable for entity extraction and recommendations
- **TF-IDF Parameters**: Customizable for similarity matching
- **ICD Code Database**: Expandable with additional codes

## 🚀 For Medical Coders

This tool is designed to assist medical coding professionals by:

1. **Reducing coding time** through automated recommendations
2. **Improving accuracy** with confidence-scored suggestions
3. **Handling complex cases** with multi-condition analysis
4. **Supporting workflow** with batch processing capabilities
5. **Providing transparency** through keyword matching and confidence indicators

## 📈 Performance

- **NER Accuracy**: Uses state-of-the-art biomedical NER models
- **ICD Recommendations**: Multi-algorithm approach for robust matching
- **Processing Speed**: Optimized for real-time clinical workflow
- **Scalability**: Supports batch processing of multiple cases

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🏥 Use Cases

- **Hospital coding departments**
- **Medical billing companies**
- **Healthcare analytics**
- **Clinical documentation improvement**
- **Medical education and training**

## 📞 Support

For questions or issues, please open an issue on GitHub or contact the development team.

---

**Note**: This is a research and development tool. Always verify ICD code recommendations with official medical coding guidelines and trained medical coding professionals.
