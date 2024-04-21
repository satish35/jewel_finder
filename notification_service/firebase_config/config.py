import firebase_admin
from firebase_admin import credentials, DefaultCredentialsError 
from dotenv import load_dotenv
import os

load_dotenv()

def admin_init():
    try:    
        admin= firebase_admin
        cred = credentials.Certificate(os.getenv("service_account"))
        admin.initialize_app(cred)
        return admin
    except DefaultCredentialsError as cred_err:
        print(cred_err)
        return None
    except Exception as err:
        print(err)
        return None