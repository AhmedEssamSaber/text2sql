from app.core.database import SessionLocal
from app.createdb import Customer, Product, Category, Order, OrderItem
from datetime import date


def seed_data():
    session = SessionLocal()

    try:
        # Categories
        cat1 = Category(name="Electronics")
        cat2 = Category(name="Clothing")

        session.add_all([cat1, cat2])
        session.commit()

        # Customers
        c1 = Customer(
            name="Ahmed",
            email="ahmed@test.com",
            country="Egypt"
        )
        c2 = Customer(
            name="Sara",
            email="sara@test.com",
            country="UAE"
        )

        session.add_all([c1, c2])
        session.commit()

        # Products
        p1 = Product(
            name="Laptop",
            price=1000,
            category_id=cat1.id
        )
        p2 = Product(
            name="T-Shirt",
            price=50,
            category_id=cat2.id
        )

        session.add_all([p1, p2])
        session.commit()

        # Orders
        o1 = Order(
            customer_id=c1.id,
            status="completed",
            total_amount=1000,
            order_date=date(2024, 1, 10)
        )

        o2 = Order(
            customer_id=c2.id,
            status="pending",
            total_amount=50,
            order_date=date(2024, 2, 15)
        )

        session.add_all([o1, o2])
        session.commit()

        # Order Items
        oi1 = OrderItem(
            order_id=o1.id,
            product_id=p1.id,
            quantity=1,
            price=1000
        )

        oi2 = OrderItem(
            order_id=o2.id,
            product_id=p2.id,
            quantity=1,
            price=50
        )

        session.add_all([oi1, oi2])
        session.commit()

        print(" Data inserted successfully!")

    except Exception as e:
        session.rollback()
        print(" Error:", e)

    finally:
        session.close()


if __name__ == "__main__":
    seed_data()