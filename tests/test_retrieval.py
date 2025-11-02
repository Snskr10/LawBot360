import unittest
from app import create_app
from models.db import db, User
from services.retrieval import KnowledgeRetrieval
import tempfile
import shutil
from pathlib import Path

class RetrievalTestCase(unittest.TestCase):
    """Test cases for knowledge retrieval service"""
    
    def setUp(self):
        """Set up test environment"""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.temp_dir = tempfile.mkdtemp()
        
        with self.app.app_context():
            # Set up temp vector store
            self.original_path = self.app.config['VECTOR_DB_PATH']
            self.app.config['VECTOR_DB_PATH'] = Path(self.temp_dir) / 'vector_store'
    
    def tearDown(self):
        """Clean up"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_retrieval_initialization(self):
        """Test that retrieval service initializes correctly"""
        with self.app.app_context():
            retrieval = KnowledgeRetrieval(force_reindex=False)
            self.assertIsNotNone(retrieval.collection)
    
    def test_search_functionality(self):
        """Test search functionality"""
        with self.app.app_context():
            retrieval = KnowledgeRetrieval(force_reindex=False)
            results = retrieval.search('contract formation', jurisdiction='IN', limit=5)
            self.assertIsInstance(results, list)
            # Should have results if vector store is populated
            if len(results) > 0:
                self.assertIn('text', results[0])
                self.assertIn('section_code', results[0])

if __name__ == '__main__':
    unittest.main()

