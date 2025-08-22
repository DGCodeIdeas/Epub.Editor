from dataclasses import dataclass


@dataclass
class SearchResult:
    """Represents a single search result."""
    file_path: str
    line_number: int
    match_text: str
    context_before: str
    context_after: str
    item_href: str  # To identify the EPUB item
