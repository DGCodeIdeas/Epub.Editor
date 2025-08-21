import zipfile
import os
from pathlib import Path

from epub_editor_pro.core.epub_model import EpubBook

class EpubSaver:
    """
    Saves the changes in an EpubBook object back to an EPUB file.
    """

    def __init__(self, book: EpubBook):
        self.book = book

    def save(self, backup=True):
        """
        Saves the EPUB file.

        Args:
            backup: If True, creates a backup of the original file.
        """
        if not self.book.is_modified:
            # No changes to save
            return

        original_path = Path(self.book.filepath)
        temp_path = original_path.with_suffix(original_path.suffix + '.tmp')
        backup_path = original_path.with_suffix(original_path.suffix + '.bak')

        try:
            with zipfile.ZipFile(self.book.filepath, 'r') as original_zip:
                with zipfile.ZipFile(temp_path, 'w', zipfile.ZIP_DEFLATED) as new_zip:
                    # Write mimetype file first, uncompressed
                    mimetype_info = original_zip.getinfo('mimetype')
                    mimetype_content = original_zip.read(mimetype_info)
                    new_zip.writestr(mimetype_info, mimetype_content, compress_type=zipfile.ZIP_STORED)

                    # Get list of modified files from the content manager cache
                    modified_files = self.book.content_manager._content_cache.keys()

                    # Copy files from original to new, skipping modified files
                    for item in original_zip.infolist():
                        if item.filename == 'mimetype':
                            continue

                        # Find the corresponding manifest item href
                        # This is tricky because item.filename is the full path in zip,
                        # and href is relative.
                        # For now, we assume a direct mapping. A more robust solution
                        # would be needed for complex EPUBs.

                        # A simple way to check is to see if the filename ends with any of the hrefs
                        is_modified = False
                        for href in modified_files:
                            if item.filename.endswith(href):
                                is_modified = True
                                break

                        if not is_modified:
                            new_zip.writestr(item, original_zip.read(item.filename))

                    # Write modified files from the cache
                    for href, content in self.book.content_manager._content_cache.items():
                        # We need to find the original zipinfo to preserve metadata
                        # This is again tricky. Let's find it by href.
                        found_info = None
                        for info in original_zip.infolist():
                            if info.filename.endswith(href):
                                found_info = info
                                break

                        if found_info:
                             new_zip.writestr(found_info, content)
                        else:
                            # If it's a new file (not yet supported), we'd add it here.
                            # For now, we assume we only modify existing files.
                            # We'll just write it with the href as the name.
                            new_zip.writestr(href, content)

            # Atomic save: rename original, then rename temp to original
            if backup and original_path.exists():
                os.replace(original_path, backup_path)

            os.replace(temp_path, original_path)

            # Reset modification state
            self.book.is_modified = False
            self.book.content_manager._content_cache.clear()

        except Exception as e:
            # Clean up temp file on error
            if temp_path.exists():
                os.remove(temp_path)
            raise IOError(f"Failed to save EPUB file: {e}") from e
