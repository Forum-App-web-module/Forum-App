import unittest
from unittest.mock import Mock, patch
from routers.api.topics import view_topics, view_topic_by_id, create_topic, lock_topic
from fastapi import FastAPI
from common.responses import NotFound, Created

class TopicRouterShould(unittest.TestCase):

    @patch('routers.api.topics.topic_service.get_all_topics')
    def test_view_topics(self, mock_get):
        mock_get.return_value = ["Test Topic 1", "Test Topic 2"]

        result = view_topics()

        self.assertEqual(result, ["Test Topic 1", "Test Topic 2"])
        mock_get.assert_called_once()

    @patch('routers.api.topics.topic_service.get_topic_with_replies', return_value={'topic': 'T1'})
    def test_view_topic_by_id_found(self, mock_get):
        result = view_topic_by_id(1)

        self.assertEqual(result, {'topic': 'T1'})
        mock_get.assert_called_once_with(1)

    @patch('routers.api.topics.topic_service.get_topic_with_replies', return_value=None)
    def test_view_topic_by_id_not_found(self, mock_get):
        result = view_topic_by_id(10)

        self.assertIsInstance(result, NotFound)
        mock_get.assert_called_once_with(10)

    @patch('routers.api.topics.verify_access_token', return_value={'key': {'id': 1}})
    @patch('routers.api.topics.topic_service.create_topic', return_value=10)
    def test_create_topic_success(self, mock_create, mock_verify):
        result = create_topic(title='Test', category_id=1, token='token')

        self.assertIsInstance(result, Created)
        mock_verify.assert_called_once_with('token')
        mock_create.assert_called_once_with('Test', 1, 1)

    @patch('routers.api.topics.verify_access_token', return_value={'key': {'id': 1}})
    @patch('routers.api.topics.admin_auth', return_value=True)
    @patch('routers.api.topics.topic_service.update_topic')
    def test_lock_topic(self, mock_update, mock_admin, mock_verify):
        result = lock_topic(topic_id=1, lock=1, token='token')

        self.assertIsInstance(result, Created)
        mock_verify.assert_called_once_with('token')
        mock_admin.assert_called_once()
        mock_update.assert_called_once_with(1, 1)