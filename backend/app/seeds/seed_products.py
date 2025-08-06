from faker import Faker
from app.models import Product
from app.seeds.db_connect import session

fake = Faker()

def create_products(num: int):
    for x in range(num):
        new_product = Product(name=fake.name(), price=fake.random_int(min=1, max=15))
        session.add(new_product)
        session.commit()


if __name__ == "__main__":
    create_products(30)
