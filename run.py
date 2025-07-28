# ~/inventory_service/run.py
import os
from dotenv import load_dotenv
from app import create_app

# Load environment variables from .env file (for local dev, not for Docker, but harmless)
load_dotenv()

# This is the part that Gunicorn will call directly:
app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
