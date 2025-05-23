import pytest
from data import Ingredients
from helpers import generate_user
from methods import OrderMethods, UserMethods
import allure

class TestCreateOrder:
    @allure.title('Создание заказа c авторизациeй и с с ингредиентами')
    def test_create_order_auth_user(self):
        user_data = generate_user()
        response_new_user = UserMethods.create_user(user_data)
        user_token = response_new_user.json().get('accessToken')
        ingredients = [Ingredients.bun, Ingredients.main, Ingredients.sauce]
        order = OrderMethods.create_order(ingredients,user_token)
        assert order.status_code == 200 and order.json()['success'] == True

    @allure.title('Создание заказа без авторизации.')
    def test_create_new_order_no_authorization(self):
        ingredients = [Ingredients.bun, Ingredients.main, Ingredients.sauce]
        order = OrderMethods.create_order(ingredients)
        assert order.status_code != 200 and order.json()['success'] != True

    @allure.title('Создание заказа с авторизацией без ингредиентов и с неверным хешем ингредиентов')
    @pytest.mark.parametrize("ingredients, code", [([], 400), (["61c0c5a7"], 500)])
    def test_create_new_order_invalid_ingredients(self, ingredients, code):
        user_data = generate_user()
        response = UserMethods.create_user(user_data)
        assert response.status_code == 200, "пользователь не создан"
        user_token = response.json().get('accessToken')
        login_response = UserMethods.post_login_user({
            "email": user_data["email"],
            "password": user_data["password"]

        })
        order = OrderMethods.create_order(ingredients, user_token)
        assert order.status_code == code

class TestGetOrder:

    @allure.title('Получение заказов пользователя без авторизации.')
    def test_get_user_orders_with_authorization(self):
        orders = OrderMethods.request_user_orders_list()
        assert orders.status_code == 401 and orders.json("message") == "You should be authorised"

    @allure.title('Получение заказов пользователя c авторизацией.')
    def test_get_user_orders_with_authorization(self):
       user_data = generate_user()
       response = UserMethods.create_user(user_data)
       assert response.status_code == 200, "пользователь не создан"
       user_token = response.json().get('accessToken')
       login_response = UserMethods.post_login_user({
           "email": user_data["email"],
           "password": user_data["password"]

       })
       ingredients = [Ingredients.bun, Ingredients.main, Ingredients.sauce]
       order = OrderMethods.create_order(ingredients, user_token)
       assert order.status_code == 200 and order.json()['success'] == True
       orders = OrderMethods.request_user_orders_list(user_token)
       assert orders.status_code == 200
