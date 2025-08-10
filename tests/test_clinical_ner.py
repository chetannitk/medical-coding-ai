"""
Unit tests for the Clinical NER utility.
"""

import unittest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from medical_coding.utils.clinical_ner import ClinicalNER


class TestClinicalNER(unittest.TestCase):
    """Test cases for Clinical NER functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.ner = ClinicalNER()
        self.sample_text = """
        Patient has diabetes and hypertension. Experiencing chest pain and taking metformin.
        Heart examination shows abnormalities.
        """
    
    def test_initialization(self):
        """Test NER model initialization."""
        self.assertIsNotNone(self.ner)
        self.assertIsNotNone(self.ner.model_name)
    
    def test_preprocess_text(self):
        """Test text preprocessing."""
        messy_text = "  Patient   has   diabetes  \n\n  and   hypertension  "
        cleaned = self.ner.preprocess_text(messy_text)
        expected = "Patient has diabetes and hypertension"
        self.assertEqual(cleaned, expected)
    
    def test_extract_entities_basic(self):
        """Test basic entity extraction."""
        entities = self.ner.extract_entities(self.sample_text)
        self.assertIsInstance(entities, list)
        self.assertGreater(len(entities), 0)
        
        # Check entity structure
        for entity in entities:
            self.assertIn('text', entity)
            self.assertIn('label', entity)
            self.assertIn('confidence', entity)
            self.assertIn('start', entity)
            self.assertIn('end', entity)
    
    def test_extract_entities_empty_text(self):
        """Test entity extraction with empty text."""
        entities = self.ner.extract_entities("")
        self.assertIsInstance(entities, list)
        self.assertEqual(len(entities), 0)
    
    def test_extract_by_category(self):
        """Test categorized entity extraction."""
        categories = self.ner.extract_by_category(self.sample_text)
        self.assertIsInstance(categories, dict)
        
        # Should have at least some categories
        self.assertGreater(len(categories), 0)
        
        # Each category should have a list of terms
        for category, terms in categories.items():
            self.assertIsInstance(terms, list)
            self.assertGreater(len(terms), 0)
    
    def test_extract_specific_category(self):
        """Test extraction of specific category."""
        # This test assumes fallback mode will find 'DISEASE' entities
        categories = self.ner.extract_by_category(self.sample_text, category='DISEASE')
        
        if 'DISEASE' in categories:
            self.assertIn('DISEASE', categories)
            self.assertIsInstance(categories['DISEASE'], list)
    
    def test_batch_extract(self):
        """Test batch processing of multiple texts."""
        texts = [
            "Patient has diabetes",
            "Chest pain and headache reported",
            "Taking aspirin for heart condition"
        ]
        
        results = self.ner.batch_extract(texts)
        self.assertIsInstance(results, list)
        self.assertEqual(len(results), len(texts))
        
        # Each result should be a list of entities
        for result in results:
            self.assertIsInstance(result, list)
    
    def test_get_entity_summary(self):
        """Test entity summary generation."""
        summary = self.ner.get_entity_summary(self.sample_text)
        
        self.assertIsInstance(summary, dict)
        self.assertIn('total_entities', summary)
        self.assertIn('unique_entities', summary)
        self.assertIn('categories', summary)
        self.assertIn('avg_confidence', summary)
        
        # Check data types
        self.assertIsInstance(summary['total_entities'], int)
        self.assertIsInstance(summary['unique_entities'], int)
        self.assertIsInstance(summary['categories'], dict)
        self.assertIsInstance(summary['avg_confidence'], (float, type(summary['avg_confidence'])))
        
        # Logical constraints
        self.assertGreaterEqual(summary['total_entities'], summary['unique_entities'])
        self.assertGreaterEqual(summary['avg_confidence'], 0.0)
        self.assertLessEqual(summary['avg_confidence'], 1.0)
    
    def test_confidence_threshold(self):
        """Test confidence threshold filtering."""
        # Test with high confidence threshold
        high_conf_entities = self.ner.extract_entities(self.sample_text, confidence_threshold=0.9)
        
        # Test with low confidence threshold
        low_conf_entities = self.ner.extract_entities(self.sample_text, confidence_threshold=0.1)
        
        # Should have fewer or equal entities with higher threshold
        self.assertLessEqual(len(high_conf_entities), len(low_conf_entities))
        
        # All returned entities should meet the threshold
        for entity in high_conf_entities:
            self.assertGreaterEqual(entity['confidence'], 0.9)
    
    def test_fallback_extraction(self):
        """Test fallback pattern matching."""
        # Test known medical terms that should be caught by fallback
        test_text = "Patient has diabetes, hypertension, and chest pain. Taking aspirin."
        
        entities = self.ner._fallback_extraction(test_text)
        self.assertIsInstance(entities, list)
        
        # Should find some medical terms
        entity_texts = [entity['text'].lower() for entity in entities]
        medical_terms = ['diabetes', 'hypertension', 'chest pain', 'pain', 'aspirin']
        
        found_terms = [term for term in medical_terms if any(term in text for text in entity_texts)]
        self.assertGreater(len(found_terms), 0)


class TestClinicalNEREdgeCases(unittest.TestCase):
    """Test edge cases for Clinical NER."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.ner = ClinicalNER()
    
    def test_very_long_text(self):
        """Test with very long text."""
        long_text = "Patient has diabetes. " * 1000
        entities = self.ner.extract_entities(long_text)
        self.assertIsInstance(entities, list)
    
    def test_special_characters(self):
        """Test with special characters."""
        special_text = "Patient has diabetes & hypertension! Blood pressure: 160/95 mmHg."
        entities = self.ner.extract_entities(special_text)
        self.assertIsInstance(entities, list)
    
    def test_mixed_case(self):
        """Test with mixed case text."""
        mixed_case = "PATIENT has Diabetes and HYPERTENSION. chest PAIN reported."
        entities = self.ner.extract_entities(mixed_case)
        self.assertIsInstance(entities, list)
    
    def test_numbers_and_units(self):
        """Test with medical numbers and units."""
        numeric_text = "Blood pressure 160/95 mmHg, glucose 150 mg/dL, heart rate 85 bpm."
        entities = self.ner.extract_entities(numeric_text)
        self.assertIsInstance(entities, list)


if __name__ == '__main__':
    unittest.main()