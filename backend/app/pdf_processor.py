import os
import re
import logging
from typing import List, Dict, Any
import pypdf
import pdfplumber

logger = logging.getLogger("pdf_processor")

class PDFProcessor:
    @staticmethod
    def extract_document_pages(file_path: str) -> List[Dict[str, Any]]:
        pages_data = []
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"PDF file not found at {file_path}")
            
        filename = os.path.basename(file_path)
        
        try:
            with pdfplumber.open(file_path) as pdf:
                for idx, page in enumerate(pdf.pages):
                    page_num = idx + 1
                    raw_text = page.extract_text() or ""
                    
                    tables = []
                    try:
                        extracted_tables = page.extract_tables()
                        for tbl in extracted_tables:
                            if tbl and len(tbl) > 1:
                                tables.append(tbl)
                    except Exception as te:
                        logger.warning(f"Table extraction error on page {page_num}: {te}")
                    
                    cleaned = PDFProcessor._clean_text(raw_text)
                    headings = PDFProcessor._find_section_headings(raw_text)
                    
                    pages_data.append({
                        "page_number": page_num,
                        "text": raw_text,
                        "cleaned_text": cleaned,
                        "tables": tables,
                        "headings": headings,
                        "doc_name": filename
                    })
        except Exception as e:
            logger.warning(f"pdfplumber extraction failed for {file_path}: {e}. Falling back to pypdf.")
            reader = pypdf.PdfReader(file_path)
            for idx, page in enumerate(reader.pages):
                page_num = idx + 1
                raw_text = page.extract_text() or ""
                cleaned = PDFProcessor._clean_text(raw_text)
                pages_data.append({
                    "page_number": page_num,
                    "text": raw_text,
                    "cleaned_text": cleaned,
                    "tables": [],
                    "headings": [],
                    "doc_name": filename
                })
                
        return pages_data
        
    @staticmethod
    def _clean_text(text: str) -> str:
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
        
    @staticmethod
    def _find_section_headings(text: str) -> List[str]:
        headings = []
        lines = text.split('\n')
        for line in lines[:10]:
            line_str = line.strip()
            if re.match(r'^(CHAPTER|SECTION|\d+\.\d+|\b[A-Z\s]{4,}\b)', line_str) and len(line_str) < 80:
                headings.append(line_str)
        return headings
