import os

SECRET_KEY = os.getenv("SECRET_KEY", "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7")
ALGORITHM = "HS256"
try:
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 15))
except:
    ACCESS_TOKEN_EXPIRE_MINUTES = 15

API_KEY = os.getenv("API_KEY", "X86NOH6II01P7R24")
API_URL = os.getenv("API_URL", "https://www.alphavantage.co/query")