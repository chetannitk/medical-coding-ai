"""
Example script demonstrating the Clinical NER utility.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from medical_coding.utils.clinical_ner import ClinicalNER


def example_basic_extraction():
    """Basic entity extraction example."""
    print("=== Basic Clinical NER Example ===\n")
    
    clinical_text = """
    Patient John Doe, 45 years old, presents to the emergency department with severe chest pain 
    radiating to the left arm. He has a history of hypertension and type 2 diabetes mellitus.
    Current medications include metformin 500mg twice daily and lisinopril 10mg once daily.
    Physical examination reveals elevated blood pressure (160/95 mmHg) and mild tachycardia.
    Laboratory results show elevated troponin levels. Recommend immediate cardiology consultation
    and consider starting aspirin and atorvastatin for cardiovascular protection.
    """
    
    ner = ClinicalNER()
    entities = ner.extract_entities(clinical_text)
    
    print(f"Found {len(entities)} clinical entities:\n")
    for i, entity in enumerate(entities, 1):
        print(f"{i}. {entity['text']} ({entity['label']}) - Confidence: {entity['confidence']:.2f}")
    
    return entities


def example_categorized_extraction():
    """Categorized entity extraction example."""
    print("\n=== Categorized Extraction Example ===\n")
    
    clinical_notes = [
        "Patient diagnosed with acute myocardial infarction and pneumonia.",
        "Prescribed insulin for diabetes management and ibuprofen for joint pain.",
        "Imaging shows abnormalities in the heart and lung structures."
    ]
    
    ner = ClinicalNER()
    
    for i, text in enumerate(clinical_notes, 1):
        print(f"Clinical Note {i}: {text}")
        categories = ner.extract_by_category(text)
        
        for category, terms in categories.items():
            print(f"  {category}: {', '.join(terms)}")
        print()


def example_batch_processing():
    """Batch processing example."""
    print("=== Batch Processing Example ===\n")
    
    batch_texts = [
        "Patient complains of chronic headache and fatigue.",
        "Examination reveals inflammation in the stomach area.",
        "Recommend acetaminophen for pain relief and follow-up in two weeks."
    ]
    
    ner = ClinicalNER()
    batch_results = ner.batch_extract(batch_texts)
    
    for i, (text, entities) in enumerate(zip(batch_texts, batch_results), 1):
        print(f"Text {i}: {text}")
        print(f"Entities found: {[e['text'] for e in entities]}")
        print()


def example_summary_statistics():
    """Summary statistics example."""
    print("=== Summary Statistics Example ===\n")
    
    medical_report = """
    Comprehensive medical evaluation reveals multiple conditions requiring attention.
    Patient has diabetes, hypertension, and mild asthma. Experiencing chest pain,
    shortness of breath, and occasional headaches. Currently on metformin for diabetes,
    lisinopril for blood pressure, and uses albuterol inhaler for asthma symptoms.
    Heart and lung function appear compromised. Liver enzymes are elevated.
    Recommend cardiology and pulmonology consultations.
    """
    
    ner = ClinicalNER()
    summary = ner.get_entity_summary(medical_report)
    
    print("Medical Report Summary:")
    print(f"Total entities found: {summary['total_entities']}")
    print(f"Unique entities: {summary['unique_entities']}")
    print(f"Average confidence: {summary['avg_confidence']:.2f}")
    print("\nEntities by category:")
    for category, count in summary['categories'].items():
        print(f"  {category}: {count} terms")


def interactive_example():
    """Interactive example for user input."""
    print("\n=== Interactive Clinical NER ===\n")
    
    ner = ClinicalNER()
    
    print("Enter clinical text to analyze (or 'quit' to exit):")
    while True:
        user_input = input("\n> ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            break
            
        if not user_input:
            continue
            
        entities = ner.extract_entities(user_input)
        
        if entities:
            print(f"\nFound {len(entities)} entities:")
            for entity in entities:
                print(f"  • {entity['text']} ({entity['label']}) - {entity['confidence']:.2f}")
        else:
            print("No clinical entities found.")


def main():
    """Run all examples."""
    try:
        example_basic_extraction()
        example_categorized_extraction()
        example_batch_processing()
        example_summary_statistics()
        
        # Uncomment for interactive mode
        # interactive_example()
        
    except Exception as e:
        print(f"Error running examples: {e}")
        print("Make sure all dependencies are installed: pip install -r requirements.txt")


if __name__ == "__main__":
    main()