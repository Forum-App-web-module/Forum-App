from unittest.mock import Mock, patch
import unittest
from services.message_service import create, list_messages, list_conversations
from data.models import MessageOut

class Create_Should(unittest.TestCase):

    def test_create_calls_insert_data_func_with_correct_args(self):
        mock_insert = Mock(return_value="message_id_123")

        result = create(1, 2, "Hello!", insert_data_func=mock_insert)

        mock_insert.assert_called_once_with(
            'INSERT INTO messages (text, sender_id, receiver_id) VALUES (?,?,?)',
            ("Hello!", 1, 2)
        )
        self.assertEqual(result, "message_id_123")


class ListMessages_Should(unittest.TestCase):

    def test_list_messages_returns_messahe_objects(self):
        mock_read = Mock(return_value=[
            (1, "Hi", "2024-01-01", "Alice", "Bob"),
            (2, "Hello", "2024-01-02", "Bob", "Alice")
        ])

        result = list_messages(1,2, get_data_func=mock_read)
        
        mock_read.assert_called_once()
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], MessageOut)
        self.assertEqual(result[0].text, "Hi")


class ListConversations_Should(unittest.TestCase):

    def test_list_conversations_returns_list_of_conversations(self):
        mock_read = Mock(return_value=[("Alice",), ("Bob",)])

        result = list_conversations(1, mock_read)

        mock_read.assert_called_once()
        self.assertEqual(result, [("Alice"), ("Bob")])
