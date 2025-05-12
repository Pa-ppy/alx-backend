#!/usr/bin/env python3
"""Server class for paginating popular baby names dataset.
"""

import csv
from typing import List
index_range = __import__('0-simple_helper_function').index_range


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Returns the cached dataset, loading it if not already done.

        Returns:
            List[List]: Dataset excluding the header row.
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]  # Remove header

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """Return the appropriate page of the dataset.

        Args:
            page (int): Page number (1-indexed).
            page_size (int): Number of rows per page.

        Returns:
            List[List]: A list of dataset rows corresponding to the page.
        """
        assert isinstance(
            page, int) and page > 0, "page must be a positive integer"
        assert isinstance(
            page_size, int) and page_size > 0, "page_size must be \
                a positive integer"

        start, end = index_range(page, page_size)
        dataset = self.dataset()

        if start >= len(dataset):
            return []

        return dataset[start:end]
