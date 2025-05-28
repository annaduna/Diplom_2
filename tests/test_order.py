import pytest
from data import Ingredients, Responses
from helpers import generate_user
from methods import OrderMethods, UserMethods
import allure

class TestCreateOrder:
    @allure.title('Создание заказа c авторизациeй и с с ингредиентами')
    def test_create_order_auth_user(self,create_user):
        user_data, user_token = create_user
        ingredients = [Ingredients.bun, Ingredients.main, Ingredients.sauce]
        order = OrderMethods.create_order(ingredients,user_token)
        assert order.status_code == 200

    @allure.title('Создание заказа без авторизации.')
    def test_create_new_order_no_authorization(self):
        ingredients = [Ingredients.bun, Ingredients.main, Ingredients.sauce]
        order = OrderMethods.create_order(ingredients)
        assert order.status_code == 401 and order.json()['success'] == False

    @allure.title('Создание заказа с авторизацией без ингредиентов и с неверным хешем ингредиентов')
    @pytest.mark.parametrize("ingredients, code", [([], 400), (["61c0c5a7"], 500)])
    def test_create_new_order_invalid_ingredients(self,create_user, ingredients, code):
        user_data, user_token = create_user
        order = OrderMethods.create_order(ingredients, user_token)
        assert order.status_code == code

class TestGetOrder:

    @allure.title('Получение заказов пользователя без авторизации.')
    def test_get_user_orders_with_authorization(self):
        orders = OrderMethods.request_user_orders_list()
        assert orders.status_code == 401 and orders.json() == Responses.CODE_401_GET_ORDERS_NO_AUTH

    @allure.title('Получение заказов пользователя c авторизацией.')
    def test_get_user_orders_with_authorization(self,create_user):
       user_data, user_token = create_user

       ingredients = [Ingredients.bun, Ingredients.main, Ingredients.sauce]
       order = OrderMethods.create_order(ingredients, user_token)
       assert order.status_code == 200 and order.json()['success'] == True

       orders = OrderMethods.request_user_orders_list(user_token)
       assert orders.status_code == 200
       response_json = orders.json()

       assert response_json.get("success") is True, "Ошибка: 'success' должен быть True"
       assert "orders" in response_json, "Ошибка: в ответе нет поля 'orders'"

       # Проверяем, что список заказов не пустой
       assert isinstance(response_json["orders"], list), "Ошибка: 'orders' должен быть списком"
       assert len(response_json["orders"]) > 0, "Ошибка: у пользователя нет заказов"

       # Проверяем наличие ключей внутри заказов
       for order in response_json["orders"]:
           assert "ingredients" in order, "Ошибка: заказ должен содержать 'ingredients'"
           assert "status" in order, "Ошибка: заказ должен содержать 'status'"
           assert "number" in order, "Ошибка: заказ должен содержать 'number'"
           assert "createdAt" in order, "Ошибка: заказ должен содержать 'createdAt'"
           assert "updatedAt" in order, "Ошибка: заказ должен содержать 'updatedAt'"
