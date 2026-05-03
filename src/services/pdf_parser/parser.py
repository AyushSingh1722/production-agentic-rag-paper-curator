import asyncio
import logging
from pathlib import Path
from typing import Optional

import pypdfium2 as pdfium
from src.exceptions import PDFParsingException, PDFValidationError
from src.schemas.pdf_parser.models import PaperSection, ParserType, PdfContent

from .docling import DoclingParser

logger = logging.getLogger(__name__)


class PDFParserService:
    """Main PDF parsing service using Docling only."""

    def __init__(self, max_pages: int, max_file_size_mb: int, do_ocr: bool = False, do_table_structure: bool = True):
        """Initialize PDF parser service with configurable limits."""
        self.docling_parser = DoclingParser(
            max_pages=max_pages, max_file_size_mb=max_file_size_mb, do_ocr=do_ocr, do_table_structure=do_table_structure
        )
        self.max_pages = max_pages

    def _parse_with_pdfium(self, pdf_path: Path) -> Optional[PdfContent]:
        """Fallback parser that extracts plain text with pypdfium2 when Docling rejects a PDF."""
        pdf_doc = pdfium.PdfDocument(str(pdf_path))
        actual_pages = len(pdf_doc)
        processed_pages = min(actual_pages, self.max_pages)

        page_texts = []
        sections = []

        try:
            for page_index in range(processed_pages):
                page = pdf_doc[page_index]
                textpage = page.get_textpage()
                page_text = textpage.get_text_bounded().strip()

                if page_text:
                    page_texts.append(page_text)
                    sections.append(PaperSection(title=f"Page {page_index + 1}", content=page_text))

                textpage.close()
                page.close()
        finally:
            pdf_doc.close()

        raw_text = "\n\n".join(page_texts).strip()
        if not raw_text:
            return None

        return PdfContent(
            sections=sections,
            figures=[],
            tables=[],
            raw_text=raw_text,
            references=[],
            parser_used=ParserType.PDFIUM,
            metadata={
                "source": "pypdfium2",
                "fallback": True,
                "actual_pages": actual_pages,
                "processed_pages": processed_pages,
                "truncated": actual_pages > self.max_pages,
            },
        )

    async def parse_pdf(self, pdf_path: Path) -> Optional[PdfContent]:
        """Parse PDF using Docling parser only.

        :param pdf_path: Path to PDF file
        :returns: PdfContent object or None if parsing failed
        """
        if not pdf_path.exists():
            logger.error(f"PDF file not found: {pdf_path}")
            raise PDFValidationError(f"PDF file not found: {pdf_path}")

        try:
            # Docling parsing is synchronous and can block for large PDFs, so run it in a worker thread.
            result = await asyncio.to_thread(self.docling_parser.parse_pdf, pdf_path)
            if result:
                logger.info(f"Parsed {pdf_path.name}")
                return result
            else:
                logger.warning(f"Docling parsing skipped or returned no result for {pdf_path.name}")
                return None

        except PDFValidationError:
            raise
        except PDFParsingException as e:
            logger.warning(f"Docling failed for {pdf_path.name}; falling back to pypdfium2 text extraction: {e}")
            fallback_result = await asyncio.to_thread(self._parse_with_pdfium, pdf_path)
            if fallback_result:
                logger.info(f"Parsed {pdf_path.name} with pypdfium2 fallback")
                return fallback_result
            raise
        except Exception as e:
            logger.error(f"Docling parsing error for {pdf_path.name}: {e}")
            raise PDFParsingException(f"Docling parsing error for {pdf_path.name}: {e}")
