# modules/loaders/pdf_loader.py

import os
import fitz  # PyMuPDF
from registry import ModuleRegistry

class PDFLoader:
    def __init__(self, path="sample_data/"):
        self.path = path

    def load(self):
        print(f"[PDFLoader] Loading PDFs from {self.path}")
        documents = []
        for filename in os.listdir(self.path):
            if filename.endswith(".pdf"):
                filepath = os.path.join(self.path, filename)
                text = self._extract_text_from_pdf(filepath)
                documents.append(text)
        return documents

    def _extract_text_from_pdf(self, filepath):
        doc = fitz.open(filepath)
        full_text = ""
        for page in doc:
            full_text += page.get_text()
        return full_text

# 起動時にレジストリ登録
ModuleRegistry.register("pdf_loader", PDFLoader)
