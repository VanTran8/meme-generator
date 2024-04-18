"""Module that define classes for ingesting differnt types of files."""
from QuoteEngine import QuoteModel
import pandas
from abc import ABC, abstractmethod
from typing import List
from docx import Document
import subprocess
import random

class IngestorInterface(ABC):
    """An abstract base class designed for parsing quotations stored in different file formats."""

    #supported_extensions = ['txt', 'csv', 'docx', 'pdf']
    supported_extensions = []

    @classmethod
    def can_ingest(cls, path) -> bool:
        """Check if the passed path has an extension in supported_extensions."""
        return path.split('.')[-1] in cls.supported_extensions

    @classmethod
    @abstractmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Abstract method for parsing each type of files."""
        pass

class CsvIngestor(IngestorInterface):
    """Imports quotes from csv files."""

    supported_extensions = ['csv']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Return a list of `QuoteModel` from parsing a csv file."""
        if not cls.can_ingest(path):
            raise Exception(f'Can not ingest {supported_extensions} files.')
        
        quotes = list()
        df = pandas.read_csv(path, header=0)
        for index, row in df.iterrows():
            quote = QuoteModel(row['body'], row['author'])
            quotes.append(quote)
        return quotes

class DocxIngestor(IngestorInterface):
    """Imports quotes from docx files."""

    supported_extensions = ['docx']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Return a list of `QuoteModel` from parsing docx file."""
        if not cls.can_ingest(path):
            raise Exception(f'Can not ingest {supported_extensions} files.')
        
        quotes = list()
        doc = Document(path)

        for paragraph in doc.paragraphs:
            if paragraph.text != "":
                body = paragraph.text.split('-')[0].strip().strip('"')
                author = paragraph.text.split('-')[1].strip()
                quote = QuoteModel(body, author)
                quotes.append(quote)

        return quotes

class PdfIngestor(IngestorInterface):
    """Imports quotes from pdf files using subprocess to launch pdftotext."""

    supported_extensions = ['pdf']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Return a list of `QuoteModel` from parsing pdf file with pdftotext binary."""
        if not cls.can_ingest(path):
            raise Exception(f'Can not ingest {supported_extensions} files.')
        
        quotes = list()
        result = subprocess.run(['pdftotext', path, '-'], stdout=subprocess.PIPE)
        if result.returncode:
            raise RuntimeError("Subprocess 'pdftotext' did not return successfully.")
        text_content = result.stdout.decode('utf-8')
        lines = text_content.splitlines()
        for line in lines:
            line = line.strip('\n\r').strip()
            if len(line) > 0:
                body = line.split('-')[0].strip().strip('"')
                author = line.split('-')[1].strip()
                quote = QuoteModel(body, author)
                quotes.append(quote)

        return quotes


class TxtIngestor(IngestorInterface):
    """Imports quotes from raw text(txt) files."""

    supported_extensions = ['txt']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Return a list of `QuoteModel` from parsing a txt file."""
        if not cls.can_ingest(path):
            raise Exception(f'Can not ingest {supported_extensions} files.')
            
        quotes = list()

        with open(path, 'r') as file:
            for line in file:
                body = line.split("-")[0].strip().strip('"')
                author = line.split("-")[1].strip()
                quote = QuoteModel(body, author)
                quotes.append(quote)

        return quotes
        
class Ingestor(IngestorInterface):
    """Encapsulates helper ingestor classes."""
    
    ingestors = [CsvIngestor, DocxIngestor, PdfIngestor, TxtIngestor]
    
    @classmethod
    def parse(cls, path) -> List[QuoteModel]:
        """Pasre files by appropriate ingestor."""
        for ingestor in cls.ingestors:
            if ingestor.can_ingest(path):
                return ingestor.parse(path)