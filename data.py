class DataForUser:
    CREATE_USER = {
        "email": 'nikitа@yandex.ru',
        "password": '123653',
        "name": 'Nikitos'
    }

class Ingredients:
    bun = "61c0c5a71d1f82001bdaaa6d"
    main = "61c0c5a71d1f82001bdaaa6f"
    sauce = "61c0c5a71d1f82001bdaaa73"

class Responses:
    CODE_403_CREATE_USER_EMPTY_LOGIN = {'message': 'Email, password and name are required fields', 'success': False}
    CODE_403_CREATE_SAME_USER = {'message': 'User already exists', 'success': False}
    CODE_401_LOGIN_USER = {'message': 'email or password are incorrect', 'success': False}
    CODE_401_UPDATE_USER_NO_AUTH = {'message': 'You should be authorised', 'success': False}
    CODE_401_GET_ORDERS_NO_AUTH = {'message': 'You should be authorised', 'success': False}

class ErrorMessages:
    INGREDIENT_IDS_MUST_BE_PROVIDED = "Ingredient ids must be provided"