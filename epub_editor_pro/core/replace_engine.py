import re
from bs4 import BeautifulSoup

from epub_editor_pro.core.epub_model import EpubBook

class ReplaceEngine:
    """A class to perform find and replace operations within an EPUB."""

    def __init__(self, book: EpubBook):
        self.book = book

    def replace_all(self, find: str, replace: str, case_sensitive: bool, whole_word: bool, regex: bool) -> int:
        """
        Replaces all occurrences of a string in the EPUB content.

        Args:
            find: The text to search for.
            replace: The text to replace with.
            case_sensitive: Whether the search is case-sensitive.
            whole_word: Whether to match whole words only.
            regex: Whether the query is a regular expression.

        Returns:
            The total number of replacements made.
        """
        flags = 0 if case_sensitive else re.IGNORECASE

        if not regex:
            find = re.escape(find)

        if whole_word:
            find = r'\b' + find + r'\b'

        try:
            search_pattern = re.compile(find, flags)
        except re.error as e:
            raise ValueError(f"Invalid regular expression: {e}") from e

        total_replacements = 0

        content_manager = self.book.content_manager
        for item in self.book.manifest.values():
            if "html" in item.media_type:
                try:
                    content = content_manager.get_content(item.href)
                    soup = BeautifulSoup(content, "lxml")

                    text_nodes = soup.find_all(string=True)

                    file_replacements = 0
                    for node in text_nodes:
                        # Make sure we don't modify text in style or script tags
                        if node.parent.name in ['style', 'script']:
                            continue

                        new_content, num_subs = search_pattern.subn(replace, node.string)
                        if num_subs > 0:
                            node.string.replace_with(new_content)
                            file_replacements += num_subs

                    if file_replacements > 0:
                        new_html = soup.prettify(encoding='utf-8')
                        content_manager.update_content(item.href, new_html)
                        total_replacements += file_replacements
                except (FileNotFoundError, KeyError):
                    # Silently ignore files that can't be found or read.
                    continue

        return total_replacements

    def batch_replace_all(self, operations: list[tuple[str, str]], case_sensitive: bool, whole_word: bool, regex: bool) -> int:
        """
        Performs a batch of replace all operations.

        For simplicity, this implementation iterates through the operations and calls
        replace_all for each. A more optimized version might process all replacements
        in a single pass over the content.

        Args:
            operations: A list of (find, replace) tuples.
            case_sensitive: Whether the search is case-sensitive for all operations.
            whole_word: Whether to match whole words for all operations.
            regex: Whether the queries are regular expressions for all operations.

        Returns:
            The total number of replacements made across all operations.
        """
        total_replacements = 0
        for find, replace in operations:
            total_replacements += self.replace_all(find, replace, case_sensitive, whole_word, regex)
        return total_replacements
