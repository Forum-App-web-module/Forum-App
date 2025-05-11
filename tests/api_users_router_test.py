from unittest.mock import Mock, patch
import unittest
from fastapi.testclient import TestClient
from main import app




# @user_router.get('/')
# # Searches user profile by filters: Username and role.
# #  2 options: 1 search by username and role. 2 Search all admins.
# def search_user(username: Optional[str]="", is_admin: Optional[str] = "False", token: str = Header()):
#     # token authentication
#     verify_access_token(token)
    
#     if not username and is_admin.lower() == "false":
#         return BadRequest(content = "Please select at least one search parameters.")

#     users_list = get_users(username, is_admin)

#     return users_list


client = TestClient(app)
class Search_users_Should(unittest.TestCase):

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
