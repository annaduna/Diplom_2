import pytest
import requests
import helpers
from curl import url
from data import DataForUser
from helpers import generate_user
from methods import UserMethods
import allure

class TestCreateUser:
    @allure.title('Регистрация нового пользователя.')
    def test_create_new_user(self):
        user_data = generate_user()
        response = UserMethods.create_user(user_data)
        assert response.status_code == 200 and response.json()['success'] == True

    @allure.title('Регистрация двух одинаковых пользователей.')
    def test_create_two_same_users(self):
        response = UserMethods.create_user(DataForUser.CREATE_USER)
        assert response.status_code == 200 and response.json()['success'] == True
        second_response = UserMethods.create_user(DataForUser.CREATE_USER)
        assert second_response.status_code == 403 and second_response.json()['success'] == False

    @allure.title("Тест проверяет, что запрос без обязательного поля возвращает ошибку  403.")
    def test_create_courier_without_login(self):
        user_data = generate_user()
        user_data.pop("email")
        response = UserMethods.create_user(user_data)
        assert response.status_code == 403
        response_json = response.json()
        assert response_json.get("message") == "Email, password and name are required fields"

class TestLoginUser:
    @allure.title('Авторизация зарегистрированного пользователя с помощью email и пароля.')
    def test_login_user(self):
        user_data = generate_user()
        response = UserMethods.create_user(user_data)
        assert response.status_code == 200, "пользователь не создан"

        login_response = UserMethods.post_login_user({
        "email": user_data["email"],
        "password": user_data["password"]

    })
        assert login_response.status_code == 200
        assert login_response.json()['success'] == True

    @allure.title('Авторизация зарегистрированного пользователя с с неверным логином/паролем.')
    def test_courier_login_invalid_credentials(self):
        login_data = {
            "email": 'nikitа@yandex.ru',
            "password": "123653"
        }
        login_response = UserMethods.post_login_user(login_data)
        assert login_response.status_code == 401
        assert login_response.json().get("message") == "email or password are incorrect"

class TestUpdateUser:

    @allure.title("Изменение данных пользователя c авторизацией")
    @pytest.mark.parametrize("param", [{"email": helpers.generate_email()},
                                       {"name": "nikirtata"}])
    def test_update_auth_user(self, param):
        user_data = generate_user()
        response_new_user = UserMethods.create_user(user_data)
        # print(response_new_user.json())
        user_token = response_new_user.json().get('accessToken')
        response = requests.patch(url.PATCH_UPDATE_USER, data=param, headers = {"Authorization": user_token})
        assert response.status_code == 200 and response.json()['success'] == True



    @allure.title("Изменение данных пользователя без авторизацией")
    @pytest.mark.parametrize("param", [{"email": helpers.generate_email()},
                                        {"name": "tanya"}])
    def test_update_no_authorized_user(self, param):
        response = requests.patch(url.PATCH_UPDATE_USER, data=param)
        assert response.status_code == 401 and response.json().get("message") == "You should be authorised"


