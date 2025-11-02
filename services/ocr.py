from typing import Dict, Any

# Optional imports - service will work without OCR dependencies
try:
    import pytesseract
    PYTESSERACT_AVAILABLE = True
except ImportError:
    PYTESSERACT_AVAILABLE = False

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

try:
    import fitz  # PyMuPDF
    PYMUPDF_AVAILABLE = True
except ImportError:
    PYMUPDF_AVAILABLE = False

try:
    import easyocr
    EASYOCR_AVAILABLE = True
except ImportError:
    EASYOCR_AVAILABLE = False

class OCRService:
    """OCR service for scanned documents"""
    
    def __init__(self):
        self.reader = None  # Lazy load easyocr
        self.use_easyocr = True
        self.available = PYTESSERACT_AVAILABLE or EASYOCR_AVAILABLE
    
    def extract_text(self, file_path: str, use_easyocr: bool = True) -> str:
        """Extract text using OCR"""
        if not self.available:
            return "OCR not available. Please install pytesseract or easyocr."
        
        if file_path.endswith('.pdf'):
            if not PYMUPDF_AVAILABLE:
                return "PyMuPDF not available for PDF OCR."
            return self._extract_from_pdf_ocr(file_path, use_easyocr)
        else:
            # Assume image file
            return self._extract_from_image(file_path, use_easyocr)
    
    def _extract_from_pdf_ocr(self, file_path: str, use_easyocr: bool) -> str:
        """Extract text from PDF using OCR"""
        try:
            if not PYMUPDF_AVAILABLE:
                return "PyMuPDF not available."
            
            doc = fitz.open(file_path)
            all_text = []
            
            for page_num in range(len(doc)):
                page = doc[page_num]
                
                # Convert page to image
                pix = page.get_pixmap()
                img_data = pix.tobytes("png")
                
                # OCR the image
                if use_easyocr:
                    text = self._ocr_with_easyocr(img_data)
                else:
                    text = self._ocr_with_tesseract(img_data)
                
                all_text.append(text)
            
            doc.close()
            return '\n'.join(all_text)
        except Exception as e:
            return f"OCR error: {e}"
    
    def _extract_from_image(self, file_path: str, use_easyocr: bool) -> str:
        """Extract text from image file"""
        try:
            if use_easyocr:
                if not EASYOCR_AVAILABLE:
                    return "EasyOCR not available."
                return self._ocr_with_easyocr_file(file_path)
            else:
                if not PYTESSERACT_AVAILABLE or not PIL_AVAILABLE:
                    return "Tesseract or PIL not available."
                img = Image.open(file_path)
                return pytesseract.image_to_string(img)
        except Exception as e:
            return f"OCR error: {e}"
    
    def _ocr_with_easyocr(self, img_data: bytes) -> str:
        """OCR using EasyOCR"""
        try:
            if not EASYOCR_AVAILABLE or not PIL_AVAILABLE:
                return "EasyOCR or PIL not available."
            
            if self.reader is None:
                self.reader = easyocr.Reader(['en', 'hi'])  # English and Hindi
            
            # EasyOCR expects file path or numpy array
            # For in-memory, we'd need to convert bytes to PIL Image first
            import io
            import numpy as np
            img = Image.open(io.BytesIO(img_data))
            img_array = np.array(img)
            
            results = self.reader.readtext(img_array)
            return ' '.join([result[1] for result in results])
        except Exception as e:
            return f"EasyOCR error: {e}"
    
    def _ocr_with_easyocr_file(self, file_path: str) -> str:
        """OCR file using EasyOCR"""
        try:
            if not EASYOCR_AVAILABLE:
                return "EasyOCR not available."
            
            if self.reader is None:
                self.reader = easyocr.Reader(['en', 'hi'])
            
            results = self.reader.readtext(file_path)
            return ' '.join([result[1] for result in results])
        except Exception as e:
            return f"EasyOCR error: {e}"
    
    def _ocr_with_tesseract(self, img_data: bytes) -> str:
        """OCR using Tesseract"""
        try:
            if not PYTESSERACT_AVAILABLE or not PIL_AVAILABLE:
                return "Tesseract or PIL not available."
            
            import io
            img = Image.open(io.BytesIO(img_data))
            return pytesseract.image_to_string(img)
        except Exception as e:
            return f"Tesseract error: {e}"
    
    def extract_with_confidence(self, file_path: str) -> Dict[str, Any]:
        """Extract text with confidence scores"""
        # For MVP, return simple structure
        text = self.extract_text(file_path)
        return {
            'text': text,
            'confidence': 0.85,  # Placeholder
            'pages': [{'page_num': 1, 'text': text, 'confidence': 0.85}]
        }


