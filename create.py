from initapp import app
from models import *

# This file is the one that has to be run everytime we want to create a new database
# it is important to try if it changes the ones we already have


db.init_app(app)

def main():
    db.create_all()

if __name__ == "__main__":
    # Flask has particular rules when we interact with the application
    # We need this code in order to interact in the command line with our flask application
    with app.app_context(): 
        main()