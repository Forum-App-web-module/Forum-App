import unittest
from unittest.mock import Mock, create_autospec, patch
from data.models import UserResponseList
from services.user_service import create, find_user_by_username, get_users, promote, deactivate, activate, update_bio, try_login, exists 

# mock_db = Mock()
# user_service.database = mock_db


class CreateUser_Should(unittest.TestCase):
    def test_create_calls_insert_data_func_with_correct_args(self):
        mock_insert = Mock(return_value=123)

        result = create("john_doe", "john@example.com", "hashedpassword", insert_data_func=mock_insert)

        mock_insert.assert_called_once_with(
            'INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
            ("john_doe", "john@example.com", "hashedpassword")
        )
        self.assertEqual(result, 123)

class FindUserByUsername_Should(unittest.TestCase):
    def test_find_user_by_username_returns_user(self):
        mock_read = Mock(return_value=[(1, "john_doe", "john@example.com", "bio", 1, 1)])

        result = find_user_by_username("john_doe", get_data_func=mock_read)

        mock_read.assert_called_once_with(
            'SELECT id, username, email, bio, is_admin, is_active FROM users WHERE username = ?',
            ("john_doe",)
        )
        self.assertEqual(result.username, "john_doe")
        self.assertEqual(result.is_admin, True)

class GetUsers_Should(unittest.TestCase):
    def test_get_users_returns_user_list(self):
        mock_read = Mock(return_value=[("john_doe", 1), ("jane_doe", 0)])

        result = get_users("john", "true", get_data_func=mock_read)

        mock_read.assert_called_once_with(
            'SELECT username, is_admin FROM users WHERE username LIKE ? and is_admin = ?',
            ("john%", 1)
        )
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], UserResponseList)
        self.assertEqual(result[0].username, "john_doe")

class Promote_Should(unittest.TestCase):
    def test_promote_calls_update_func_with_correct_args(self):
        mock_update = Mock(return_value=1)  # simulate successful update

        result = promote("john_doe", update_func=mock_update)

        mock_update.assert_called_once_with(
            'UPDATE users SET is_admin = ? WHERE username = ?',
            (1, "john_doe")
        )
        self.assertEqual(result, 1)

class DeactivateActivate_Should(unittest.TestCase):
    def test_deactivate_calls_update_func(self):
        mock_update = Mock(return_value=1)  # simulate successful update

        result = deactivate("john_doe", update_func=mock_update)

        mock_update.assert_called_once_with(
            'UPDATE users SET is_active = ? WHERE username = ?',
            (0, "john_doe")
        )
        self.assertEqual(result, 1)

    def test_activate_calls_update_func(self):
        mock_update = Mock(return_value=1)  # simulate successful update

        result = activate("john_doe", update_func=mock_update)

        mock_update.assert_called_once_with(
            'UPDATE users SET is_active = ? WHERE username = ?',
            (1, "john_doe")
        )
        self.assertEqual(result, 1)

class Exists_Should(unittest.TestCase):
    def test_exists_returns_correct_result(self):
        mock_read = Mock(return_value=[("john_doe",)])

        result = exists("john_doe", get_data_func=mock_read)

        mock_read.assert_called_once_with(
            'SELECT username FROM users WHERE username = ?',
            ("john_doe",)
        )
        self.assertEqual(result, [("john_doe",)])

class UpdateBio_Should(unittest.TestCase):
    def test_update_bio_calls_update_func_with_correct_args(self):
        mock_update = Mock(return_value=1)  # simulate successful update

        result = update_bio("john_doe", "new bio", update_func=mock_update)

        mock_update.assert_called_once_with(
            'UPDATE users SET bio = ? WHERE username = ?',
            ("new bio", "john_doe")
        )
        self.assertEqual(result, 1)

class TryLogin_Should(unittest.TestCase):
    def test_try_login_returns_user_data(self):
        mock_read = Mock(return_value=[(1, "john_doe", "john@example.com", "bio", 1, 1)])

        result = try_login("john_doe", "hashedpassword", get_data_func=mock_read)

        mock_read.assert_called_once_with(
            'SELECT id, username, email, bio, is_admin, is_active from users WHERE username = ? and password = ?',
            ("john_doe", "hashedpassword")
        )
        self.assertTrue(result["key"]["id"])
        self.assertEqual(result["key"]["username"], "john_doe")