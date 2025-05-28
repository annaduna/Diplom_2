import pytest
from helpers import generate_user
from methods import UserMethods

@pytest.fixture
def create_user():
    create_user_new = generate_user()
    response = UserMethods.create_user(create_user_new)
    user_token = response.json().get('accessToken')
    yield create_user_new, user_token
    UserMethods.delete_user(user_token)

