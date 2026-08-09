from dotenv import load_dotenv
import os

load_dotenv()


class Settings:
    def __init__(self):
        self.SECRET_KEY = os.getenv("SECRET_KEY")
        self.ALGORITHM = os.getenv("ALGORITHM", "HS256")

        self.ACCESS_TOKEN_EXPIRE_MINUTES = int(
            os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60)
        )

        self.ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
        self.ADMIN_PASSWORD_HASH = os.getenv("ADMIN_PASSWORD_HASH")

        self.DATABASE_URL = os.getenv(
            "DATABASE_URL",
            "sqlite:///novixa.db",
        )


settings = Settings()