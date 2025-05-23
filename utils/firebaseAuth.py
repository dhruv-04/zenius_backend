import firebase_admin
from firebase_admin import credetials, auth
from fastapi import Depends, Header

cred = credentials.certificate()