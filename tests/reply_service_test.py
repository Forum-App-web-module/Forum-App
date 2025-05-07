import unittest
from unittest.mock import Mock, create_autospec, patch
from data.models import Replies
from services import reply_service

# mock_db = Mock()
# reply_service.database = mock_db


class ReplyService_Should(unittest.TestCase):

    @patch('services.reply_service.insert_query')
    def test_create_reply_insert_once_with_parameters(self, mock_insert_query):
        # Arrange
        mock_reply_data = 1
        mock_insert_query.return_value = mock_reply_data

        #Act
        result = reply_service.create_reply("Test Reply", 1, 1)

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

