import os 

class Config():
    # Secret key is used to store the sessions and being able to have the data stored without not being able to being taken
    # If a person has the secret key, then they can access to the information
    SECRET_KEY = os.environ.get('SECRET_KEY') or "you-will-never-guess-muajajaja"

    # This is saying that if a person logs out, the session is going to finish
    SESSION_PERMANENT = False

    # This part is saying that it is grabbing the files from the filesystem of the database
    SESSION_TYPE = "filesystem"

    # Takes the database url to make the connection
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL") or "postgres://idddlpqpcgljyx:6281d126fbb94c36fa60991b8f973246e5db0053cff1313d7f207a55c09a7412@ec2-52-206-15-227.compute-1.amazonaws.com:5432/dcbo59m4pm4894"

    # It says that it will not track each change the data has been through
    SQLALCHEMY_TRACK_MODIFICATIONS = False
