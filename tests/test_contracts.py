import unittest
from app import create_app
from models.db import db, User, Contract
from routers.contracts import bp
import json

class ContractTestCase(unittest.TestCase):
    """Test cases for contract generation endpoints"""
    
    def setUp(self):
        """Set up test client and database"""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()
            # Create test user
            user = User(
                name='Test User',
                email='test@example.com',
                password_hash='hashed_password'
            )
            db.session.add(user)
            db.session.commit()
            self.user_id = user.id
    
    def tearDown(self):
        """Clean up after tests"""
        with self.app.app_context():
            db.drop_all()
    
    def test_generate_contract_basic(self):
        """Test basic contract generation"""
        response = self.client.post('/api/contracts/generate',
            json={
                'contract_type': 'NDA',
                'parties': ['Party A', 'Party B'],
                'terms': {
                    'consideration': 'Test consideration',
                    'scope': 'Test scope'
                },
                'jurisdiction': 'IN',
                'language': 'en'
            },
            content_type='application/json',
            headers={'X-User-Id': str(self.user_id)}
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('contract_id', data)
        self.assertIn('html', data)
    
    def test_generate_contract_invalid_data(self):
        """Test contract generation with invalid data"""
        response = self.client.post('/api/contracts/generate',
            json={
                'contract_type': '',
                'parties': []
            },
            content_type='application/json',
            headers={'X-User-Id': str(self.user_id)}
        )
        
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()

