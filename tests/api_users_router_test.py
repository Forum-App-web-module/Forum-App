from unittest.mock import Mock, patch
import unittest
from fastapi.testclient import TestClient
from main import app
from mariadb import IntegrityError
from fastapi import HTTPException

client = TestClient(app)


class Search_users_Should(unittest.TestCase):

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

    # @user_router.post('/register', status_code=201)
# # Creates user profile
# def register(data: RegisterData):
#     try: new_id = create(data.username, data.email, hash_password(data.password))
#     except IntegrityError as integ:
#         return BadRequest(content = "Invalid input - {integ}")

#     return Created(content = f"Account with username {data.username} created successfully")

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

# @user_router.post('/login')
# def login(login: LoginData):

#     user = try_login(login.username, hash_password(login.password))

#     if user: 
#         return create_access_token(user)
#     else: return BadRequest(content = "Invalid login data")

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


class Get_Profile_Should(unittest.TestCase):

# @user_router.get('/{username}')
# # Returns User profile information
# def get_profile(username: str, token: str = Header()):

#     # token authentication
#     verify_access_token(token)
    
#     user_information = find_user_by_username(username)
#     if not user_information:
#         return BadRequest(content = f'There is no account with username: {username}')
#     else: 
#         return user_information

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


class Update_Profile_Bio_Should(unittest.TestCase):

    # @user_router.put('/bio')
    # # Update user bio BY the user.
    # def update_profile_bio(bio: str = Body(..., min_length=1, max_length=150), token: str = Header()):

    #     # token authentication
    #     payload = verify_access_token(token)
        
    #     result = update_bio(payload["key"]["username"], bio)

    #     # following is mariadb validation error. No need to proceed if Body validation error above.
    #     # except DataError as dat:
    #     #     return JSONResponse (status_code=400, content= {"message": f"Invalid input - {dat} , max lenght is 150 characters."})
        
    #     if result:
    #         return Successful(content= f"Bio is updated")
    

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










# @user_router.put('/deactivate/{username}')
# # Deactivation(block) of account BY ADMIN
# def deactivate_user(username: str, token: str = Header()):

#     # token authentication
#     payload = verify_access_token(token)

#     #  ADMIN authorization
#     admin_auth(payload)

#     if not exists(username):
#         return BadRequest(content = f'There is no account with username: {username}')

#     result = deactivate(username)
#     if result:
#         return Successful(content = f"{username} is now blocked.")

#     else: return Successful(content = f'{username} already has been blocked.')

# @user_router.put('/activate/{username}')
# # Activation(Unblock) account BY ADMIN
# def activate_user(username: str, token: str = Header()):

#     # token authentication
#     payload = verify_access_token(token)

#     #  ADMIN authorization
#     admin_auth(payload)

# #  requires ADMIN authorization
#     if not exists(username):
#         return BadRequest(content = f'There is no account with username: {username}')

#     result = activate(username)
#     if result:
#         return Successful(content = f"{username} is activated.")

#     else: return Successful(content = f'{username} is already activated.')


# @user_router.put('/promote/{username}')
# # Promote user into admin.
# def promote_user(username: str, token: str = Header()):
    
#      # token authentication
#     payload = verify_access_token(token)

#     #  ADMIN authorization
#     admin_auth(payload)

#     if not exists(username):
#         return BadRequest(content = f'There is no account with username: {username}')
    
#     result = promote(username)
#     if result:Successful(content = f"{username} is now Admin.")

#     else: return Successful(content = f'{username} is already Admin.')


# # Give User Category read access
# @user_router.put('/read_access/{id}/category/{category_id}')
# def give_user_category_access(id: int, category_id: int, token: str = Header()):
#     payload = verify_access_token(token)

#     # Admin authorization returns an error or None
#     if admin_auth(payload):
#         # call service
#         give_access(id, category_id)
#         return Created(content=f'User {id} has access to category {category_id}')


# # Give User a Category Write Access
# @user_router.put('/write_access/{id}/category/{category_id}')
# def give_user_category_write_access(id: int, category_id: int, token: str = Header()):
#     payload = verify_access_token(token)

#     # Admin authorization returns an error or None
#     if admin_auth(payload):
#         # call service
#         update_write_access(id, category_id, True)
#         return Created(content=f'User {id} has write access to category {category_id}')


# # Revoke User Access
# @user_router.delete('/access/{id}/category/{category_id}')
# def delete_user_category_access(id: int, category_id: int, token: str = Header()):
#     payload = verify_access_token(token)

#     # Admin authorization returns an error or None
#     if admin_auth(payload):
#         # call service
#         revoke_access(id, category_id)
#         return Created(content=f'User {id} has no access to category {category_id}')


# # View Privileged Users
# @user_router.get('/access/{category_id}')
# def get_privileged_users(category_id: int, token: str = Header()):
#     payload = verify_access_token(token)

#     # Admin authorization returns an error or None
#     if admin_auth(payload):
#         # call service
#         service_response = view_privileged_users(category_id)[0]
#         return [PrivilegedUsersResponse.from_query_result(row) for row in service_response]