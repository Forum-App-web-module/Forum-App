import unittest
from unittest.mock import Mock, create_autospec, patch
from data.models import Replies
from routers import replies as replies_router
from common.responses import BadRequest, Created

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
        self.patcher_reply_service = patch('routers.replies.reply_service')
        self.patcher_category_service = patch('routers.replies.category_service')
        self.patcher_topic_service = patch('routers.replies.topic_service')
        self.patcher_verify_access_token = patch('routers.replies.verify_access_token')

        self.mock_reply_service = self.patcher_reply_service.start()
        self.mock_category_service = self.patcher_category_service.start()
        self.mock_topic_service = self.patcher_topic_service.start()
        self.mock_verify_access_token = self.patcher_verify_access_token.start()

        # Common return for token verification
        self.mock_verify_access_token.return_value = {'key': {'id': 1, 'username': 'test_user'}}       # {'key': {'id': 1}}
        self.mock_user_has_access = True

    def tearDown(self):
        patch.stopall()

    def test_create_reply_returns_400_when_topic_locked(self):
        # Arrange
        self.mock_category_service.is_locked.return_value = True

        #Act
        result = replies_router.create_reply(1, 'Test Reply', 'test_token')

        # Assert
        self.assertIsInstance(result, BadRequest)
        self.assertEqual(result.status_code, 400)

    # @patch('routers.replies.verify_access_token', return_value={'key': {'id': 1, 'username': 'test_user'}})
    @patch('routers.replies.admin_auth', return_value=False)
    def test_create_reply_returns_201_when_user_with_access(self, mock_admin_auth): # mock_verify_token
        # Arrange
        self.mock_category_service.is_locked.return_value = False
        self.mock_category_service.is_private.return_value = False

        # Act
        result = replies_router.create_reply(1, 'Test Reply', 'test_token')

        # Assert
        self.assertIsInstance(result, Created)
        self.assertEqual(result.status_code, 201)

    @patch('routers.replies.verify_access_token', return_value={'key': {'id': 1, 'username': 'test_user'}})
    @patch('routers.replies.admin_auth', return_value=False)
    def test_create_reply_returns_400_when_private_category_and_notAdmin(self, mock_admin_auth, mock_verify_token):
        # Arrange
        self.mock_category_service.is_locked.return_value = False
        self.mock_category_service.is_private.return_value = True

        # Act
        result = replies_router.create_reply(1, 'Test Reply', 'test_token')

        # Assert
        self.assertIsInstance(result, BadRequest)
        self.assertEqual(result.status_code, 400)