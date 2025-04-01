"""Document manager for storing and retrieving processed documents."""

from __future__ import annotations

import logging

from docler.models import Document
from prettyqt import core


logger = logging.getLogger(__name__)


class DocumentManager(core.Object):
    """In-memory manager for converted documents."""

    document_added = core.Signal(str, Document)  # doc_id, document
    document_removed = core.Signal(str)  # doc_id

    __instance: DocumentManager | None = None

    def __init__(self):
        super().__init__()
        self.documents: dict[str, Document] = {}
        self.converter_info: dict[str, str] = {}  # doc_id -> converter name

    @classmethod
    def instance(cls) -> DocumentManager:
        """Return global DocumentManager singleton instance."""
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def add_document(self, doc_id: str, document: Document, converter: str) -> None:
        """Add a document to the manager."""
        self.documents[doc_id] = document
        self.converter_info[doc_id] = converter
        logger.info("Added document: %s", doc_id)
        self.document_added.emit(doc_id, document)

    def get_document(self, doc_id: str) -> Document | None:
        """Get a document by ID."""
        return self.documents.get(doc_id)

    def get_converter(self, doc_id: str) -> str | None:
        """Get the converter name used for a document."""
        return self.converter_info.get(doc_id)

    def list_documents(self) -> list[tuple[str, Document]]:
        """List all documents."""
        return list(self.documents.items())

    def remove_document(self, doc_id: str) -> bool:
        """Remove a document by ID."""
        if doc_id in self.documents:
            del self.documents[doc_id]
            if doc_id in self.converter_info:
                del self.converter_info[doc_id]
            self.document_removed.emit(doc_id)
            logger.info("Removed document: %s", doc_id)
            return True
        return False

    def clear(self) -> None:
        """Clear all documents."""
        doc_ids = list(self.documents.keys())
        self.documents.clear()
        self.converter_info.clear()
        for doc_id in doc_ids:
            self.document_removed.emit(doc_id)
        logger.info("Cleared all documents")
