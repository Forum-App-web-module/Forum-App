import unittest
from unittest.mock import Mock, create_autospec, patch
from data.models import Replies
from services import reply_service

# mock_db = Mock()
# reply_service.database = mock_db


class ReplyService_Should(unittest.TestCase):
    def setUp(self):
        # mocking the db calls
        self.insert_query = Mock()
        self.query_count = Mock()
        self.update_query = Mock()

        # monkey-patching the service functions
        reply_service.insert_query = self.insert_query
        reply_service.query_count = self.query_count
        reply_service.update_query = self.update_query



    @patch('services.reply_service.insert_query')
    def test_create_reply_insert_once_with_parameters(self, mock_insert_query):
        # Arrange
        mock_reply_data = 1
        mock_insert_query.return_value = mock_reply_data

        #Act
        result = reply_service.create_reply('Test Reply', 1, 1)

        #Assert
        # Commenting out a more readable approach but it could fail the test if the string is off
        # even by a single space.

        # mock_insert_query.assert_called_once_with(
        #     """
        #             insert into replies
        #             (creator_id,
        #             topic_id,
        #             text,
        #             created_on)
        #             values (?, ?, ?, NOW())
        #             """,
        #     (1, 1, "Test Reply"))

        mock_insert_query.assert_called_once()
        sql_arg, params_arg = mock_insert_query.call_args[0]
        self.assertIn("insert into replies", sql_arg.lower())
        self.assertEqual((1, 1, "Test Reply"), params_arg)

        self.assertEqual(mock_reply_data, result)

    def test_validate_topic_and_reply_raises_exception(self):
        # Arrange
        self.query_count.return_value = 0

        #Act & Assert
        with self.assertRaises(ValueError):
            reply_service.validate_topic_and_reply(1, 1)

    def test_validate_topic_and_reply_returns_count_when_valid(self):
        # Arrange
        self.query_count.return_value = 1
        # Act
        result = reply_service.validate_topic_and_reply(1, 1)
        #Assert
        self.assertEqual(1, result)
        self.query_count.assert_called_once()

    def test_vote_to_db_returns_vote_when_exists(self):
        # Arrange
        self.update_query.return_value = 1
        # Act
        result = reply_service.vote_to_db(1, 1, 1)
        #Assert
        self.assertEqual(1, result)

    def test_vote_to_db_returns_vote_when_not_exists(self):
        # Arrange
        self.update_query.return_value = -1
        # Act
        result = reply_service.vote_to_db(1, 1, -1)
        # Assert
        self.assertEqual(-1, result)

    def test_mark_best_reply_returns_false_when_user_not_author(self):
        # Arrange
        reply_service.validate_is_author = Mock(return_value=False)
        # Act
        result = reply_service.mark_best_reply(1, 1, 1)
        # Assert
        self.assertFalse(result)

    def test_mark_best_reply_returns_true_when_user_is_author(self):
        # Arrange
        reply_service.validate_is_author = Mock(return_value=True)
        # Act
        result = reply_service.mark_best_reply(1, 1, 1)
        # Assert
        self.assertTrue(result)
        self.update_query.assert_called_once()

    def test_validate_is_author_returns_rowcount_when_valid(self):
        # Arrange
        self.query_count.return_value = 1
        # Act
        result = reply_service.validate_is_author(1, 1)
        # Assert
        self.assertEqual(1, result)


