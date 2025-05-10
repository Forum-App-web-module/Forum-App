import unittest
from unittest.mock import Mock, create_autospec, patch
from data.models import Topic
from services import topic_service

# mock_db = Mock()
# topic_service.database = mock_db


class TopicService_Should(unittest.TestCase):
    
# def create_topic(title: str, category_id: int, author_id: int, insert_func=None)
    def test_create_topic_returns_new_topic(self):
        mock_insert = Mock(return_value=11)

        new_topic_id = topic_service.create_topic("Test Topic 1", 1, 2, insert_func=mock_insert)

        self.assertEqual(new_topic_id, 11)
        mock_insert.assert_called_once()

    def test_get_all_topics(self):
        mock_data = [
            (1, "Topic 1", 1, 2, None, 0),
            (2, "Topic 2", 2, 2, None, 1),
            (3, "Topic 3", 3, 1, None, 0)
        ]

        mock_read = Mock(return_value=mock_data)

        topics = topic_service.get_all_topics(get_data_func=mock_read)

        self.assertEqual(len(topics), 3)
        self.assertIsInstance(topics[0], Topic)
        self.assertEqual(topics[2].title, "Topic 3")
        self.assertTrue(topics[1].lock)

    #TODO
    def test_get_topic_with_replies(self):
        pass

    def test_update_topic_returns_success(self):
        mock_update = Mock(return_value=1)

        result = topic_service.update_topic(1, locked=1, update_func=mock_update)

        self.assertEqual(result, 1)
        mock_update.assert_called_once()

    def test_is_locked_returns_true_if_no_topic_found(self):
        mock_empty = Mock(return_value=None)

        result = topic_service.is_locked(2, get_data_func=mock_empty)

        self.assertTrue(result)

    def test_is_locked_returns_false_if_not_locked(self):
        topic_data = {
            "topic":Topic(id=1, title="Test Title 1", category_id=1, author_id=1, best_reply_id=None, lock=False),
            "replies": []
        }

        mock_tpic_fetch = Mock(return_value=topic_data)

        result = topic_service.is_locked(1, topic_fetch_func=mock_tpic_fetch)
        self.assertFalse(result)

    def test_get_category_id_returns_category_id(self):
        mock_read = Mock(return_value=[(2,)])

        category_id = topic_service.get_category_id(5, get_data_func=mock_read)

        self.assertEqual(category_id, 2)