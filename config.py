import os
from dotenv import load_dotenv

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    
    # Stripe configuration
    STRIPE_PUBLIC_KEY = 'pk_test_51RE9llHDZIJX5EM3ToAQPol1o6JmP5h6bOuV4lhnpazN2WBdWo8z8tfb6DySQqNy4J6seuIGeQeB1t4agPNj941c002VNUuDc6'
    STRIPE_SECRET_KEY = 'sk_test_51RE9llHDZIJX5EM30uzaoJfp8azX89CcXzymSNbU1P6R6dvXWFdom2TiyFnQKcuy2GVmTiOu993pJbqdT4RVvNbq00ncQyqL0Z'
    STRIPE_CURRENCY = 'egp'
    STRIPE_ENDPOINT_SECRET = os.environ.get('STRIPE_ENDPOINT_SECRET')