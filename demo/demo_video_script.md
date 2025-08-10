# Medical Coding AI Assistant - Demo Video Script

## Video Structure (Total Time: 8-10 minutes)

### 🎬 **Scene 1: Introduction (30 seconds)**
**[Screen: Project title and overview]**

**Narrator:**
"Welcome to the Medical Coding AI Assistant - an intelligent system that helps medical coders automatically extract clinical information and recommend ICD codes from medical text. This project combines Named Entity Recognition with advanced ICD code recommendation algorithms."

**[Show project structure on screen]**

---

### 🎬 **Scene 2: Project Overview (45 seconds)**
**[Screen: Terminal showing project structure]**

**Narrator:**
"Our system has two main components: First, a Clinical NER utility that extracts medical entities like diseases, symptoms, and medications from clinical text. Second, an ICD Code Recommendation engine that suggests the top 5 most probable ICD-10 codes based on diagnosis descriptions."

**[Show directory structure with tree command]**

---

### 🎬 **Scene 3: Clinical NER Demo (2 minutes)**
**[Screen: Running Clinical NER example]**

**Narrator:**
"Let's start with the Clinical NER system. I'll run our NER example to show how it extracts medical entities from clinical text."

**[Terminal commands to demonstrate:]**
```bash
cd medical_coding
python examples/ner_example.py
```

**[Show real-time output highlighting:]**
- Medical entities being extracted
- Confidence scores
- Entity categories (Disease, Symptom, Medication, Anatomy)
- Batch processing capabilities

**Narrator:**
"As you can see, the system accurately identifies medical terms like 'diabetes', 'chest pain', and 'metformin' with high confidence scores. It categorizes them by type and can process multiple texts in batch."

---

### 🎬 **Scene 4: ICD Code Recommendation Demo (3 minutes)**
**[Screen: Running ICD recommendation example]**

**Narrator:**
"Now let's see the ICD code recommendation system in action. This is the core feature that medical coders will use daily."

**[Terminal commands:]**
```bash
python examples/icd_recommendation_example.py
```

**[Highlight key demonstrations:]**

1. **Basic Recommendations:**
   - Show complex medical case input
   - Display top 5 ICD code recommendations
   - Point out confidence scores and matched keywords

2. **Medical Coder Workflow:**
   - Complex multi-condition case
   - Specialty distribution analysis
   - Primary vs secondary diagnosis suggestions

3. **Batch Processing:**
   - Multiple cases processed together
   - Efficiency for daily workflow

**Narrator:**
"Notice how the system correctly identifies 'Type 2 diabetes mellitus' as E11.9 with high confidence, and 'acute myocardial infarction' as I21.9. The keyword matching shows exactly why each code was recommended."

---

### 🎬 **Scene 5: Interactive Demo (2 minutes)**
**[Screen: Custom interactive session]**

**Narrator:**
"Let's do a live demonstration where I'll input real medical scenarios and show how the system responds in real-time."

**[Live typing scenarios:]**

1. **Scenario 1:** "67-year-old female with acute chest pain, elevated troponin, and EKG changes"
   - Show immediate ICD recommendations
   - Highlight I21.9 (Acute MI) as top recommendation

2. **Scenario 2:** "Patient with chronic cough, wheezing, and smoking history"
   - Show J44.1 (COPD) recommendation
   - Demonstrate specialty categorization

3. **Scenario 3:** "Persistent headache with photophobia and nausea"
   - Show G43.909 (Migraine) recommendation
   - Show confidence scoring

**Narrator:**
"The system processes each query in real-time, providing medical coders with immediate, accurate recommendations that can significantly speed up their workflow."

---

### 🎬 **Scene 6: Technical Features (1 minute)**
**[Screen: Code snippets and architecture]**

**Narrator:**
"Behind the scenes, our system uses several advanced techniques:"

**[Show bullet points with visuals:]**
- Pre-trained biomedical NER models from HuggingFace
- TF-IDF vectorization for semantic similarity
- Medical abbreviation expansion (HTN → hypertension)
- Multi-algorithm confidence scoring
- Fallback pattern matching for robustness

**[Show test results:]**
```bash
python -m pytest tests/ -v
```

**Narrator:**
"The system is thoroughly tested with over 30 test cases ensuring reliability and accuracy."

---

### 🎬 **Scene 7: Real-World Applications (30 seconds)**
**[Screen: Use case graphics]**

**Narrator:**
"This system is designed for:"

**[Show use cases with icons:]**
- Hospital coding departments
- Medical billing companies
- Healthcare analytics
- Clinical documentation improvement
- Medical education and training

---

### 🎬 **Scene 8: Installation and Setup (30 seconds)**
**[Screen: Installation commands]**

**Narrator:**
"Getting started is simple. Clone the repository, install dependencies, and you're ready to go."

**[Show commands:]**
```bash
git clone https://github.com/yourusername/medical-coding-ai.git
cd medical-coding-ai
pip install -r requirements.txt
python examples/icd_recommendation_example.py
```

---

### 🎬 **Scene 9: Performance Metrics (30 seconds)**
**[Screen: Performance highlights]**

**Narrator:**
"Our system delivers impressive results:"

**[Show metrics:]**
- Accurate entity extraction with biomedical NER
- Top 5 ICD recommendations with confidence scores
- Real-time processing for clinical workflow
- Support for 20+ ICD categories
- Batch processing capabilities

---

### 🎬 **Scene 10: Conclusion and Call to Action (30 seconds)**
**[Screen: GitHub repository and contact info]**

**Narrator:**
"The Medical Coding AI Assistant represents a significant advancement in automated medical coding. It's open source, extensible, and ready for integration into existing healthcare workflows. Visit our GitHub repository to try it out, contribute, or learn more. Thank you for watching!"

**[Show final screen with:]**
- GitHub repository URL
- Star/Fork buttons
- Contact information
- License information

---

## 🎥 **Recording Tips:**

### **Screen Setup:**
1. Use a clean terminal with good contrast
2. Increase font size for visibility
3. Use syntax highlighting for code
4. Clear screen between major sections

### **Demo Environment:**
1. Fresh terminal session
2. All dependencies pre-installed
3. Sample data ready
4. Stable internet for model downloads

### **Timing:**
- Speak clearly and at moderate pace
- Pause between major concepts
- Allow time for viewers to read output
- Use transitions between sections

### **Visual Enhancement:**
1. Highlight important text with cursor
2. Use terminal colors effectively
3. Show typing for live feel
4. Include progress indicators where relevant

---

## 🔧 **Pre-Demo Checklist:**

- [ ] All dependencies installed
- [ ] NER models downloaded and working
- [ ] Example scripts tested
- [ ] Clean project directory
- [ ] Good lighting and audio setup
- [ ] Screen recording software ready
- [ ] Backup scenarios prepared