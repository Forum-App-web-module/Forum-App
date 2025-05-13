from unittest.mock import Mock, patch
import unittest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

class GetConversations_Should(unittest.TestCase):

    @patch('routers.api.messages.verify_access_token', return_value = {"key": {
            "id" : 1,
            "username" : "Tester1",
            "email" : "Test@email.com",
            "bio" : "test bio",
            "is_admin" : 1,
            "is_active" : 1
        }})
    @patch('routers.api.messages.list_conversations', return_value = ['alice','bob','charlie'])
    def test_get_conversations_returns_list_of_conversations(self, mock_list_conversations, mock_verify_access_token):
        response = client.get('/api/messages/', headers={"token": "TestToken"})

        self.assertEqual(response.json(), ['alice', 'bob', 'charlie'])
        mock_list_conversations.assert_called_once_with(1)
        mock_verify_access_token.assert_called_once_with("TestToken")
        

class GetSpecificConversation_Should(unittest.TestCase):

    @patch('routers.api.messages.verify_access_token', return_value = {"key": {
            "id" : 1,
            "username" : "Tester1",
            "email" : "Test@email.com",
            "bio" : "test bio",
            "is_admin" : 1,
            "is_active" : 1
        }})
    @patch('routers.api.messages.find_user_by_username', return_value=None)
    def test_get_specific_conversation_returns_400_when_invalid_username(self, mock_find_user_by_username, mock_verify_access_token):
        response = client.get('/api/messages/Tester1', headers={"token": "TestToken"})

        self.assertEqual(response.status_code, 400)
        mock_find_user_by_username.assert_called_once_with("Tester1")
        mock_verify_access_token.assert_called_once_with("TestToken")



    @patch('routers.api.messages.verify_access_token', return_value = {"key": {
            "id" : 1,
            "username" : "Tester1",
            "email" : "Test@email.com",
            "bio" : "test bio",
            "is_admin" : 1,
            "is_active" : 1
        }})
    @patch('routers.api.messages.find_user_by_username', return_value=Mock(id=2))
    @patch('routers.api.messages.list_messages', return_value = None)
    def test_get_specific_conversation_returns_204_when_no_messages(self, mock_list_messages, mock_find_user_by_username, mock_verify_access_token):
        response = client.get('/api/messages/Tester1', headers={"token": "TestToken"})

        self.assertEqual(response.status_code, 204)
        mock_find_user_by_username.assert_called_once_with("Tester1")
        mock_verify_access_token.assert_called_once_with("TestToken")
        mock_list_messages.assert_called_once_with(1,2)


    @patch('routers.api.messages.verify_access_token', return_value = {"key": {
            "id" : 1,
            "username" : "Tester1",
            "email" : "Test@email.com",
            "bio" : "test bio",
            "is_admin" : 1,
            "is_active" : 1
        }})
    @patch('routers.api.messages.find_user_by_username', return_value=Mock(id=2))
    @patch('routers.api.messages.list_messages', return_value=[{"id" : 1,
                   "text" : "testtext",
                   "sent_on" : "testdate",
                   "sender_username" : "Tester1",
                   "receiver_username" : "Tester2"}])
    def test_get_specific_conversation_returns_list_of_messages(self, mock_list_messages, mock_find_user_by_username, mock_verify_access_token):
        response = client.get('/api/messages/Tester1', headers={"token": "TestToken"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [{"id" : 1,
                   "text" : "testtext",
                   "sent_on" : "testdate",
                   "sender_username" : "Tester1",
                   "receiver_username" : "Tester2"}] )
        mock_find_user_by_username.assert_called_once_with("Tester1")
        mock_verify_access_token.assert_called_once_with("TestToken")
        mock_list_messages.assert_called_once_with(1,2)


class CreateMessage_Should(unittest.TestCase):

    @patch('routers.api.messages.verify_access_token', return_value = {"key": {
            "id" : 1,
            "username" : "Tester1",
            "email" : "Test@email.com",
            "bio" : "test bio",
            "is_admin" : 1,
            "is_active" : 1
        }})
    @patch('routers.api.messages.find_user_by_username', return_value=None)
    def test_create_message_returns_400_when_invalid_username(self, mock_find_user_by_username, mock_verify_access_token):
        response = client.post('/api/messages/Tester1', headers={"token": "TestToken"}, content='"testMessage"')

        self.assertEqual(response.status_code, 400)
        mock_find_user_by_username.assert_called_once_with("Tester1")
        mock_verify_access_token.assert_called_once_with("TestToken")


    @patch('routers.api.messages.verify_access_token', return_value = {"key": {
            "id" : 1,
            "username" : "Tester1",
            "email" : "Test@email.com",
            "bio" : "test bio",
            "is_admin" : 1,
            "is_active" : 1
        }})
    @patch('routers.api.messages.find_user_by_username', return_value=Mock(id=2))
    @patch('routers.api.messages.create', return_value=7)
    def test_create_message_returns_201_when_succesfull_creation(self, mock_create, mock_find_user_by_username, mock_verify_access_token):
        response = client.post('/api/messages/Tester1', headers={"token": "TestToken"}, content='"testMessage"')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.text, "Message is created" )
        mock_find_user_by_username.assert_called_once_with("Tester1")
        mock_verify_access_token.assert_called_once_with("TestToken")
        mock_create.assert_called_once_with(1,2,"testMessage")
