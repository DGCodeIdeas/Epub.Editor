from dataclasses import dataclass, field
from typing import List, Dict, Optional

@dataclass
class EpubMetadata:
    """
    Stores metadata from the EPUB's OPF file.
    """
    title: Optional[str] = None
    creator: Optional[str] = None  # Author
    language: Optional[str] = None
    identifier: Optional[str] = None
    publisher: Optional[str] = None
    date: Optional[str] = None
    rights: Optional[str] = None
    all_metadata: Dict[str, List[str]] = field(default_factory=dict)

@dataclass
class ManifestItem:
    """
    Represents an item in the EPUB manifest.
    """
    id: str
    href: str
    media_type: str
    properties: Optional[str] = None

@dataclass
class SpineItem:
    """
    Represents an item in the EPUB spine.
    """
    idref: str
    linear: bool = True

@dataclass
class EpubBook:
    """
    Represents a complete EPUB book's structure, metadata, and content.
    """
    metadata: EpubMetadata
    manifest: Dict[str, ManifestItem] = field(default_factory=dict)
    spine: List[SpineItem] = field(default_factory=list)
    toc: List[Dict] = field(default_factory=list)  # For NCX or Nav document
    content: Dict[str, bytes] = field(default_factory=dict)
