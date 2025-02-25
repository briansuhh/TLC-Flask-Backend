from api import create_app  # Import the create_app function from the api module
from dotenv import load_dotenv  # Import the load_dotenv function from the dotenv module
from api.models import *  # Import everything from the api.models module
import os  # Import the os module for interacting with the operating system

os.environ["PYTHONDONTWRITEBYTECODE"] = "1"  # Set an environment variable to prevent Python from writing .pyc files

load_dotenv()  # Load environment variables from a .env file

app = create_app()  # Create an instance of the Flask application

if __name__ == "__main__":  # Check if the script is being run directly
    app.run(port=5001)  # Run the Flask application on port 5001
