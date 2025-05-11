import unittest
from unittest.mock import Mock, create_autospec, patch
from data.models import Replies
from routers.api import replies as replies_router
from common.responses import BadRequest, Created
from routers.api.replies import user_has_access


# mock_reply_service = Mock(spec=reply_service)
# replies_router.reply_service = mock_reply_service
#
# mock_category_service = Mock(spec=category_service)
# replies_router.category_service = mock_category_service
#
# def fake_reply(reply = 'Test Reply', topic_id = 1, user_id = 1):
#     mock_reply = Mock(spec=Replies)
#     mock_reply.text = reply
#     mock_reply.topic_id = topic_id
#     mock_reply.user_id = user_id
#     return mock_reply


class ReplyRouter_Should(unittest.TestCase):

    def setUp(self):
        # Patch services in the replies_router module
        self.patcher_reply_service = patch('routers.api.replies.reply_service')
        self.patcher_category_service = patch('routers.api.replies.category_service')
        self.patcher_topic_service = patch('routers.api.replies.topic_service')
        self.patcher_verify_access_token = patch('routers.api.replies.verify_access_token')
        self.patcher_replies_admin_auth = patch('routers.api.replies.admin_auth')

        self.mock_reply_service = self.patcher_reply_service.start()
        self.mock_category_service = self.patcher_category_service.start()
        self.mock_topic_service = self.patcher_topic_service.start()
        self.mock_verify_access_token = self.patcher_verify_access_token.start()
        self.mock_replies_admin_auth = self.patcher_replies_admin_auth.start()

        # Common return for token verification
        self.mock_verify_access_token.return_value = {'key': {'id': 1, 'username': 'test_user'}}       # {'key': {'id': 1}}
        self.mock_replies_admin_auth.return_value = True
        self.mock_user_has_access = True

    def tearDown(self):
        patch.stopall()

    def test_user_has_access_returns_true_when_admin(self):
        #Arrange
        mock_payload = self.mock_verify_access_token.return_value
        # Act
        result = user_has_access(mock_payload, 1)
        #Assert
        self.assertTrue(result)

    def test_user_has_access_returns_true_when_not_private_category(self):
        #Arrange
        mock_payload = self.mock_verify_access_token.return_value
        self.mock_replies_admin_auth.return_value = False
        self.mock_category_service.is_private.return_value = False
        #Act
        result = user_has_access(mock_payload, 1, 1)
        #Assert
        self.assertTrue(result)

    @patch('services.category_members_service.is_member', return_value=True)
    def test_user_has_access_returns_true_when_is_member_is_true(self, mock_is_member):
        #Arrange
        mock_payload = self.mock_verify_access_token.return_value
        self.mock_replies_admin_auth.return_value = False
        self.mock_category_service.is_private.return_value = True
        # Act
        result = user_has_access(mock_payload, 1, 1)
        # Assert
        self.assertTrue(result)

    def test_user_has_access_returns_false_when_private_category_and_user_not_member(self):
        # Arrange
        mock_payload = self.mock_verify_access_token.return_value
        self.mock_replies_admin_auth.return_value = False
        self.mock_category_service.is_private.return_value = True
        self.mock_category_service.is_member.return_value = False
        # Act
        result = user_has_access(mock_payload, 1)
        # Assert
        self.assertFalse(result)

    def test_create_reply_returns_400_when_topic_locked(self):
        # Arrange
        self.mock_category_service.is_locked.return_value = True
        #Act
        result = replies_router.create_reply(1, 'Test Reply', 'test_token')
        # Assert
        self.assertIsInstance(result, BadRequest)
        self.assertEqual(result.status_code, 400)

    @patch('routers.api.replies.admin_auth', return_value=False)
    def test_create_reply_returns_201_when_user_with_access(self, mock_admin_auth):
        # Arrange
        self.mock_category_service.is_locked.return_value = False
        self.mock_category_service.is_private.return_value = False
        # Act
        result = replies_router.create_reply(1, 'Test Reply', 'test_token')
        # Assert
        mock_admin_auth.assert_called_once()
        self.mock_verify_access_token.assert_called_once_with('test_token')
        self.assertIsInstance(result, Created)
        self.assertEqual(result.status_code, 201)

    @patch('routers.api.replies.user_has_access', return_value=False)
    def test_create_reply_returns_400_when_private_category_and_notAdmin(self, mock_user_has_access):
        # Arrange
        self.mock_category_service.is_locked.return_value = False
        # Act
        result = replies_router.create_reply(1, 'Test Reply', 'test_token')
        # Assert
        mock_user_has_access.assert_called_once()
        self.mock_verify_access_token.assert_called_once_with('test_token')
        self.assertIsInstance(result, BadRequest)
        self.assertEqual(result.status_code, 400)

    def test_mark_best_reply_returns_400_when_user_not_author(self):
        #Arrange
        self.mock_reply_service.mark_best_reply.return_value = False
        #Act
        result = replies_router.mark_best_reply(1, 1, 'test_token')
        #Assert
        self.mock_verify_access_token.assert_called_once_with('test_token')
        self.assertIsInstance(result, BadRequest)
        self.assertEqual(result.status_code, 400)

    def test_mark_best_reply_returns_201_when_user_is_author(self):
        # Arrange
        self.mock_reply_service.validate_is_author.return_value = True
        # Act
        result = replies_router.mark_best_reply(1, 1, 'test_token')
        # Assert
        self.mock_verify_access_token.assert_called_once_with('test_token')
        self.assertIsInstance(result, Created)
        self.assertEqual(result.status_code, 201)































