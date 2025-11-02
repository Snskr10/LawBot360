import unittest
from app import create_app
from models.db import db, User
from werkzeug.security import check_password_hash
import json

class AuthTestCase(unittest.TestCase):
    """Test cases for authentication endpoints"""
    
    def setUp(self):
        """Set up test client and database"""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()
    
    def tearDown(self):
        """Clean up after tests"""
        with self.app.app_context():
            db.drop_all()
    
    def test_register_user(self):
        """Test user registration"""
        response = self.client.post('/api/auth/register',
            json={
                'name': 'Test User',
                'email': 'test@example.com',
                'password': 'testpass123'
            },
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('access_token', data)
        self.assertIn('user', data)
        self.assertEqual(data['user']['email'], 'test@example.com')
    
    def test_register_duplicate_email(self):
        """Test registration with duplicate email"""
        # Register first user
        self.client.post('/api/auth/register',
            json={
                'name': 'Test User',
                'email': 'test@example.com',
                'password': 'testpass123'
            },
            content_type='application/json'
        )
        
        # Try to register again with same email
        response = self.client.post('/api/auth/register',
            json={
                'name': 'Another User',
                'email': 'test@example.com',
                'password': 'testpass123'
            },
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
    
    def test_login_success(self):
        """Test successful login"""
        # Register user first
        self.client.post('/api/auth/register',
            json={
                'name': 'Test User',
                'email': 'test@example.com',
                'password': 'testpass123'
            },
            content_type='application/json'
        )
        
        # Login
        response = self.client.post('/api/auth/login',
            json={
                'email': 'test@example.com',
                'password': 'testpass123'
            },
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('access_token', data)
        self.assertIn('user', data)
    
    def test_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        response = self.client.post('/api/auth/login',
            json={
                'email': 'wrong@example.com',
                'password': 'wrongpass'
            },
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 401)
    
    def test_get_current_user(self):
        """Test getting current user with valid token"""
        # Register and get token
        reg_response = self.client.post('/api/auth/register',
            json={
                'name': 'Test User',
                'email': 'test@example.com',
                'password': 'testpass123'
            },
            content_type='application/json'
        )
        token = json.loads(reg_response.data)['access_token']
        
        # Get current user
        response = self.client.get('/api/auth/me',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['email'], 'test@example.com')

if __name__ == '__main__':
    unittest.main()

