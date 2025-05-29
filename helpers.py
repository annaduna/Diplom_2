from faker import Faker

from data import ErrorMessages

fake = Faker()

def generate_user():
    return {
        "email": "test"+ fake.email(),
        "password": fake.password(length=8),
        "name": fake.name()
    }

def generate_email():
    return "test2"+ fake.email()

def validate_order_keys(orders):
    for order in orders:
        assert "ingredients" in order, "Ошибка: заказ должен содержать 'ingredients'"
        assert "status" in order, "Ошибка: заказ должен содержать 'status'"
        assert "number" in order, "Ошибка: заказ должен содержать 'number'"
        assert "createdAt" in order, "Ошибка: заказ должен содержать 'createdAt'"
        assert "updatedAt" in order, "Ошибка: заказ должен содержать 'updatedAt'"

def validate_order_response(response_data, code):
    assert response_data['success'] is False, "'success' должно быть False"
    if code == 400:
        assert response_data['message'] == ErrorMessages.INGREDIENT_IDS_MUST_BE_PROVIDED, "Сообщение об ошибке неверное"
    elif code == 500:
        assert 'message' in response_data, "Ответ не содержит поле 'message'"
