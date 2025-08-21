import re
from typing import Iterator
from bs4 import BeautifulSoup

from epub_editor_pro.core.epub_model import EpubBook
from epub_editor_pro.core.search_models import SearchResult

class SearchEngine:
    """A class to perform searches within an EPUB."""

    def __init__(self, book: EpubBook):
        self.book = book

    def search(self, query: str, case_sensitive: bool, whole_word: bool, regex: bool) -> Iterator[SearchResult]:
        """
        Searches the EPUB content.

        Args:
            query: The text to search for.
            case_sensitive: Whether the search is case-sensitive.
            whole_word: Whether to match whole words only.
            regex: Whether the query is a regular expression.

        Yields:
            SearchResult objects for each match.
        """
        flags = 0 if case_sensitive else re.IGNORECASE

        if not regex:
            query = re.escape(query)

        if whole_word:
            query = r'\b' + query + r'\b'

        try:
            search_pattern = re.compile(query, flags)
        except re.error as e:
            raise ValueError(f"Invalid regular expression: {e}") from e

        for item in self.book.manifest.values():
            if "html" in item.media_type:
                try:
                    content = self.book.content_manager.get_content(item.href)
                    soup = BeautifulSoup(content, "lxml")
                    text_lines = soup.get_text().splitlines()

                    for i, line in enumerate(text_lines):
                        for match in search_pattern.finditer(line):
                            context_before = line[:match.start()]
                            match_text = match.group(0)
                            context_after = line[match.end():]

                            yield SearchResult(
                                file_path=item.href,
                                line_number=i + 1,
                                match_text=match_text,
                                context_before=context_before,
                                context_after=context_after,
                                item_href=item.href
                            )
                except (FileNotFoundError, KeyError):
                    # Silently ignore files that can't be found or read.
                    # A more robust solution might log this.
                    continue
