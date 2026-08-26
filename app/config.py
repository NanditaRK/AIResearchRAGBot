import os

# will use os.environ instead of os.getenv or os.env.get to make it throw an error
# if env variable is missing
SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = os.environ["ALGORITHM"]
SESSION_SECRET_KEY = os.environ["SESSION_SECRET_KEY"]
FRONTEND_URL = os.environ["FRONTEND_URL"]
ACCESS_TOKEN_EXPIRE_MINUTES = os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"]
S3_ENDPOINT_URL = os.getenv("S3_ENDPOINT_URL", "http://localhost:9000")
S3_ACCESS_KEY = os.getenv("S3_ACCESS_KEY", "minioadmin")
S3_SECRET_KEY = os.getenv("S3_SECRET_KEY", "minioadmin")
S3_BUCKET = os.getenv("S3_BUCKET", "research-papers")