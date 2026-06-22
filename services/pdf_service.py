"""
Service for extracting text from PDF and TXT files.
"""
from pathlib import Path
from typing import Tuple
import PyPDF2


class DocumentExtractor:
    """Handles extraction of text from PDF and TXT files."""
    
    @staticmethod
    def extract_from_pdf(file_path: str) -> str:
        """
        Extract text from a PDF file.
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            Extracted text from the PDF
            
        Raises:
            ValueError: If PDF cannot be read
        """
        try:
            text = ""
            with open(file_path, 'rb') as pdf_file:
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                
                if len(pdf_reader.pages) == 0:
                    raise ValueError("PDF file contains no pages")
                
                for page in pdf_reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            
            if not text.strip():
                raise ValueError("No text could be extracted from the PDF")
            
            return text.strip()
        
        except Exception as e:
            raise ValueError(f"Error extracting text from PDF: {str(e)}")
    
    @staticmethod
    def extract_from_txt(file_path: str) -> str:
        """
        Extract text from a TXT file.
        
        Args:
            file_path: Path to the TXT file
            
        Returns:
            Extracted text from the TXT file
            
        Raises:
            ValueError: If TXT cannot be read
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as txt_file:
                text = txt_file.read()
            
            if not text.strip():
                raise ValueError("TXT file is empty")
            
            return text.strip()
        
        except Exception as e:
            raise ValueError(f"Error extracting text from TXT: {str(e)}")
    
    @staticmethod
    def extract_text(file_path: str, file_type: str) -> str:
        """
        Extract text from a file based on its type.
        
        Args:
            file_path: Path to the file
            file_type: Type of the file ('pdf' or 'txt')
            
        Returns:
            Extracted text
            
        Raises:
            ValueError: If file type is not supported
        """
        if file_type.lower() == 'pdf':
            return DocumentExtractor.extract_from_pdf(file_path)
        elif file_type.lower() == 'txt':
            return DocumentExtractor.extract_from_txt(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")
    
    @staticmethod
    def get_text_preview(text: str, max_length: int = 500) -> str:
        """
        Get a preview of the extracted text.
        
        Args:
            text: Full text
            max_length: Maximum length of preview
            
        Returns:
            Preview text
        """
        if len(text) <= max_length:
            return text
        
        return text[:max_length] + "..."
    
    @staticmethod
    def get_file_size(file_path: str) -> int:
        """
        Get the size of a file in bytes.
        
        Args:
            file_path: Path to the file
            
        Returns:
            File size in bytes
        """
        return Path(file_path).stat().st_size
