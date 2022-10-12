#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Optional
import motor.motor_asyncio
from fastapi import FastAPI, Request, Depends
from fastapi_users import FastAPIUsers, models
from fastapi_users.db import MongoDBUserDatabase
from fastapi_users.authentication import CookieAuthentication, JWTAuthentication
import serve.models.users as users_model
from serve.db import Collections


# --- Authentication Method Setup ---------------------------------------------

"""
    Session duration/expiration can be changed through the lifetime_seconds
    attribute

    Learn more at https://frankie567.github.io/fastapi-users/configuration/authentication/

"""

# Secret Key (must be changed from "SECRET")
SECRET = "SECRET"

# Authentication Method JWT
auth_backends = []
authentication = JWTAuthentication(secret=SECRET, lifetime_seconds=3600)
auth_backends.append(authentication)


# --- FastAPIUsers Object Declaration -----------------------------------------

user_db = MongoDBUserDatabase(users_model.UserDB, Collections.users)


fastapi_users = FastAPIUsers(
    db=user_db,
    auth_backends=auth_backends,
    user_model=users_model.User,
    user_create_model=users_model.UserCreate,
    user_update_model=users_model.UserUpdate,
    user_db_model=users_model.UserDB
)


# Below function can be used to init any backend process like sending out a
# successful registeration email
def on_after_register(user: users_model.UserDB, request: Request):
    print(f"User {user.id} has registered.")


auth = fastapi_users.get_auth_router(backend=auth_backends[0])
register = fastapi_users.get_register_router(on_after_register)
users = fastapi_users.get_users_router()
reset = fastapi_users.get_reset_password_router("SECRET")
get_current_user = fastapi_users.get_current_user
get_optional_current_user = fastapi_users.get_optional_current_user
