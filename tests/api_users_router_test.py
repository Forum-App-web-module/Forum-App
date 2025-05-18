from unittest.mock import Mock, patch
import unittest
from fastapi.testclient import TestClient
from main import app
from mariadb import IntegrityError
from fastapi import HTTPException

client = TestClient(app)


class SearchUsers_Should(unittest.TestCase):

    # Test via calling directly the function
    @patch('routers.api.users.verify_access_token', return_value = "Payload")
    def test_search_users_returns_StatusCode_400_if_no_username_and_no_admin(self, mock_verify_access_token):

        # Test via calling the api:

        response = client.get("/api/users/",  # route path
            headers={"token": "test_token"},
            params={"username": "", "is_admin": "False"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b"Please select at least one search parameters.")
        mock_verify_access_token.assert_called_once_with("test_token")

            # test via direct calling the function
        # response = search_user(username="", is_admin="False", token="test_token")
        # self.assertEqual(response.status_code, 400)
        # mock_verify_access_token.assert_called_once_with("test_token")

    @patch('routers.api.users.verify_access_token', return_value = "Payload")
    @patch('routers.api.users.get_users', return_value = [{"username": "Tester1", "is_admin": True}, {"username": "Tester2", "is_admin": True}] )
    def test_search_users_returns_users_list(self, mock_get_users, mock_verify_accesss_token):
        
            # test via direct calling the function
        # expected_response = [{"username": "Tester1", "is_admin": True}, {"username": "Tester2", "is_admin": True}]
        # response = search_user(username="", is_admin="True", token="test_token")
        # self.assertEqual(response,expected_response)
        # mock_verify_access_token.assert_called_once_with("test_token")
        # mock_get_users.assert_called_once_with("", "True")

        response = client.get("/api/users",
                              headers={"token": "test_token"},
                              params={"username":"", "is_admin": "True"})
        
        expected_response = [{"username": "Tester1", "is_admin": True}, {"username": "Tester2", "is_admin": True}]
        self.assertEqual(response.json(), expected_response)
        mock_verify_accesss_token.assert_called_once_with("test_token")
        mock_get_users.assert_called_once_with("", "True")


class Register_Should(unittest.TestCase):

    @patch('routers.api.users.hash_password', return_value="hashedTestPassword")
    @patch('routers.api.users.create', side_effect = IntegrityError("fakeQuery", ("Tester1", "test@example.com", "testpassword"), "Error"))
    def test_register_returns_status_code_400_if_invalid_input(self, mock_create, mock_hash_password):
        response = client.post("/api/users/register",
                              json={"username": "Tester1", "email": "test@example.com", "password": "testpassword"})
        
        self.assertEqual(response.status_code, 400)
        mock_create.assert_called_once_with("Tester1", "test@example.com", "hashedTestPassword")
        mock_hash_password.assert_called_once_with("testpassword")

    @patch('routers.api.users.hash_password', return_value="hashedTestPassword")
    @patch('routers.api.users.create', return_value = 50)
    def test_register_returns_status_code_201_if_succesfull_creations(self, mock_create, mock_hash_password):
        response = client.post("/api/users/register", 
                               json={"username": "Tester1", "email": "test@example.com", "password": "testpassword"})
        
        self.assertEqual(response.status_code, 201)
        mock_create.assert_called_once_with("Tester1", "test@example.com", "hashedTestPassword")
        mock_hash_password.assert_called_once_with("testpassword")
        

class Login_Should(unittest.TestCase):

    @patch('routers.api.users.try_login', return_value = False)
    @patch('routers.api.users.hash_password', return_value="hashedTestPassword")
    def test_login_returns_status_code_400_if_invalid_data(self, mock_hash_password, mock_try_login):
        response = client.post('/api/users/login',
                               json={"username": "Tester1", "password": "TestPassword"})
        
        self.assertEqual(response.status_code, 400)
        mock_hash_password.assert_called_once_with("TestPassword")
        mock_try_login.assert_called_once_with("Tester1", "hashedTestPassword")
        

    @patch('routers.api.users.try_login', return_value = {"key": {
        "id": 1,
        "username": "Tester1",
        "email": "test@example.com",
        "bio": "",
        "is_admin": False,
        "is_active": True}})
    @patch('routers.api.users.hash_password', return_value="hashedTestPassword")
    @patch('routers.api.users.create_access_token', return_value = {"JWT": "testToken"} )
    def test_login_returns_token_when_valid_data(self, mock_create_access_token, mock_hash_password, mock_try_login):
        
        response = client.post('/api/users/login',
                               json={"username": "Tester1", "password": "TestPassword"})
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"JWT": "testToken"})
        mock_hash_password.assert_called_once_with("TestPassword")
        mock_try_login.assert_called_once_with("Tester1", "hashedTestPassword")
        mock_create_access_token.assert_called_once_with({"key": {
        "id": 1,
        "username": "Tester1",
        "email": "test@example.com",
        "bio": "",
        "is_admin": False,
        "is_active": True}})


class GetProfile_Should(unittest.TestCase):

    @patch('routers.api.users.verify_access_token', return_value = "testPayload" )
    @patch('routers.api.users.find_user_by_username', return_value = None)
    def test_get_profile_returns_status_code_204_if_no_such_username(self, mock_find_user_by_username, mock_verify_access_token):
        response = client.get('api/users/Tester1', headers={"token": "TestToken"}, params= {"username": "Tester1"})

        self.assertEqual(response.status_code, 204)
        mock_find_user_by_username.assert_called_once_with("Tester1")
        mock_verify_access_token.assert_called_once_with("TestToken")

    @patch('routers.api.users.verify_access_token', side_effect=HTTPException(401, detail="Authentication failed!"))
    def test_get_profile_raises_HTTPException_if_invalid_token(self, mock_verify_access_token):
        response = client.get('api/users/Tester1', headers={"token": "TestToken"}, params= {"username": "Tester1"})
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"detail" :"Authentication failed!"} )
        mock_verify_access_token.assert_called_once_with("TestToken")

    @patch('routers.api.users.verify_access_token', return_value = "testPayload" )
    @patch('routers.api.users.find_user_by_username', return_value = {"id": 1,
    "username": "TestUser",
    "email": "test@example.com",
    "bio": "",
    "is_admin": False,
    "is_active": True })
    def test_get_profile_returns_user_information_if_valid_input(self, mock_find_user_by_username, mock_verify_access_token):
        expected_result = {"id": 1, "username": "TestUser", "email": "test@example.com", "bio": "", "is_admin": False, "is_active": True }

        response = client.get('api/users/Tester1', headers={"token": "TestToken"}, params= {"username": "Tester1"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected_result )
        mock_verify_access_token.assert_called_once_with("TestToken")


class UpdateProfileBio_Should(unittest.TestCase):

    @patch('routers.api.users.verify_access_token', return_value = {"key": {"username": "Tester1"}} )
    @patch('routers.api.users.update_bio', return_value = 1)
    def test_update_profile_bio_returns_successful_if_valid_input(self, mock_update_bio, mock_verify_access_token):
        response = client.put('/api/users/bio', headers={"token": "TestToken", "Content-Type": "text/plain"}, content= "Test Bio" )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, "Bio is updated" )
        mock_verify_access_token.assert_called_once_with("TestToken")
        mock_update_bio.assert_called_once_with("Tester1", "Test Bio")

    @patch('routers.api.users.verify_access_token', side_effect=HTTPException(401, detail="Authentication failed!"))
    def test_update_profile_bio_returns_401_if_token_invalid(self, mock_verify_access_token):

        response = client.put('api/users/bio', headers={"token": "TestToken", "Content-Type": "text/plain"}, content= "Test Bio" )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"detail" :"Authentication failed!"} )
        mock_verify_access_token.assert_called_once_with("TestToken")


class DeactivateUserShould(unittest.TestCase):

    @patch('routers.api.users.verify_access_token', return_value = {"key": {"username": "Tester1"}})
    @patch('routers.api.users.admin_auth', return_value = True)
    @patch('routers.api.users.exists', return_value = None)
    def test_deactivate_user_returns_400_when_invalid_username(self, mock_exists, mock_admin_auth, mock_verify_access_token):
        response = client.put('/api/users/deactivate/Tester1', headers={'token':"ValidToken"}, params={"username": "Tester1"})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.text, 'There is no account with username: Tester1')
        mock_admin_auth.assert_called_once_with({"key": {"username": "Tester1"}})
        mock_exists.assert_called_once_with("Tester1")
        mock_verify_access_token.assert_called_once_with("ValidToken")

    @patch('routers.api.users.verify_access_token', return_value = {"key": {"username": "Tester1"}} )
    @patch('routers.api.users.admin_auth', return_value = True)
    @patch('routers.api.users.exists', return_value = "Tester1")
    @patch('routers.api.users.deactivate', return_value = 1)
    def test_deactivate_user_returns_successfull_when_account_deactivated(self, mock_deactivate, mock_exists, mock_admin_auth, mock_verify_access_token):
        response = client.put('/api/users/deactivate/Tester1', headers={'token':"ValidToken"}, params={"username": "Tester1"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, 'Tester1 is now blocked.')
        mock_admin_auth.assert_called_once_with({"key": {"username": "Tester1"}})
        mock_exists.assert_called_once_with("Tester1")
        mock_verify_access_token.assert_called_once_with("ValidToken")
        mock_deactivate.assert_called_once_with("Tester1")

    @patch('routers.api.users.verify_access_token', return_value = {"key": {"username": "Tester1"}})
    @patch('routers.api.users.admin_auth', return_value = True)
    @patch('routers.api.users.exists', return_value = "Tester1")
    @patch('routers.api.users.deactivate', return_value = 0)
    def test_deactivate_user_returns_successfull_when_account_already_deactivated(self, mock_deactivate, mock_exists, mock_admin_auth, mock_verify_access_token):
        response = client.put('/api/users/deactivate/Tester1', headers={'token':"ValidToken"}, params={"username": "Tester1"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, 'Tester1 already has been blocked.')
        mock_admin_auth.assert_called_once_with({"key": {"username": "Tester1"}})
        mock_exists.assert_called_once_with("Tester1")
        mock_verify_access_token.assert_called_once_with("ValidToken")
        mock_deactivate.assert_called_once_with("Tester1")


class ActivateUser_Should(unittest.TestCase):

    @patch('routers.api.users.verify_access_token', return_value = {"key": {"username": "Tester1"}})
    @patch('routers.api.users.admin_auth', return_value = True)
    @patch('routers.api.users.exists', return_value = None)
    def test_activate_user_returns_400_when_invalid_username(self, mock_exists, mock_admin_auth, mock_verify_access_token):
        response = client.put('/api/users/activate/Tester1', headers={'token':"ValidToken"}, params={"username": "Tester1"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.text, 'There is no account with username: Tester1')
        mock_admin_auth.assert_called_once_with({"key": {"username": "Tester1"}})
        mock_exists.assert_called_once_with("Tester1")
        mock_verify_access_token.assert_called_once_with("ValidToken")

    @patch('routers.api.users.verify_access_token', return_value = {"key": {"username": "Tester1"}} )
    @patch('routers.api.users.admin_auth', return_value = True)
    @patch('routers.api.users.exists', return_value = "Tester1")
    @patch('routers.api.users.activate', return_value = 1)
    def test_activate_user_returns_successfull_when_account_activated(self, mock_activate, mock_exists, mock_admin_auth, mock_verify_access_token):
        response = client.put('/api/users/activate/Tester1', headers={'token':"ValidToken"}, params={"username": "Tester1"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, 'Tester1 is activated.')
        mock_admin_auth.assert_called_once_with({"key": {"username": "Tester1"}})
        mock_exists.assert_called_once_with("Tester1")
        mock_verify_access_token.assert_called_once_with("ValidToken")
        mock_activate.assert_called_once_with("Tester1")

    @patch('routers.api.users.verify_access_token', return_value = {"key": {"username": "Tester1"}} )
    @patch('routers.api.users.admin_auth', return_value = True)
    @patch('routers.api.users.exists', return_value = "Tester1")
    @patch('routers.api.users.activate', return_value = 0)
    def test_activate_user_returns_successfull_when_account_already_deactivated(self, mock_activate, mock_exists, mock_admin_auth, mock_verify_access_token):
        response = client.put('/api/users/activate/Tester1', headers={'token':"ValidToken"}, params={"username": "Tester1"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, 'Tester1 is already activated.')
        mock_admin_auth.assert_called_once_with({"key": {"username": "Tester1"}})
        mock_exists.assert_called_once_with("Tester1")
        mock_verify_access_token.assert_called_once_with("ValidToken")
        mock_activate.assert_called_once_with("Tester1")


class PromoteUser_Should(unittest.TestCase):

    @patch('routers.api.users.verify_access_token', return_value = {"key": {"username": "Tester1"}})
    @patch('routers.api.users.admin_auth', return_value = True)
    @patch('routers.api.users.exists', return_value = None)
    def test_promote_user_returns_400_when_invalid_username(self, mock_exists, mock_admin_auth, mock_verify_access_token):
        response = client.put('/api/users/promote/Tester1', headers={'token':"ValidToken"}, params={"username": "Tester1"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.text, 'There is no account with username: Tester1')
        mock_admin_auth.assert_called_once_with({"key": {"username": "Tester1"}})
        mock_exists.assert_called_once_with("Tester1")
        mock_verify_access_token.assert_called_once_with("ValidToken")

    @patch('routers.api.users.verify_access_token', return_value = {"key": {"username": "Tester1"}} )
    @patch('routers.api.users.admin_auth', return_value = True)
    @patch('routers.api.users.exists', return_value = "Tester1")
    @patch('routers.api.users.promote', return_value = 1)
    def test_promote_user_returns_successfull_when_user_promoted(self, mock_promote, mock_exists, mock_admin_auth, mock_verify_access_token):
        response = client.put('/api/users/promote/Tester1', headers={'token':"ValidToken"}, params={"username": "Tester1"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, 'Tester1 is now Admin.')
        mock_admin_auth.assert_called_once_with({"key": {"username": "Tester1"}})
        mock_exists.assert_called_once_with("Tester1")
        mock_verify_access_token.assert_called_once_with("ValidToken")
        mock_promote.assert_called_once_with("Tester1")

    @patch('routers.api.users.verify_access_token', return_value = {"key": {"username": "Tester1"}} )
    @patch('routers.api.users.admin_auth', return_value = True)
    @patch('routers.api.users.exists', return_value = "Tester1")
    @patch('routers.api.users.promote', return_value = 0)
    def test_promote_user_returns_successfull_when_user_already_admin(self, mock_promote, mock_exists, mock_admin_auth, mock_verify_access_token):
        response = client.put('/api/users/promote/Tester1', headers={'token':"ValidToken"}, params={"username": "Tester1"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, 'Tester1 is already Admin.')
        mock_admin_auth.assert_called_once_with({"key": {"username": "Tester1"}})
        mock_exists.assert_called_once_with("Tester1")
        mock_verify_access_token.assert_called_once_with("ValidToken")
        mock_promote.assert_called_once_with("Tester1")


class GiveUserCategoryAccess_Should(unittest.TestCase):

    @patch('routers.api.users.verify_access_token', return_value = {"key": {"username": "Tester1"}} )
    @patch('routers.api.users.admin_auth', return_value = True)
    @patch('routers.api.users.give_access', return_value = True)
    def test_give_user_category_access_returns_201_when_access_granted(self, mock_give_access, mock_admin_auth, mock_verify_access_token):
        response = client.put('/api/users/read_access/1/category/1', headers={'token':"ValidToken"}, params={"id": 1, "category_id": 1})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.text, 'User 1 has access to category 1')
        mock_admin_auth.assert_called_once_with({"key": {"username": "Tester1"}})
        mock_verify_access_token.assert_called_once_with("ValidToken")
        mock_give_access.assert_called_once_with(1, 1)


class GiveUserCategoryWriteAccess_Should(unittest.TestCase):

    @patch('routers.api.users.verify_access_token', return_value = {"key": {"username": "Tester1"}} )
    @patch('routers.api.users.admin_auth', return_value = True)
    @patch('routers.api.users.update_write_access', return_value = True)
    def test_give_user_category_write_access_return_200_when_permision_granted(self, mock_update_writer_access, mock_admin_auth, mock_verify_access_token):
        response = client.put('/api/users/write_access/1/category/1', headers={'token':"ValidToken"}, params={"id": 1, "category_id": 1}, content='true')
        self.assertEqual(response.status_code, 200)
        mock_admin_auth.assert_called_once_with({"key": {"username": "Tester1"}})
        mock_verify_access_token.assert_called_once_with("ValidToken")
        mock_update_writer_access.assert_called_once_with(1, 1, True)

    @patch('routers.api.users.verify_access_token', return_value = {"key": {"username": "Tester1"}} )
    @patch('routers.api.users.admin_auth', return_value = True)
    @patch('routers.api.users.update_write_access', return_value = True)
    def test_give_user_category_write_access_return_200_when_permision_cancelled(self, mock_update_writer_access, mock_admin_auth, mock_verify_access_token):
        response = client.put('/api/users/write_access/1/category/1', headers={'token':"ValidToken"}, params={"id": 1, "category_id": 1}, content='false')
        self.assertEqual(response.status_code, 200)
        mock_admin_auth.assert_called_once_with({"key": {"username": "Tester1"}})
        mock_verify_access_token.assert_called_once_with("ValidToken")
        mock_update_writer_access.assert_called_once_with(1, 1, False)


class DeleteUserCategoryAccess_Should(unittest.TestCase):

    @patch('routers.api.users.verify_access_token', return_value = {"key": {"username": "Tester1"}} )
    @patch('routers.api.users.admin_auth', return_value = True)
    @patch('routers.api.users.revoke_access', return_value = True)
    def test_delete_user_category_access_returns_201_when_access_cancelled(self, mock_revoke_access, mock_admin_auth, mock_verify_access_token):
        response = client.delete('/api/users/access/1/category/1', headers={'token':"ValidToken"}, params={"id": 1, "category_id": 1})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.text, 'User 1 has no access to category 1')
        mock_admin_auth.assert_called_once_with({"key": {"username": "Tester1"}})
        mock_verify_access_token.assert_called_once_with("ValidToken")
        mock_revoke_access.assert_called_once_with(1, 1)


class GetPrivilegedUsers_Should(unittest.TestCase):

    @patch('routers.api.users.verify_access_token', return_value = {"key": {"username": "Tester1"}} )
    @patch('routers.api.users.admin_auth', return_value = True)
    @patch('routers.api.users.view_privileged_users', return_value = [("username1", True), ("username2", False)] )
    def test_get_pribileged_users_returns_200_list_of_users(self, mock_view_privileged_users, mock_admin_auth, mock_verify_access_token):
        expected_result = [
    {"username": "username1", "can_write": True},
    {"username": "username2", "can_write": False}
    ]
        response = client.get('/api/users/access/1', headers={'token':"ValidToken"}, params={"category_id": 1})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected_result)
        mock_admin_auth.assert_called_once_with({"key": {"username": "Tester1"}})
        mock_verify_access_token.assert_called_once_with("ValidToken")
        mock_view_privileged_users.assert_called_once_with(1)