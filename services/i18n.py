from typing import Dict, Any
import json
from pathlib import Path

class I18nService:
    """Internationalization service for EN/HI"""
    
    def __init__(self):
        self.translations = {
            'en': {
                'create_contract': 'Create Contract',
                'verify_document': 'Verify Document',
                'explain_law': 'Explain Law',
                'dashboard': 'Dashboard',
                'templates': 'Templates',
                'settings': 'Settings'
            },
            'hi': {
                'create_contract': 'अनुबंध बनाएं',
                'verify_document': 'दस्तावेज़ सत्यापित करें',
                'explain_law': 'कानून समझाएं',
                'dashboard': 'डैशबोर्ड',
                'templates': 'टेम्प्लेट',
                'settings': 'सेटिंग्स'
            }
        }
    
    def translate(self, key: str, language: str = 'en') -> str:
        """Translate a key to the specified language"""
        return self.translations.get(language, self.translations['en']).get(key, key)
    
    def get_translations(self, language: str = 'en') -> Dict[str, str]:
        """Get all translations for a language"""
        return self.translations.get(language, self.translations['en'])


