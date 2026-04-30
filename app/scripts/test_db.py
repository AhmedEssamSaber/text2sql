from app.core.database import SessionLocal
from app.db_models import Customer

def main():
    session = SessionLocal()

    users = session.query(Customer).all()
    print(users)

if __name__ == "__main__":
    main()
    
    