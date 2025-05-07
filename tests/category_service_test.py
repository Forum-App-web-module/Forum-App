import unittest
from unittest.mock import Mock, create_autospec, patch
from data.models import Category
from services import category_service

# mock_db = Mock()
# category_service.database = mock_db


class CategoryService_Should(unittest.TestCase):

    def test_get_all_categories_when_data_is_present(self):
        get_data_func = lambda q: [(1, "Test Category 1", 0, 0),
                                   (2, "Test Category 2", 1, 1)]
        result = list(category_service.get_all(get_data_func))
        self.assertEqual(2, len(result))
        self.assertEqual(Category, type(result[0]))
        self.assertEqual(1, result[0].id)
        self.assertEqual("Test Category 1", result[0].name)
        self.assertEqual(0, result[0].is_private)
        self.assertEqual(0, result[0].lock)

    def test_get_all_categories_when_data_is_empty(self):
        get_data_func = lambda q: []
        result = list(category_service.get_all(get_data_func))
        self.assertEqual(0, len(result))





