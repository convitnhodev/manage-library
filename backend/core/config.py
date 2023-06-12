import os 
from pathlib import Path
from dotenv import load_dotenv

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)



class Settings: 
    PROJECT_TITLE: str = "Project Title"
    PROJECT_VERSION: str = "0.0.1"

    SECRET_KEY: str = "convitnhodev"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRATION_EXPIRE = 30 


    
    MYSQL_USER: str = os.getenv("MYSQL_USER")
    MYSQL_PASSWORD: str = os.getenv("MYSQL_PASSWORD")
    MYSQL_SERVER: str = os.getenv("MYSQL_SERVER")
    MYSQL_POST: str = os.getenv("MYSQL_POST", 3306)
    MYSQL_DB = os.getenv("MYSQL_DB")
    
    
    
    DATABASE_URL = f"mysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_SERVER}:{MYSQL_POST}/{MYSQL_DB}"


settings = Settings()