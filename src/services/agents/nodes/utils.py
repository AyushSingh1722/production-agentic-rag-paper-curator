import ast
import logging
import re
from typing import Dict, List, Optional

from langchain_core.messages import AIMessage, HumanMessage, ToolMessage

from ..models import ReasoningStep, SourceItem, ToolArtefact

logger = logging.getLogger(__name__)

ARXIV_PDF_URL_RE = re.compile(r"https://arxiv\.org/pdf/([0-9]+\.[0-9]+(?:v\d+)?)\.pdf")
ARXIV_ID_RE = re.compile(r"\b([0-9]{4}\.[0-9]{4,5}(?:v\d+)?)\b")


def normalize_arxiv_id(arxiv_id: str) -> str:
    """Return versionless arXiv ID for canonical source URLs."""
    return arxiv_id.split("v")[0] if "v" in arxiv_id else arxiv_id


def canonical_arxiv_pdf_url(arxiv_id: str) -> str:
    """Build a canonical versionless arXiv PDF URL."""
    return f"https://arxiv.org/pdf/{normalize_arxiv_id(arxiv_id)}.pdf"


def _source_item_from_metadata(metadata: Dict) -> Optional[SourceItem]:
    """Build a SourceItem from document metadata if possible."""
    arxiv_id = metadata.get("arxiv_id")
    if not arxiv_id:
        return None
    url = canonical_arxiv_pdf_url(arxiv_id)

    authors = metadata.get("authors", [])
    if isinstance(authors, str):
        authors = [author.strip() for author in authors.split(",") if author.strip()]

    return SourceItem(
        arxiv_id=arxiv_id,
        title=metadata.get("title", arxiv_id),
        authors=authors,
        url=url,
        relevance_score=float(metadata.get("score", metadata.get("relevance_score", 0.0)) or 0.0),
    )


def _extract_source_items_from_string(content: str) -> List[SourceItem]:
    """Best-effort extraction of arXiv sources from tool message content."""
    items: List[SourceItem] = []
    seen_urls = set()

    try:
        parsed = ast.literal_eval(content)
    except Exception:
        parsed = None

    if isinstance(parsed, list):
        for entry in parsed:
            metadata = getattr(entry, "metadata", None)
            if metadata is None and isinstance(entry, dict):
                metadata = entry.get("metadata")
            if isinstance(metadata, dict):
                source_item = _source_item_from_metadata(metadata)
                if source_item and source_item.url not in seen_urls:
                    items.append(source_item)
                    seen_urls.add(source_item.url)

    for match in ARXIV_PDF_URL_RE.finditer(content):
        arxiv_id = match.group(1)
        url = canonical_arxiv_pdf_url(arxiv_id)
        if url not in seen_urls:
            items.append(
                SourceItem(
                    arxiv_id=arxiv_id,
                    title=arxiv_id,
                    authors=[],
                    url=url,
                    relevance_score=0.0,
                )
            )
            seen_urls.add(url)

    if not items:
        for match in ARXIV_ID_RE.finditer(content):
            arxiv_id = match.group(1)
            url = canonical_arxiv_pdf_url(arxiv_id)
            if url not in seen_urls:
                items.append(
                    SourceItem(
                        arxiv_id=arxiv_id,
                        title=arxiv_id,
                        authors=[],
                        url=url,
                        relevance_score=0.0,
                    )
                )
                seen_urls.add(url)

    return items


def count_retrieved_documents_from_tool_messages(messages: List) -> int:
    """Count retrieved documents/chunks represented in tool messages."""
    max_count = 0

    for msg in messages:
        if isinstance(msg, ToolMessage) and getattr(msg, "name", None) == "retrieve_papers":
            artifact = getattr(msg, "artifact", None)
            if isinstance(artifact, list):
                max_count = max(max_count, len(artifact))
                continue

            content = getattr(msg, "content", "")
            if isinstance(content, str):
                try:
                    parsed = ast.literal_eval(content)
                except Exception:
                    parsed = None
                if isinstance(parsed, list):
                    max_count = max(max_count, len(parsed))
                    continue

                document_matches = len(re.findall(r"Document\(", content))
                if document_matches:
                    max_count = max(max_count, document_matches)
                    continue

                metadata_matches = len(re.findall(r"'arxiv_id':\s*'[^']+'", content))
                if metadata_matches:
                    max_count = max(max_count, metadata_matches)

    return max_count


def extract_sources_from_tool_messages(messages: List) -> List[SourceItem]:
    """Extract sources from tool messages in conversation.

    :param messages: List of messages from graph state
    :returns: List of SourceItem objects
    """
    sources = []
    seen_urls = set()

    for msg in messages:
        if isinstance(msg, ToolMessage) and hasattr(msg, "name"):
            if msg.name == "retrieve_papers":
                artifact = getattr(msg, "artifact", None)
                if isinstance(artifact, list):
                    for item in artifact:
                        metadata = getattr(item, "metadata", None)
                        if metadata is None and isinstance(item, dict):
                            metadata = item.get("metadata")
                        if isinstance(metadata, dict):
                            source_item = _source_item_from_metadata(metadata)
                            if source_item and source_item.url not in seen_urls:
                                sources.append(source_item)
                                seen_urls.add(source_item.url)

                content = getattr(msg, "content", "")
                if isinstance(content, str):
                    for source_item in _extract_source_items_from_string(content):
                        if source_item.url not in seen_urls:
                            sources.append(source_item)
                            seen_urls.add(source_item.url)

    return sources


def extract_tool_artefacts(messages: List) -> List[ToolArtefact]:
    """Extract tool artifacts from messages.

    :param messages: List of messages from graph state
    :returns: List of ToolArtefact objects
    """
    artefacts = []

    for msg in messages:
        if isinstance(msg, ToolMessage):
            artefact = ToolArtefact(
                tool_name=getattr(msg, "name", "unknown"),
                tool_call_id=getattr(msg, "tool_call_id", ""),
                content=msg.content,
                metadata={},
            )
            artefacts.append(artefact)

    return artefacts


def create_reasoning_step(
    step_name: str,
    description: str,
    metadata: Optional[Dict] = None,
) -> ReasoningStep:
    """Create a reasoning step record.

    :param step_name: Name of the step/node
    :param description: Human-readable description
    :param metadata: Additional metadata
    :returns: ReasoningStep object
    """
    return ReasoningStep(
        step_name=step_name,
        description=description,
        metadata=metadata or {},
    )


def filter_messages(messages: List) -> List[AIMessage | HumanMessage]:
    """Filter messages to include only HumanMessage and AIMessage types.

    Excludes tool messages and other internal message types.

    :param messages: List of messages to filter
    :returns: Filtered list of messages
    """
    return [msg for msg in messages if isinstance(msg, (HumanMessage, AIMessage))]


def get_latest_query(messages: List) -> str:
    """Get the latest user query from messages.

    :param messages: List of messages
    :returns: Latest query text
    :raises ValueError: If no user query found
    """
    for msg in reversed(messages):
        if isinstance(msg, HumanMessage):
            return msg.content

    raise ValueError("No user query found in messages")


def get_latest_context(messages: List) -> str:
    """Get the latest context from tool messages.

    :param messages: List of messages
    :returns: Latest context text or empty string
    """
    for msg in reversed(messages):
        if isinstance(msg, ToolMessage):
            return msg.content if hasattr(msg, "content") else ""

    return ""
