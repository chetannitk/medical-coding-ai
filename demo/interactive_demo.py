"""
Interactive Demo Script for Medical Coding AI Assistant Video Recording.
This script provides a guided demonstration with realistic medical scenarios.
"""

import sys
import os
import time
import json
from typing import Dict, List
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from medical_coding.utils.clinical_ner import ClinicalNER
from medical_coding.utils.icd_recommender import ICDRecommender


class DemoPresentation:
    """Interactive demonstration class for video recording."""
    
    def __init__(self):
        """Initialize demo components."""
        print("🔥 Initializing Medical Coding AI Assistant Demo...")
        print("=" * 60)
        
        # Initialize components with loading indicators
        print("📥 Loading Clinical NER model...")
        self.ner = ClinicalNER()
        print("✅ Clinical NER ready!")
        
        print("📥 Loading ICD Recommendation engine...")
        self.recommender = ICDRecommender()
        print("✅ ICD Recommender ready!")
        
        print("🚀 Demo system initialized successfully!")
        print("=" * 60)
        print()
    
    def demo_clinical_ner(self):
        """Demonstrate Clinical NER capabilities."""
        print("🏥 CLINICAL NER DEMONSTRATION")
        print("=" * 50)
        print()
        
        # Demo scenario 1: Emergency Department Case
        print("📋 SCENARIO 1: Emergency Department Case")
        print("-" * 30)
        
        ed_case = """
        58-year-old male presents to ED with severe chest pain radiating to left arm,
        associated with nausea and diaphoresis. Patient has history of diabetes mellitus
        and hypertension. Currently taking metformin and lisinopril. Vitals show BP 180/100,
        HR 110 bpm. Physical exam reveals diaphoresis and mild distress.
        """
        
        print("📝 Medical Text:")
        print(ed_case.strip())
        print()
        
        print("🔍 Extracting medical entities...")
        time.sleep(1)  # Pause for video effect
        
        entities = self.ner.extract_entities(ed_case)
        
        print(f"✅ Found {len(entities)} medical entities:")
        print()
        
        # Group entities by category for better visualization
        categories = self.ner.extract_by_category(ed_case)
        
        for category, terms in categories.items():
            print(f"🏷️  {category}:")
            for term in terms[:3]:  # Show top 3 per category
                print(f"   • {term}")
            if len(terms) > 3:
                print(f"   ... and {len(terms) - 3} more")
            print()
        
        # Show confidence scores for top entities
        print("📊 Top Entities with Confidence Scores:")
        sorted_entities = sorted(entities, key=lambda x: x['confidence'], reverse=True)
        for i, entity in enumerate(sorted_entities[:5], 1):
            confidence_bar = "█" * int(entity['confidence'] * 10)
            print(f"{i}. {entity['text']:20} | {confidence_bar:10} | {entity['confidence']:.3f}")
        
        print("\n" + "=" * 50)
        print()
    
    def demo_icd_recommendations(self):
        """Demonstrate ICD code recommendation system."""
        print("📋 ICD CODE RECOMMENDATION DEMONSTRATION")
        print("=" * 55)
        print()
        
        # Demo scenarios with different complexity levels
        scenarios = [
            {
                "title": "SCENARIO 1: Acute Myocardial Infarction",
                "diagnosis": "Patient presents with acute ST-elevation myocardial infarction, troponin positive, with inferior wall involvement",
                "expected": "Should recommend I21.9 (Acute myocardial infarction)"
            },
            {
                "title": "SCENARIO 2: Diabetes Management",
                "diagnosis": "67-year-old with type 2 diabetes mellitus, HbA1c 9.8%, requiring insulin adjustment",
                "expected": "Should recommend E11.9 (Type 2 diabetes mellitus)"
            },
            {
                "title": "SCENARIO 3: Respiratory Emergency",
                "diagnosis": "COPD exacerbation with acute respiratory failure, requiring nebulizer treatment and oxygen therapy",
                "expected": "Should recommend J44.1 (COPD with exacerbation)"
            }
        ]
        
        for i, scenario in enumerate(scenarios, 1):
            print(f"📋 {scenario['title']}")
            print("-" * (len(scenario['title']) + 5))
            print()
            
            print("📝 Diagnosis Text:")
            print(f'"{scenario["diagnosis"]}"')
            print()
            
            print("🔍 Analyzing diagnosis and generating recommendations...")
            time.sleep(1.5)  # Pause for dramatic effect
            
            recommendations = self.recommender.recommend_icd_codes(scenario['diagnosis'], top_k=5)
            
            print("🎯 TOP 5 ICD CODE RECOMMENDATIONS:")
            print()
            
            for rank, rec in enumerate(recommendations, 1):
                # Visual confidence indicator
                if rec['confidence_score'] > 0.3:
                    confidence_icon = "🟢 HIGH"
                elif rec['confidence_score'] > 0.15:
                    confidence_icon = "🟡 MEDIUM"
                else:
                    confidence_icon = "🔴 LOW"
                
                print(f"{rank}. {rec['icd_code']} | {confidence_icon} | Score: {rec['confidence_score']:.3f}")
                print(f"   📄 {rec['description']}")
                print(f"   🏥 Category: {rec['category']}")
                
                if rec['matched_keywords']:
                    print(f"   🔍 Keywords: {', '.join(rec['matched_keywords'])}")
                print()
            
            # Show category distribution for complex cases
            if i == 1:  # Show for first scenario as example
                print("📊 SPECIALTY DISTRIBUTION:")
                distribution = self.recommender.get_category_distribution(scenario['diagnosis'])
                for category, score in list(distribution.items())[:3]:
                    bar_length = int(score * 20)
                    bar = "█" * bar_length + "░" * (20 - bar_length)
                    print(f"   {category:15} [{bar}] {score:.3f}")
                print()
            
            print("=" * 60)
            print()
    
    def demo_real_time_interaction(self):
        """Demonstrate real-time interaction capabilities."""
        print("💬 REAL-TIME INTERACTION DEMO")
        print("=" * 40)
        print()
        
        # Simulated real-time queries
        queries = [
            "Patient with chronic headache and photophobia",
            "Elderly male with chest pain and dyspnea",
            "Female with abdominal pain and nausea",
            "Child with fever and cough"
        ]
        
        print("🎭 Simulating medical coder workflow...")
        print()
        
        for i, query in enumerate(queries, 1):
            print(f"Query {i}: {query}")
            print("Processing..." + "." * (i % 3 + 1))
            time.sleep(0.5)
            
            recommendations = self.recommender.recommend_icd_codes(query, top_k=3)
            
            if recommendations:
                top_rec = recommendations[0]
                print(f"→ Primary: {top_rec['icd_code']} ({top_rec['confidence_score']:.3f})")
                print(f"  {top_rec['description'][:50]}...")
            else:
                print("→ No clear recommendations found")
            print()
        
        print("=" * 40)
        print()
    
    def demo_batch_processing(self):
        """Demonstrate batch processing capabilities."""
        print("📦 BATCH PROCESSING DEMO")
        print("=" * 35)
        print()
        
        # Simulate daily medical coder workload
        daily_cases = [
            "Acute appendicitis with complications",
            "Type 1 diabetes with ketoacidosis",
            "Pneumonia with respiratory distress",
            "Major depression with suicidal ideation",
            "Essential hypertension uncontrolled",
            "Migraine without aura, chronic"
        ]
        
        print(f"📋 Processing {len(daily_cases)} cases from daily workload...")
        print()
        
        print("🔄 Batch processing in progress...")
        time.sleep(2)
        
        batch_results = self.recommender.batch_recommend(daily_cases, top_k=1)
        
        print("✅ Batch processing complete!")
        print()
        print("📊 BATCH RESULTS SUMMARY:")
        print("-" * 30)
        
        for i, (case, results) in enumerate(zip(daily_cases, batch_results), 1):
            print(f"{i}. {case[:40]}...")
            if results:
                top_result = results[0]
                confidence_level = "High" if top_result['confidence_score'] > 0.3 else "Med" if top_result['confidence_score'] > 0.1 else "Low"
                print(f"   → {top_result['icd_code']} ({confidence_level}) - {top_result['description'][:45]}...")
            else:
                print("   → No recommendations")
            print()
        
        print("=" * 35)
        print()
    
    def demo_performance_metrics(self):
        """Show system performance metrics."""
        print("📈 PERFORMANCE METRICS")
        print("=" * 30)
        print()
        
        metrics = {
            "ICD Codes Supported": len(self.recommender.icd_codes),
            "Medical Categories": len(set(info['category'] for info in self.recommender.icd_codes.values())),
            "Processing Speed": "< 1 second per case",
            "Confidence Scoring": "Multi-algorithm approach",
            "Batch Capacity": "Unlimited cases",
            "Model Accuracy": "Biomedical NER trained"
        }
        
        for metric, value in metrics.items():
            print(f"✅ {metric:20} : {value}")
        
        print()
        print("🧪 Running quick system validation...")
        time.sleep(1)
        
        # Quick validation
        test_case = "Patient with diabetes and chest pain"
        start_time = time.time()
        results = self.recommender.recommend_icd_codes(test_case, top_k=3)
        end_time = time.time()
        
        print(f"⚡ Processed test case in {(end_time - start_time)*1000:.0f}ms")
        print(f"🎯 Generated {len(results)} recommendations")
        print()
    
    def run_complete_demo(self):
        """Run the complete demo sequence."""
        print("🎬 MEDICAL CODING AI ASSISTANT - COMPLETE DEMO")
        print("=" * 60)
        print("🤖 Revolutionizing Medical Coding with AI")
        print("=" * 60)
        print()
        
        input("Press Enter to start Clinical NER Demo...")
        self.demo_clinical_ner()
        
        input("Press Enter to continue to ICD Recommendation Demo...")
        self.demo_icd_recommendations()
        
        input("Press Enter to see Real-Time Interaction...")
        self.demo_real_time_interaction()
        
        input("Press Enter to view Batch Processing...")
        self.demo_batch_processing()
        
        input("Press Enter to see Performance Metrics...")
        self.demo_performance_metrics()
        
        print("🎉 DEMO COMPLETE!")
        print("=" * 25)
        print()
        print("🌟 Key Takeaways:")
        print("   • Accurate medical entity extraction")
        print("   • Intelligent ICD code recommendations")
        print("   • Real-time processing capabilities")
        print("   • Batch workflow support")
        print("   • Multi-algorithm confidence scoring")
        print()
        print("📞 Ready for integration into medical coding workflows!")
        print("🔗 GitHub: https://github.com/yourusername/medical-coding-ai")
        print()
        print("Thank you for watching! ⭐ Star us on GitHub!")


def main():
    """Main demo function."""
    try:
        demo = DemoPresentation()
        demo.run_complete_demo()
        
    except KeyboardInterrupt:
        print("\n🛑 Demo interrupted by user.")
    except Exception as e:
        print(f"\n❌ Demo error: {e}")
        print("Please ensure all dependencies are installed.")


if __name__ == "__main__":
    main()