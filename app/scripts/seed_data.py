import random
from faker import Faker
from datetime import date, timedelta

from app.core.database import SessionLocal
from app.db_models import Customer, Product, Category, Order, OrderItem

fake = Faker()


def seed_data():
    session = SessionLocal()

    try:
        # Categories
        categories = [
            Category(name="Electronics"),
            Category(name="Clothing"),
            Category(name="Books"),
            Category(name="Home"),
        ]
        session.add_all(categories)
        session.commit()

        # Customers
        customers = []
        for _ in range(200):
            c = Customer(
                name=fake.name(),
                email=fake.email(),
                country=random.choice(["Egypt", "UAE", "USA", "Germany"])
            )
            customers.append(c)

        session.add_all(customers)
        session.commit()

        # Products
        products = []
        for _ in range(100):
            p = Product(
                name=fake.word(),
                price=random.randint(10, 2000),
                category_id=random.choice(categories).id
            )
            products.append(p)

        session.add_all(products)
        session.commit()

        # Orders + OrderItems
        for _ in range(500):
            customer = random.choice(customers)

            order = Order(
                customer_id=customer.id,
                status=random.choice(["completed", "pending", "cancelled"]),
                total_amount=0,
                order_date=date(2023, 1, 1) + timedelta(days=random.randint(0, 365))
            )

            session.add(order)
            session.commit()

            total = 0

            for _ in range(random.randint(1, 5)):
                product = random.choice(products)
                quantity = random.randint(1, 3)

                oi = OrderItem(
                    order_id=order.id,
                    product_id=product.id,
                    quantity=quantity,
                    price=product.price
                )

                total += product.price * quantity

                session.add(oi)

            order.total_amount = total
            session.commit()

        print("Large dataset inserted successfully!")

    except Exception as e:
        session.rollback()
        print("Error:", e)

    finally:
        session.close()


if __name__ == "__main__":
    seed_data()