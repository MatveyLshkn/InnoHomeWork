import json
import requests
from sqlalchemy.orm import Session
from . import models, auth
from .database import SessionLocal

def init_db():
    db = SessionLocal()
    try:
        # Check if we already have users
        if db.query(models.User).first():
            return

        # Fetch data from JSONPlaceholder
        response = requests.get("https://jsonplaceholder.typicode.com/users")
        users_data = response.json()

        for user_data in users_data:
            # Create user with a default password
            user = models.User(
                name=user_data["name"],
                username=user_data["username"],
                email=user_data["email"],
                password_hash=auth.get_password_hash("password123"),  # Default password
                phone=user_data["phone"],
                website=user_data["website"]
            )

            # Create address
            address_data = user_data["address"]
            address = models.Address(
                street=address_data["street"],
                suite=address_data["suite"],
                city=address_data["city"],
                zipcode=address_data["zipcode"]
            )

            # Create geo
            geo_data = address_data["geo"]
            geo = models.Geo(
                lat=geo_data["lat"],
                lng=geo_data["lng"]
            )
            address.geo = geo
            user.address = address

            # Create company
            company_data = user_data["company"]
            company = models.Company(
                name=company_data["name"],
                catchPhrase=company_data["catchPhrase"],
                bs=company_data["bs"]
            )
            user.company = company

            db.add(user)

        db.commit()
    except Exception as e:
        print(f"Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_db() 