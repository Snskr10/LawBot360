import os
from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv

# Load .env file from project root
BASE_DIR = Path(__file__).parent
env_path = BASE_DIR / '.env'
load_dotenv(dotenv_path=env_path)

# Flask Configuration
class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///lawbot360.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # File Storage
    UPLOAD_FOLDER = BASE_DIR / 'data' / 'uploads'
    EXPORT_FOLDER = BASE_DIR / 'data' / 'exports'
    MAX_UPLOAD_SIZE = int(os.getenv('MAX_UPLOAD_SIZE', '10485760'))  # 10MB
    
    # Vector Database
    VECTOR_DB_PATH = BASE_DIR / os.getenv('VECTOR_DB_PATH', 'data/vector_store')
    EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL', 'sentence-transformers/all-MiniLM-L6-v2')
    
    # OpenAI
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    
    # Jurisdiction
    DEFAULT_JURISDICTION = os.getenv('DEFAULT_JURISDICTION', 'IN')
    SUPPORTED_LANGUAGES = os.getenv('SUPPORTED_LANGUAGES', 'en,hi').split(',')
    DEFAULT_LANGUAGE = os.getenv('DEFAULT_LANGUAGE', 'en')
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE = int(os.getenv('RATE_LIMIT_PER_MINUTE', '30'))
    
    # JWT Configuration
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', SECRET_KEY)
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=7)
    
    # DocuSign (Optional)
    DOCUSIGN_INTEGRATION_KEY = os.getenv('DOCUSIGN_INTEGRATION_KEY', '')
    DOCUSIGN_USER_ID = os.getenv('DOCUSIGN_USER_ID', '')
    DOCUSIGN_ACCOUNT_ID = os.getenv('DOCUSIGN_ACCOUNT_ID', '')
    
    # Paths
    LAWS_DATA_PATH = BASE_DIR / 'data' / 'laws'
    TEMPLATES_DATA_PATH = BASE_DIR / 'data' / 'templates'


