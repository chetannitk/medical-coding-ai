"""
Example script demonstrating the ICD Code Recommendation utility for medical coders.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from medical_coding.utils.icd_recommender import ICDRecommender


def example_basic_recommendations():
    """Basic ICD code recommendation example."""
    print("=== Basic ICD Code Recommendations ===\n")
    
    # Initialize the recommender
    recommender = ICDRecommender()
    
    # Sample diagnosis texts that medical coders might encounter
    diagnosis_texts = [
        "Patient presents with acute chest pain, shortness of breath, and elevated troponin levels. ECG shows ST elevation.",
        "67-year-old male with type 2 diabetes mellitus, HbA1c 9.2%, complaining of polyuria and polydipsia.",
        "Female patient with chronic obstructive pulmonary disease exacerbation, increased dyspnea, productive cough.",
        "Patient reports severe recurring headaches with photophobia and nausea, lasting 4-6 hours.",
        "45-year-old with persistent depressed mood, anhedonia, and sleep disturbances for past 3 weeks."
    ]
    
    for i, diagnosis in enumerate(diagnosis_texts, 1):
        print(f"Case {i}:")
        print(f"Diagnosis: {diagnosis}")
        print("\nTop 5 ICD Code Recommendations:")
        print("-" * 50)
        
        recommendations = recommender.recommend_icd_codes(diagnosis, top_k=5)
        
        for rank, rec in enumerate(recommendations, 1):
            print(f"{rank}. {rec['icd_code']} ({rec['confidence_score']})")
            print(f"   {rec['description']}")
            print(f"   Category: {rec['category']}")
            if rec['matched_keywords']:
                print(f"   Keywords matched: {', '.join(rec['matched_keywords'])}")
            print()
        
        print("=" * 60)
        print()


def example_medical_coder_workflow():
    """Simulate a medical coder's workflow with ICD recommendations."""
    print("=== Medical Coder Workflow Simulation ===\n")
    
    recommender = ICDRecommender()
    
    # Simulate a complex medical case
    complex_case = """
    Patient: 58-year-old male with past medical history significant for hypertension 
    and hyperlipidemia presents to ED with acute onset severe chest pain radiating 
    to left arm, associated with diaphoresis and nausea. Vitals show BP 180/100, 
    HR 110. ECG reveals ST elevation in leads II, III, aVF. Troponin elevated at 15.2. 
    Echo shows inferior wall motion abnormality. Patient also has background diabetes 
    mellitus type 2 on metformin with recent HbA1c of 8.5%.
    """
    
    print("Complex Medical Case:")
    print(complex_case)
    print("\nMedical Coder Analysis:")
    print("-" * 40)
    
    # Get recommendations
    recommendations = recommender.recommend_icd_codes(complex_case, top_k=5)
    
    print("Primary Diagnosis Recommendations:")
    for i, rec in enumerate(recommendations, 1):
        confidence_level = "High" if rec['confidence_score'] > 0.7 else "Medium" if rec['confidence_score'] > 0.4 else "Low"
        print(f"{i}. {rec['icd_code']} - {rec['description']}")
        print(f"   Confidence: {rec['confidence_score']} ({confidence_level})")
        print(f"   Specialty: {rec['category']}")
        print()
    
    # Show category distribution to help coder understand which specialties are involved
    print("Specialty Distribution Analysis:")
    distribution = recommender.get_category_distribution(complex_case)
    for category, score in distribution.items():
        bar_length = int(score * 20)  # Visual bar representation
        bar = "█" * bar_length + "░" * (20 - bar_length)
        print(f"{category:15} [{bar}] {score}")
    print()


def example_batch_processing():
    """Example of batch processing multiple cases."""
    print("=== Batch Processing Example ===\n")
    
    recommender = ICDRecommender()
    
    # Multiple cases from a medical coder's daily workload
    daily_cases = [
        "Acute MI with STEMI",
        "T2DM with diabetic nephropathy",
        "COPD exacerbation with respiratory failure",
        "Major depressive disorder, recurrent episode",
        "Essential hypertension, uncontrolled",
        "Migraine without aura",
        "Gastroesophageal reflux disease",
        "Chronic kidney disease stage 3"
    ]
    
    print(f"Processing {len(daily_cases)} cases in batch...")
    
    # Batch process all cases
    batch_results = recommender.batch_recommend(daily_cases, top_k=3)
    
    print("\nBatch Processing Results Summary:")
    print("-" * 50)
    
    for i, (case, recommendations) in enumerate(zip(daily_cases, batch_results), 1):
        print(f"Case {i}: {case}")
        
        if recommendations:
            top_recommendation = recommendations[0]
            print(f"   → Primary: {top_recommendation['icd_code']} ({top_recommendation['confidence_score']})")
            print(f"     {top_recommendation['description']}")
        else:
            print("   → No recommendations found")
        print()


def example_keyword_search():
    """Example of searching ICD codes by keywords."""
    print("=== Keyword Search for Medical Coders ===\n")
    
    recommender = ICDRecommender()
    
    # Common search terms medical coders might use
    search_terms = ["diabetes", "heart", "pneumonia", "depression", "hypertension"]
    
    for term in search_terms:
        print(f"Searching for: '{term}'")
        results = recommender.search_by_keyword(term, max_results=3)
        
        for result in results:
            print(f"  {result['icd_code']} - {result['description']}")
        print()


def example_interactive_coder_assistant():
    """Interactive assistant for medical coders."""
    print("=== Interactive Medical Coder Assistant ===\n")
    print("Enter diagnosis text for ICD code recommendations (or 'quit' to exit)")
    print("Example: 'Patient with chest pain and elevated troponin'")
    
    recommender = ICDRecommender()
    
    while True:
        print("\n" + "-" * 50)
        user_input = input("Diagnosis: ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("Thank you for using the ICD Code Assistant!")
            break
        
        if not user_input:
            continue
        
        print("\nAnalyzing diagnosis...")
        recommendations = recommender.recommend_icd_codes(user_input, top_k=5)
        
        if recommendations:
            print(f"\nTop {len(recommendations)} ICD Code Recommendations:")
            print("-" * 40)
            
            for i, rec in enumerate(recommendations, 1):
                confidence_indicator = "🟢" if rec['confidence_score'] > 0.7 else "🟡" if rec['confidence_score'] > 0.4 else "🔴"
                print(f"{i}. {confidence_indicator} {rec['icd_code']}")
                print(f"   {rec['description']}")
                print(f"   Confidence: {rec['confidence_score']:.3f} | Category: {rec['category']}")
                print()
            
            # Ask if user wants more details
            detail_input = input("Enter code number for details (or press Enter to continue): ").strip()
            if detail_input.isdigit():
                code_idx = int(detail_input) - 1
                if 0 <= code_idx < len(recommendations):
                    selected = recommendations[code_idx]
                    details = recommender.get_code_details(selected['icd_code'])
                    if details:
                        print(f"\nDetailed Information for {selected['icd_code']}:")
                        print(f"Description: {details['description']}")
                        print(f"Category: {details['category']}")
                        print(f"Keywords: {', '.join(details['keywords'])}")
        else:
            print("No ICD code recommendations found. Try rephrasing the diagnosis.")


def main():
    """Run all examples."""
    try:
        example_basic_recommendations()
        example_medical_coder_workflow()
        example_batch_processing()
        example_keyword_search()
        
        # Uncomment for interactive mode
        # example_interactive_coder_assistant()
        
    except Exception as e:
        print(f"Error running examples: {e}")
        print("Make sure all dependencies are installed and the clinical NER model is available.")


if __name__ == "__main__":
    main()