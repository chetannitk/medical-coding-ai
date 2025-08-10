"""
Unit tests for the ICD Code Recommender utility.
"""

import unittest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from medical_coding.utils.icd_recommender import ICDRecommender
from medical_coding.utils.clinical_ner import ClinicalNER


class TestICDRecommender(unittest.TestCase):
    """Test cases for ICD Code Recommender functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.recommender = ICDRecommender()
        self.sample_diagnosis = "Patient presents with chest pain and shortness of breath. History of diabetes."
        self.diabetes_text = "Type 2 diabetes mellitus with poor glycemic control"
        self.heart_attack_text = "Acute myocardial infarction with ST elevation"
    
    def test_initialization(self):
        """Test recommender initialization."""
        self.assertIsNotNone(self.recommender)
        self.assertIsNotNone(self.recommender.icd_codes)
        self.assertIsNotNone(self.recommender.vectorizer)
        self.assertIsInstance(self.recommender.ner, ClinicalNER)
        self.assertGreater(len(self.recommender.icd_codes), 0)
    
    def test_preprocess_diagnosis_text(self):
        """Test diagnosis text preprocessing."""
        messy_text = "  Patient has   HTN and  DM  with   CAD  "
        processed = self.recommender.preprocess_diagnosis_text(messy_text)
        
        # Should be lowercase and cleaned
        self.assertEqual(processed.lower(), processed)
        self.assertNotIn("  ", processed)  # No double spaces
        
        # Should expand abbreviations
        self.assertIn("hypertension", processed)
        self.assertIn("diabetes mellitus", processed)
        self.assertIn("coronary artery disease", processed)
    
    def test_extract_diagnosis_entities(self):
        """Test medical entity extraction from diagnosis."""
        entities = self.recommender.extract_diagnosis_entities(self.sample_diagnosis)
        self.assertIsInstance(entities, list)
        
        # Should extract some medical terms
        entity_text = " ".join(entities).lower()
        self.assertTrue(any(term in entity_text for term in ["chest", "pain", "diabetes", "breath"]))
    
    def test_recommend_icd_codes_basic(self):
        """Test basic ICD code recommendations."""
        recommendations = self.recommender.recommend_icd_codes(self.diabetes_text, top_k=5)
        
        self.assertIsInstance(recommendations, list)
        self.assertLessEqual(len(recommendations), 5)
        self.assertGreater(len(recommendations), 0)
        
        # Check structure of recommendations
        for rec in recommendations:
            self.assertIn('icd_code', rec)
            self.assertIn('description', rec)
            self.assertIn('category', rec)
            self.assertIn('confidence_score', rec)
            self.assertIn('matched_keywords', rec)
            
            # Validate score range
            self.assertGreaterEqual(rec['confidence_score'], 0.0)
            self.assertLessEqual(rec['confidence_score'], 1.0)
    
    def test_recommend_icd_codes_diabetes(self):
        """Test specific diabetes diagnosis recommendations."""
        recommendations = self.recommender.recommend_icd_codes(self.diabetes_text, top_k=3)
        
        # Should have at least one recommendation
        self.assertGreater(len(recommendations), 0)
        
        # Top recommendation should be diabetes-related
        top_rec = recommendations[0]
        self.assertTrue(
            "diabetes" in top_rec['description'].lower() or
            any("diabetes" in kw.lower() for kw in top_rec['matched_keywords'])
        )
    
    def test_recommend_icd_codes_heart_attack(self):
        """Test heart attack diagnosis recommendations."""
        recommendations = self.recommender.recommend_icd_codes(self.heart_attack_text, top_k=3)
        
        self.assertGreater(len(recommendations), 0)
        
        # Should find cardiovascular codes
        categories = [rec['category'] for rec in recommendations]
        self.assertIn('Cardiovascular', categories)
        
        # Top recommendation should be heart-related
        top_rec = recommendations[0]
        description_and_keywords = (top_rec['description'] + " " + " ".join(top_rec['matched_keywords'])).lower()
        self.assertTrue(any(term in description_and_keywords for term in ["myocardial", "infarction", "heart", "cardiac"]))
    
    def test_recommend_empty_text(self):
        """Test recommendations with empty text."""
        recommendations = self.recommender.recommend_icd_codes("", top_k=5)
        self.assertEqual(len(recommendations), 0)
        
        recommendations = self.recommender.recommend_icd_codes("   ", top_k=5)
        self.assertEqual(len(recommendations), 0)
    
    def test_calculate_similarity_score(self):
        """Test similarity score calculation."""
        # Test with a known ICD code
        icd_codes = list(self.recommender.icd_codes.keys())
        if icd_codes:
            test_code = icd_codes[0]
            score = self.recommender.calculate_similarity_score(self.diabetes_text, test_code)
            
            self.assertIsInstance(score, float)
            self.assertGreaterEqual(score, 0.0)
            self.assertLessEqual(score, 1.0)
    
    def test_get_matched_keywords(self):
        """Test keyword matching functionality."""
        # Test with diabetes text against a diabetes code
        diabetes_codes = [code for code, info in self.recommender.icd_codes.items() 
                         if 'diabetes' in info['description'].lower()]
        
        if diabetes_codes:
            matched = self.recommender._get_matched_keywords(self.diabetes_text, diabetes_codes[0])
            self.assertIsInstance(matched, list)
            # Should find some diabetes-related keywords
            matched_text = " ".join(matched).lower()
            self.assertTrue("diabetes" in matched_text or len(matched) > 0)
    
    def test_get_code_details(self):
        """Test retrieving code details."""
        # Test with a known code
        known_codes = list(self.recommender.icd_codes.keys())
        if known_codes:
            test_code = known_codes[0]
            details = self.recommender.get_code_details(test_code)
            
            self.assertIsNotNone(details)
            self.assertIn('description', details)
            self.assertIn('keywords', details)
            self.assertIn('category', details)
        
        # Test with non-existent code
        details = self.recommender.get_code_details("FAKE.CODE")
        self.assertIsNone(details)
    
    def test_search_by_keyword(self):
        """Test keyword search functionality."""
        # Search for diabetes
        results = self.recommender.search_by_keyword("diabetes", max_results=5)
        self.assertIsInstance(results, list)
        self.assertLessEqual(len(results), 5)
        
        # Results should contain diabetes-related codes
        for result in results:
            self.assertIn('icd_code', result)
            self.assertIn('description', result)
            text_to_search = result['description'].lower() + " " + " ".join(result['keywords']).lower()
            self.assertIn('diabetes', text_to_search)
        
        # Search for non-existent term
        results = self.recommender.search_by_keyword("nonexistentdisease", max_results=5)
        self.assertEqual(len(results), 0)
    
    def test_batch_recommend(self):
        """Test batch processing of multiple diagnoses."""
        diagnosis_list = [
            self.diabetes_text,
            self.heart_attack_text,
            "Patient has hypertension and headache"
        ]
        
        batch_results = self.recommender.batch_recommend(diagnosis_list, top_k=3)
        
        self.assertIsInstance(batch_results, list)
        self.assertEqual(len(batch_results), len(diagnosis_list))
        
        # Each result should be a list of recommendations
        for result in batch_results:
            self.assertIsInstance(result, list)
            self.assertLessEqual(len(result), 3)
    
    def test_get_category_distribution(self):
        """Test category distribution calculation."""
        distribution = self.recommender.get_category_distribution(self.sample_diagnosis)
        
        self.assertIsInstance(distribution, dict)
        
        # Should have some categories
        self.assertGreater(len(distribution), 0)
        
        # All values should be floats between 0 and 1
        for category, score in distribution.items():
            self.assertIsInstance(score, float)
            self.assertGreaterEqual(score, 0.0)
            self.assertLessEqual(score, 1.0)
        
        # Should be sorted by score (highest first)
        scores = list(distribution.values())
        self.assertEqual(scores, sorted(scores, reverse=True))
    
    def test_confidence_score_ordering(self):
        """Test that recommendations are ordered by confidence score."""
        recommendations = self.recommender.recommend_icd_codes(self.diabetes_text, top_k=5)
        
        if len(recommendations) > 1:
            # Scores should be in descending order
            scores = [rec['confidence_score'] for rec in recommendations]
            self.assertEqual(scores, sorted(scores, reverse=True))
    
    def test_top_k_parameter(self):
        """Test that top_k parameter works correctly."""
        # Test different values of top_k
        for k in [1, 3, 5, 10]:
            recommendations = self.recommender.recommend_icd_codes(self.diabetes_text, top_k=k)
            self.assertLessEqual(len(recommendations), k)
            self.assertLessEqual(len(recommendations), len(self.recommender.icd_codes))


class TestICDRecommenderEdgeCases(unittest.TestCase):
    """Test edge cases for ICD Recommender."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.recommender = ICDRecommender()
    
    def test_very_long_diagnosis(self):
        """Test with very long diagnosis text."""
        long_diagnosis = "Patient presents with chest pain. " * 100
        recommendations = self.recommender.recommend_icd_codes(long_diagnosis, top_k=3)
        self.assertIsInstance(recommendations, list)
    
    def test_special_characters(self):
        """Test with special characters in diagnosis."""
        special_diagnosis = "Patient has Type-2 DM & HTN!!! BP: 160/95 mmHg."
        recommendations = self.recommender.recommend_icd_codes(special_diagnosis, top_k=3)
        self.assertIsInstance(recommendations, list)
    
    def test_medical_abbreviations(self):
        """Test handling of medical abbreviations."""
        abbrev_diagnosis = "Pt w/ CAD, CHF, HTN, DM, COPD, GERD"
        recommendations = self.recommender.recommend_icd_codes(abbrev_diagnosis, top_k=5)
        
        self.assertIsInstance(recommendations, list)
        self.assertGreater(len(recommendations), 0)
        
        # Should find multiple relevant conditions
        categories = set(rec['category'] for rec in recommendations)
        self.assertGreaterEqual(len(categories), 2)  # Should span multiple categories
    
    def test_numeric_values(self):
        """Test diagnosis with numeric values."""
        numeric_diagnosis = "HbA1c 9.2%, BP 180/95, HR 110, glucose 250 mg/dL"
        recommendations = self.recommender.recommend_icd_codes(numeric_diagnosis, top_k=3)
        self.assertIsInstance(recommendations, list)
    
    def test_mixed_case_diagnosis(self):
        """Test with mixed case diagnosis text."""
        mixed_case = "PATIENT HAS Diabetes And HYPERTENSION with Chest Pain"
        recommendations = self.recommender.recommend_icd_codes(mixed_case, top_k=3)
        self.assertIsInstance(recommendations, list)
        self.assertGreater(len(recommendations), 0)


if __name__ == '__main__':
    # Add verbose output for better test reporting
    unittest.main(verbosity=2)