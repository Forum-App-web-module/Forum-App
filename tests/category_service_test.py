import unittest
from unittest.mock import Mock, create_autospec, patch
from data.models import Category, Topic
from services import category_service

# mock_db = Mock()
# category_service.database = mock_db


class CategoryService_Should(unittest.TestCase):

    #def test_get_all_categories_when_data_is_present(self):
    #    get_data_func = lambda q: [(1, "Test Category 1", 0, 0),
    #                               (2, "Test Category 2", 1, 1)]
    #    result = list(category_service.get_all(get_data_func))
    #    self.assertEqual(2, len(result))
    #    self.assertEqual(Category, type(result[0]))
    #    self.assertEqual(1, result[0].id)
    #    self.assertEqual("Test Category 1", result[0].name)
    #    self.assertEqual(0, result[0].is_private)
    #    self.assertEqual(0, result[0].lock)
#
    #def test_get_all_categories_when_data_is_empty(self):
    #    get_data_func = lambda q: []
    #    result = list(category_service.get_all(get_data_func))
    #    self.assertEqual(0, len(result))
#
    def test_get_all_categories_when_data_is_present(self):
        mock_data = Mock(return_value=[
            (1, "Category 1", 0, 0),
            (2, "Category 2", 1, 1)
        ])

        result = category_service.get_all(get_data_func=mock_data)

        self.assertEqual(2, len(result))
        self.assertEqual(result[0].id, 1)
        self.assertEqual(result[1].name, "Category 2")
        self.assertIsInstance(result[1], Category)

        mock_data.assert_called_once()

    def test_get_all_categories_when_data_is_empty(self):
        mock_data = Mock(return_value=[])

        result = category_service.get_all(get_data_func=mock_data)

        self.assertEqual(result, [])

        mock_data.assert_called_once()

    def test_get_category_by_id_returns_category(self):
        mock_data = Mock(return_value=[(1, "Test Category 1", 1, 1)])

        category = category_service.get_category_by_id(1, get_data_func=mock_data)

        self.assertEqual(category.id, 1)
        self.assertTrue(category.is_private)
        self.assertIsInstance(category, Category)
        self.assertTrue(category.lock)

        mock_data.assert_called_once()

    def test_get_category_by_id_returns_none_if_not_found(self):
        mock_data = Mock(return_value=[])

        category = category_service.get_category_by_id(11, get_data_func=mock_data)

        self.assertIsNone(category)

        mock_data.assert_called_once()

    def test_get_topics_by_category_returs_topic_list(self):
        mock_data = Mock(return_value=[
            (1, "Topic 1", 1, 2, None, 0),
            (2, "Topic 2", 1, 2, None, 1),
            (3, "Topic 3", 1, 3, None, 1)
        ])

        topics = category_service.get_topics_by_category(3, get_data_func=mock_data)

        self.assertEqual(len(topics), 3)
        self.assertEqual(topics[0].title, "Topic 1")
        self.assertIsInstance(topics[1], Topic)
        self.assertTrue(topics[2].lock)

        mock_data.assert_called_once()

    def test_create_category_returns_id(self):
        mock_insert = Mock(return_value=5)

        result = category_service.create_category("New Category", insert_func=mock_insert)

        self.assertEqual(result, 5)

        mock_insert.assert_called_once()

    def test_lock_category_updates_status(self):
        mock_update = Mock(return_value=1)

        result = category_service.lock_category(2, 1, update_func=mock_update)

        self.assertEqual(result, 1)
        mock_update.assert_called_once()

    def test_is_locked_returns_true_if_category_not_found(self):
        mock_read = Mock(return_value=None)

        result = category_service.is_locked(2, get_data_func=mock_read)
        self.assertTrue(result)

    def test_is_locked_returns_correct_value(self):
        mock_read = Mock(return_value=[(1, "Test Category 1", False, True)])

        result = category_service.is_locked(1, get_data_func=mock_read)
        self.assertTrue(result)

    def test_update_privacy_updates_status(self):
        mock_update = Mock(return_value=1)

        result = category_service.update_privacy(2, 1, update_func=mock_update)

        self.assertEqual(result, 1)
        mock_update.assert_called_once()


    def test_is_private_returns_true_if_category_not_found(self):
        mock_read = Mock(return_value=None)

        result = category_service.is_private(2, get_data_func=mock_read)
        self.assertTrue(result)

    def test_is_private_returns_correct_value(self):
        mock_read = Mock(return_value=[(1, "Test Category 1", True, True)])

        result = category_service.is_private(1, get_data_func=mock_read)
        self.assertTrue(result)
