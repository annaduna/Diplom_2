import pytest
import requests
import helpers
from curl import url
from data import DataForUser, Responses
from helpers import generate_user
from methods import UserMethods
import allure

class TestCreateUser:
    @allure.title('Регистрация нового пользователя.')
    def test_create_new_user(self, create_user):
        user_data, user_token = create_user
        assert user_token is not None, "Ошибка: пользователь не создался"

    @allure.title('Регистрация двух одинаковых пользователей.')
    def test_create_two_same_users(self,create_user):
        user_data, user_token = create_user
        response = UserMethods.create_user(user_data)
        assert response.status_code == 403 and response.json() == Responses.CODE_403_CREATE_SAME_USER

    @allure.title("Тест проверяет, что запрос без обязательного поля возвращает ошибку  403.")
    def test_create_courier_without_login(self):
        user_data = generate_user()
        user_data.pop("email")
        response = UserMethods.create_user(user_data)
        assert response.status_code == 403
        response_json = response.json()
        assert response.status_code == 403 and response.json() == Responses.CODE_403_CREATE_USER_EMPTY_LOGIN

class TestLoginUser:
    @allure.title('Авторизация зарегистрированного пользователя с помощью email и пароля.')
    def test_login_user(self, create_user):
        user_data, user_token = create_user
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
        assert login_response.status_code == 401 and login_response.json() == Responses.CODE_401_LOGIN_USER

class TestUpdateUser:

    @allure.title("Изменение данных пользователя c авторизацией")
    @pytest.mark.parametrize("param", [{"email": helpers.generate_email()},
                                       {"name": "nikirtata"}])
    def test_update_auth_user(self, param):
        user_data = generate_user()
        response_new_user = UserMethods.create_user(user_data)
        user_token = response_new_user.json().get('accessToken')
        response = requests.patch(url.PATCH_UPDATE_USER, data=param, headers = {"Authorization": user_token})
        assert response.status_code == 200 and response.json()['success'] == True



    @allure.title("Изменение данных пользователя без авторизацией")
    @pytest.mark.parametrize("param", [{"email": helpers.generate_email()},
                                        {"name": "tanya"}])
    def test_update_no_authorized_user(self, param):
        response = requests.patch(url.PATCH_UPDATE_USER, data=param)
        assert response.status_code == 401 and response.json() == Responses.CODE_401_UPDATE_USER_NO_AUTH


