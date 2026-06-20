import csv
import os

from app.db.session import SessionLocal, engine
from app.db.base import Base
from app.models.apartment import Apartment


def seed():
    # Create tables (safe for dev)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        # Prevent duplicate seeding
        if db.query(Apartment).first():
            print("Database already seeded 🚀")
            return

        # Resolve project root safely
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        csv_path = os.path.join(BASE_DIR, "data", "apartments.csv")

        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"CSV not found at: {csv_path}")

        with open(csv_path, "r") as file:
            reader = csv.DictReader(file)

            for row in reader:
                apt = Apartment(
                    id=int(row["id"]),
                    name=row["name"],
                    price=int(row["price"]),
                    bedrooms=int(row["bedrooms"]),
                    bathrooms=int(row["bathrooms"]),
                    city=row["city"],
                    pool=row["pool"],
                    gym=row["gym"],
                    parking=row["parking"],
                    pet_friendly=row["pet_friendly"],
                )
                db.add(apt)

            db.commit()

        print("Database seeded successfully 🚀")

    finally:
        db.close()


if __name__ == "__main__":
    seed()