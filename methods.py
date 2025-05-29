import allure
import requests
from curl import url

class UserMethods:
    @staticmethod
    def create_user(user_data):
        response = requests.post(url.POST_CREATE_USE, json=user_data)
        return response

    @staticmethod
    @allure.step('Метод Авторизации пользователя')
    def post_login_user(login_data):
        return requests.post(url.POST_LOGIN, json=login_data)

    @staticmethod
    @allure.step('Удаление пользователя.')
    def delete_user(token):
        return requests.delete(url.DELETE_USER, headers={"Authorization": f"{token}"})

class OrderMethods:
    @staticmethod
    @allure.step('Создание нового заказа.')
    def create_order(ingredients, token=''):
        return requests.post(url.CREATE_ORDER, json={"ingredients": ingredients}, headers={"Authorization": f"{token}"})

    @staticmethod
    @allure.step('Получение списка заказов.')
    def request_user_orders_list(token=''):
        return requests.get(url.GET_USER_ORDER_LIST, headers={"Authorization": f"{token}"})



