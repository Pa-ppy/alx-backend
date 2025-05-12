#!/usr/bin/env python3
"""Helper function for pagination.
"""

from typing import Tuple


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """Return a tuple of start and end index for pagination parameters.

    Args:
        page (int): Page number (1-indexed).
        page_size (int): Number of items per page.

    Returns:
        Tuple[int, int]: Tuple containing the start index and the end index.
    """
    start = (page - 1) * page_size
    end = page * page_size
    return start, end
