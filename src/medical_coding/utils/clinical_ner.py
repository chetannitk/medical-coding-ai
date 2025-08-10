"""
Clinical Named Entity Recognition (NER) utility for extracting medical terms from text.
"""

import re
from typing import List, Dict, Tuple, Optional
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
import torch


class ClinicalNER:
    """
    A utility class for extracting clinical terms using Named Entity Recognition.
    """
    
    def __init__(self, model_name: str = "d4data/biomedical-ner-all"):
        """
        Initialize the Clinical NER model.
        
        Args:
            model_name (str): HuggingFace model name for biomedical NER
        """
        self.model_name = model_name
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self._load_model()
    
    def _load_model(self):
        """Load the NER model and tokenizer."""
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForTokenClassification.from_pretrained(self.model_name)
            self.nlp_pipeline = pipeline(
                "ner",
                model=self.model,
                tokenizer=self.tokenizer,
                aggregation_strategy="simple",
                device=0 if self.device == "cuda" else -1
            )
            print(f"Loaded model: {self.model_name}")
        except Exception as e:
            print(f"Error loading model: {e}")
            print("Falling back to basic pattern matching...")
            self.nlp_pipeline = None
    
    def preprocess_text(self, text: str) -> str:
        """
        Preprocess text for better NER performance.
        
        Args:
            text (str): Input text
            
        Returns:
            str: Preprocessed text
        """
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        return text
    
    def extract_entities(self, text: str, confidence_threshold: float = 0.5) -> List[Dict]:
        """
        Extract clinical entities from text.
        
        Args:
            text (str): Input text
            confidence_threshold (float): Minimum confidence score
            
        Returns:
            List[Dict]: List of extracted entities with metadata
        """
        preprocessed_text = self.preprocess_text(text)
        
        if self.nlp_pipeline is None:
            return self._fallback_extraction(preprocessed_text)
        
        try:
            entities = self.nlp_pipeline(preprocessed_text)
            
            filtered_entities = []
            for entity in entities:
                if entity['score'] >= confidence_threshold:
                    filtered_entities.append({
                        'text': entity['word'],
                        'label': entity['entity_group'],
                        'confidence': entity['score'],
                        'start': entity['start'],
                        'end': entity['end']
                    })
            
            return filtered_entities
            
        except Exception as e:
            print(f"Error during entity extraction: {e}")
            return self._fallback_extraction(preprocessed_text)
    
    def _fallback_extraction(self, text: str) -> List[Dict]:
        """
        Fallback method using pattern matching for common medical terms.
        
        Args:
            text (str): Input text
            
        Returns:
            List[Dict]: List of extracted entities
        """
        medical_patterns = {
            'DISEASE': r'\b(?:diabetes|hypertension|cancer|pneumonia|asthma|arthritis|migraine|depression|anxiety)\b',
            'SYMPTOM': r'\b(?:pain|fever|nausea|fatigue|headache|cough|shortness of breath|chest pain)\b',
            'MEDICATION': r'\b(?:aspirin|ibuprofen|acetaminophen|insulin|metformin|lisinopril|atorvastatin)\b',
            'ANATOMY': r'\b(?:heart|lung|liver|kidney|brain|stomach|chest|abdomen|head|neck)\b'
        }
        
        entities = []
        for label, pattern in medical_patterns.items():
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                entities.append({
                    'text': match.group(),
                    'label': label,
                    'confidence': 0.8,
                    'start': match.start(),
                    'end': match.end()
                })
        
        return entities
    
    def extract_by_category(self, text: str, category: str = None) -> Dict[str, List[str]]:
        """
        Extract entities grouped by category.
        
        Args:
            text (str): Input text
            category (str): Specific category to extract (optional)
            
        Returns:
            Dict[str, List[str]]: Entities grouped by category
        """
        entities = self.extract_entities(text)
        
        categorized = {}
        for entity in entities:
            label = entity['label']
            if category is None or label == category:
                if label not in categorized:
                    categorized[label] = []
                if entity['text'] not in categorized[label]:
                    categorized[label].append(entity['text'])
        
        return categorized
    
    def batch_extract(self, texts: List[str]) -> List[List[Dict]]:
        """
        Extract entities from multiple texts.
        
        Args:
            texts (List[str]): List of input texts
            
        Returns:
            List[List[Dict]]: List of entity lists for each text
        """
        results = []
        for text in texts:
            entities = self.extract_entities(text)
            results.append(entities)
        
        return results
    
    def get_entity_summary(self, text: str) -> Dict:
        """
        Get a summary of extracted entities.
        
        Args:
            text (str): Input text
            
        Returns:
            Dict: Summary statistics
        """
        entities = self.extract_entities(text)
        categories = self.extract_by_category(text)
        
        summary = {
            'total_entities': len(entities),
            'unique_entities': len(set(entity['text'].lower() for entity in entities)),
            'categories': {cat: len(terms) for cat, terms in categories.items()},
            'avg_confidence': sum(entity['confidence'] for entity in entities) / len(entities) if entities else 0
        }
        
        return summary


def main():
    """Example usage of the Clinical NER utility."""
    
    sample_text = """
    The patient presents with chest pain and shortness of breath. 
    History of diabetes and hypertension. Currently taking metformin and lisinopril.
    Examination reveals tenderness in the chest area. Recommend ECG and blood tests.
    Consider prescribing aspirin for cardiovascular protection.
    """
    
    ner = ClinicalNER()
    
    print("Clinical NER Extraction Results:")
    print("-" * 40)
    
    entities = ner.extract_entities(sample_text)
    for entity in entities:
        print(f"Entity: {entity['text']}")
        print(f"Category: {entity['label']}")
        print(f"Confidence: {entity['confidence']:.2f}")
        print("-" * 20)
    
    print("\nCategorized Results:")
    print("-" * 40)
    categories = ner.extract_by_category(sample_text)
    for category, terms in categories.items():
        print(f"{category}: {', '.join(terms)}")
    
    print("\nSummary:")
    print("-" * 40)
    summary = ner.get_entity_summary(sample_text)
    for key, value in summary.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()