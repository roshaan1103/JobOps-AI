from sqlalchemy import select

from app.db.session import SessionLocal
from app.models.user import User


def seed_initial_user() -> None:
    db = SessionLocal()

    try:
        existing_user = db.scalar(
            select(User).where(
                User.email == "local@jobops.ai"
            )
        )

        if existing_user is not None:
            print("Initial user already exists.")
            return

        user = User(
            email="local@jobops.ai"
        )

        db.add(user)
        db.commit()

        print("Initial development user created.")

    finally:
        db.close()


if __name__ == "__main__":
    seed_initial_user()