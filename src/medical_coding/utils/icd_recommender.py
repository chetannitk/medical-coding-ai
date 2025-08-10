"""
ICD Code Recommendation utility for medical coding based on diagnosis text.
"""

import re
import json
from typing import List, Dict, Tuple, Optional, Union
from collections import Counter
import difflib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from .clinical_ner import ClinicalNER


class ICDRecommender:
    """
    A utility class for recommending ICD codes based on medical diagnosis text.
    """
    
    def __init__(self, ner_model: Optional[ClinicalNER] = None):
        """
        Initialize the ICD Recommender.
        
        Args:
            ner_model (ClinicalNER, optional): Pre-trained NER model instance
        """
        self.ner = ner_model or ClinicalNER()
        self.icd_codes = self._load_icd_codes()
        self.vectorizer = None
        self.icd_vectors = None
        self._initialize_vectorizer()
    
    def _load_icd_codes(self) -> Dict[str, Dict]:
        """
        Load ICD-10 codes with descriptions and keywords.
        In a real implementation, this would load from a comprehensive database.
        """
        icd_codes = {
            # Cardiovascular diseases
            "I25.10": {
                "description": "Atherosclerotic heart disease of native coronary artery without angina pectoris",
                "keywords": ["atherosclerotic heart disease", "coronary artery disease", "CAD", "heart disease", "coronary atherosclerosis"],
                "category": "Cardiovascular"
            },
            "I25.9": {
                "description": "Chronic ischemic heart disease, unspecified",
                "keywords": ["ischemic heart disease", "chronic ischemia", "heart ischemia", "coronary ischemia"],
                "category": "Cardiovascular"
            },
            "I10": {
                "description": "Essential (primary) hypertension",
                "keywords": ["hypertension", "high blood pressure", "elevated blood pressure", "HTN", "primary hypertension"],
                "category": "Cardiovascular"
            },
            "I21.9": {
                "description": "Acute myocardial infarction, unspecified",
                "keywords": ["myocardial infarction", "heart attack", "MI", "acute MI", "cardiac infarction"],
                "category": "Cardiovascular"
            },
            "I50.9": {
                "description": "Heart failure, unspecified",
                "keywords": ["heart failure", "cardiac failure", "congestive heart failure", "CHF", "heart insufficiency"],
                "category": "Cardiovascular"
            },
            
            # Respiratory diseases
            "J44.1": {
                "description": "Chronic obstructive pulmonary disease with acute exacerbation",
                "keywords": ["COPD", "chronic obstructive pulmonary disease", "emphysema", "chronic bronchitis", "obstructive lung disease"],
                "category": "Respiratory"
            },
            "J45.9": {
                "description": "Asthma, unspecified",
                "keywords": ["asthma", "bronchial asthma", "allergic asthma", "asthmatic", "bronchospasm"],
                "category": "Respiratory"
            },
            "J18.9": {
                "description": "Pneumonia, unspecified organism",
                "keywords": ["pneumonia", "lung infection", "pulmonary infection", "pneumonitis", "chest infection"],
                "category": "Respiratory"
            },
            "J20.9": {
                "description": "Acute bronchitis, unspecified",
                "keywords": ["acute bronchitis", "bronchitis", "bronchial inflammation", "chest cold"],
                "category": "Respiratory"
            },
            
            # Endocrine diseases
            "E11.9": {
                "description": "Type 2 diabetes mellitus without complications",
                "keywords": ["diabetes", "type 2 diabetes", "diabetes mellitus", "T2DM", "adult onset diabetes", "non-insulin dependent diabetes"],
                "category": "Endocrine"
            },
            "E10.9": {
                "description": "Type 1 diabetes mellitus without complications",
                "keywords": ["type 1 diabetes", "T1DM", "insulin dependent diabetes", "juvenile diabetes"],
                "category": "Endocrine"
            },
            "E78.5": {
                "description": "Hyperlipidemia, unspecified",
                "keywords": ["hyperlipidemia", "high cholesterol", "dyslipidemia", "elevated lipids", "hypercholesterolemia"],
                "category": "Endocrine"
            },
            
            # Gastrointestinal diseases
            "K21.9": {
                "description": "Gastro-esophageal reflux disease without esophagitis",
                "keywords": ["GERD", "gastroesophageal reflux", "acid reflux", "heartburn", "reflux disease"],
                "category": "Gastrointestinal"
            },
            "K59.00": {
                "description": "Constipation, unspecified",
                "keywords": ["constipation", "chronic constipation", "bowel irregularity", "difficult defecation"],
                "category": "Gastrointestinal"
            },
            
            # Mental health
            "F32.9": {
                "description": "Major depressive disorder, single episode, unspecified",
                "keywords": ["depression", "major depression", "depressive disorder", "clinical depression", "major depressive episode"],
                "category": "Mental Health"
            },
            "F41.9": {
                "description": "Anxiety disorder, unspecified",
                "keywords": ["anxiety", "anxiety disorder", "generalized anxiety", "panic disorder", "anxious"],
                "category": "Mental Health"
            },
            
            # Musculoskeletal
            "M79.3": {
                "description": "Panniculitis, unspecified",
                "keywords": ["chronic pain", "musculoskeletal pain", "body pain", "widespread pain"],
                "category": "Musculoskeletal"
            },
            "M25.50": {
                "description": "Pain in unspecified joint",
                "keywords": ["joint pain", "arthralgia", "joint ache", "articular pain"],
                "category": "Musculoskeletal"
            },
            
            # Neurological
            "G43.909": {
                "description": "Migraine, unspecified, not intractable, without status migrainosus",
                "keywords": ["migraine", "headache", "severe headache", "migrainous headache"],
                "category": "Neurological"
            },
            "R51": {
                "description": "Headache",
                "keywords": ["headache", "cephalgia", "head pain"],
                "category": "Neurological"
            }
        }
        
        return icd_codes
    
    def _initialize_vectorizer(self):
        """Initialize TF-IDF vectorizer with ICD code descriptions and keywords."""
        # Combine descriptions and keywords for each ICD code
        corpus = []
        for code, info in self.icd_codes.items():
            text = f"{info['description']} {' '.join(info['keywords'])}"
            corpus.append(text.lower())
        
        # Initialize and fit vectorizer
        self.vectorizer = TfidfVectorizer(
            stop_words='english',
            ngram_range=(1, 3),
            max_features=5000,
            min_df=1
        )
        
        self.icd_vectors = self.vectorizer.fit_transform(corpus)
    
    def preprocess_diagnosis_text(self, text: str) -> str:
        """
        Preprocess diagnosis text for better matching.
        
        Args:
            text (str): Raw diagnosis text
            
        Returns:
            str: Preprocessed text
        """
        # Convert to lowercase
        text = text.lower()
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Expand common medical abbreviations
        abbreviations = {
            'htn': 'hypertension',
            'dm': 'diabetes mellitus',
            'cad': 'coronary artery disease',
            'chf': 'congestive heart failure',
            'copd': 'chronic obstructive pulmonary disease',
            'gerd': 'gastroesophageal reflux disease',
            'mi': 'myocardial infarction',
            'cvd': 'cardiovascular disease',
            'ckd': 'chronic kidney disease',
            'uti': 'urinary tract infection',
            'dvt': 'deep vein thrombosis',
            'pe': 'pulmonary embolism'
        }
        
        for abbrev, full_form in abbreviations.items():
            text = re.sub(r'\b' + abbrev + r'\b', full_form, text)
        
        return text
    
    def extract_diagnosis_entities(self, text: str) -> List[str]:
        """
        Extract medical entities from diagnosis text.
        
        Args:
            text (str): Diagnosis text
            
        Returns:
            List[str]: List of extracted medical entities
        """
        entities = self.ner.extract_entities(text, confidence_threshold=0.3)
        
        # Focus on disease and symptom entities
        relevant_entities = []
        for entity in entities:
            if entity['label'] in ['DISEASE', 'SYMPTOM', 'MEDICATION']:
                relevant_entities.append(entity['text'].lower())
        
        return relevant_entities
    
    def calculate_similarity_score(self, diagnosis_text: str, icd_code: str) -> float:
        """
        Calculate similarity score between diagnosis text and ICD code.
        
        Args:
            diagnosis_text (str): Preprocessed diagnosis text
            icd_code (str): ICD code
            
        Returns:
            float: Similarity score (0-1)
        """
        icd_info = self.icd_codes[icd_code]
        
        # Text-based similarity using TF-IDF
        diagnosis_vector = self.vectorizer.transform([diagnosis_text])
        icd_index = list(self.icd_codes.keys()).index(icd_code)
        icd_vector = self.icd_vectors[icd_index:icd_index+1]
        
        tfidf_similarity = cosine_similarity(diagnosis_vector, icd_vector)[0][0]
        
        # Keyword matching score
        keywords = [kw.lower() for kw in icd_info['keywords']]
        keyword_matches = sum(1 for kw in keywords if kw in diagnosis_text)
        keyword_score = keyword_matches / len(keywords) if keywords else 0
        
        # Entity matching score
        entities = self.extract_diagnosis_entities(diagnosis_text)
        entity_matches = 0
        for entity in entities:
            if any(entity in kw for kw in keywords) or any(kw in entity for kw in keywords):
                entity_matches += 1
        entity_score = entity_matches / max(len(entities), 1) if entities else 0
        
        # String similarity with description
        description_similarity = difflib.SequenceMatcher(
            None, 
            diagnosis_text, 
            icd_info['description'].lower()
        ).ratio()
        
        # Weighted combination of all scores
        final_score = (
            0.4 * tfidf_similarity +
            0.3 * keyword_score +
            0.2 * entity_score +
            0.1 * description_similarity
        )
        
        return min(final_score, 1.0)  # Cap at 1.0
    
    def recommend_icd_codes(self, diagnosis_text: str, top_k: int = 5) -> List[Dict]:
        """
        Recommend top K ICD codes for given diagnosis text.
        
        Args:
            diagnosis_text (str): Medical diagnosis text
            top_k (int): Number of recommendations to return
            
        Returns:
            List[Dict]: List of recommended ICD codes with scores
        """
        if not diagnosis_text.strip():
            return []
        
        # Preprocess the diagnosis text
        processed_text = self.preprocess_diagnosis_text(diagnosis_text)
        
        # Calculate scores for all ICD codes
        recommendations = []
        for icd_code in self.icd_codes:
            score = self.calculate_similarity_score(processed_text, icd_code)
            
            recommendations.append({
                'icd_code': icd_code,
                'description': self.icd_codes[icd_code]['description'],
                'category': self.icd_codes[icd_code]['category'],
                'confidence_score': round(score, 3),
                'matched_keywords': self._get_matched_keywords(processed_text, icd_code)
            })
        
        # Sort by confidence score and return top K
        recommendations.sort(key=lambda x: x['confidence_score'], reverse=True)
        return recommendations[:top_k]
    
    def _get_matched_keywords(self, diagnosis_text: str, icd_code: str) -> List[str]:
        """Get keywords that matched for this ICD code."""
        keywords = self.icd_codes[icd_code]['keywords']
        matched = []
        
        for keyword in keywords:
            if keyword.lower() in diagnosis_text:
                matched.append(keyword)
        
        return matched
    
    def get_code_details(self, icd_code: str) -> Optional[Dict]:
        """
        Get detailed information about a specific ICD code.
        
        Args:
            icd_code (str): ICD code
            
        Returns:
            Dict: Code details or None if not found
        """
        return self.icd_codes.get(icd_code)
    
    def search_by_keyword(self, keyword: str, max_results: int = 10) -> List[Dict]:
        """
        Search ICD codes by keyword.
        
        Args:
            keyword (str): Search keyword
            max_results (int): Maximum number of results
            
        Returns:
            List[Dict]: Matching ICD codes
        """
        keyword = keyword.lower()
        matches = []
        
        for code, info in self.icd_codes.items():
            # Check if keyword is in description or keywords
            if (keyword in info['description'].lower() or 
                any(keyword in kw.lower() for kw in info['keywords'])):
                
                matches.append({
                    'icd_code': code,
                    'description': info['description'],
                    'category': info['category'],
                    'keywords': info['keywords']
                })
        
        return matches[:max_results]
    
    def batch_recommend(self, diagnosis_texts: List[str], top_k: int = 5) -> List[List[Dict]]:
        """
        Get recommendations for multiple diagnosis texts.
        
        Args:
            diagnosis_texts (List[str]): List of diagnosis texts
            top_k (int): Number of recommendations per text
            
        Returns:
            List[List[Dict]]: Recommendations for each text
        """
        results = []
        for text in diagnosis_texts:
            recommendations = self.recommend_icd_codes(text, top_k)
            results.append(recommendations)
        
        return results
    
    def get_category_distribution(self, diagnosis_text: str) -> Dict[str, float]:
        """
        Get distribution of confidence across ICD categories.
        
        Args:
            diagnosis_text (str): Diagnosis text
            
        Returns:
            Dict[str, float]: Category confidence distribution
        """
        recommendations = self.recommend_icd_codes(diagnosis_text, top_k=len(self.icd_codes))
        
        category_scores = {}
        category_counts = {}
        
        for rec in recommendations:
            category = rec['category']
            score = rec['confidence_score']
            
            if category not in category_scores:
                category_scores[category] = 0
                category_counts[category] = 0
            
            category_scores[category] += score
            category_counts[category] += 1
        
        # Calculate average scores per category
        category_distribution = {}
        for category in category_scores:
            avg_score = category_scores[category] / category_counts[category]
            category_distribution[category] = round(avg_score, 3)
        
        return dict(sorted(category_distribution.items(), key=lambda x: x[1], reverse=True))


def main():
    """Example usage of the ICD Recommender."""
    
    # Sample diagnosis texts
    sample_diagnoses = [
        "Patient presents with chest pain and shortness of breath. History of coronary artery disease.",
        "Type 2 diabetes mellitus with poor glycemic control. HbA1c elevated.",
        "Chronic cough with wheezing. History of asthma and smoking.",
        "Severe headaches with visual disturbances. Possible migraine.",
        "Patient reports persistent sadness and loss of interest in activities."
    ]
    
    print("ICD Code Recommendation System")
    print("=" * 50)
    
    recommender = ICDRecommender()
    
    for i, diagnosis in enumerate(sample_diagnoses, 1):
        print(f"\nDiagnosis {i}: {diagnosis}")
        print("-" * 60)
        
        recommendations = recommender.recommend_icd_codes(diagnosis)
        
        for j, rec in enumerate(recommendations, 1):
            print(f"{j}. {rec['icd_code']} - {rec['description']}")
            print(f"   Category: {rec['category']}")
            print(f"   Confidence: {rec['confidence_score']}")
            if rec['matched_keywords']:
                print(f"   Matched Keywords: {', '.join(rec['matched_keywords'])}")
            print()
        
        # Show category distribution
        print("Category Distribution:")
        distribution = recommender.get_category_distribution(diagnosis)
        for category, score in distribution.items():
            print(f"  {category}: {score}")
        print()


if __name__ == "__main__":
    main()