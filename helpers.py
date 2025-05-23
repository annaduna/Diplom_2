from faker import Faker

fake = Faker()

def generate_user():
    return {
        "email": "test"+ fake.email(),
        "password": fake.password(length=8),
        "name": fake.name()
    }

def generate_email():
    return "test2"+ fake.email()
