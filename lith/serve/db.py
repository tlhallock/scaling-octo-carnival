#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Optional
import motor.motor_asyncio
from fastapi import FastAPI, Request, Depends
from fastapi_users import FastAPIUsers, models
from fastapi_users.db import MongoDBUserDatabase
from fastapi_users.authentication import CookieAuthentication, JWTAuthentication

from motor.motor_asyncio import AsyncIOMotorCollection


# --- MongoDB Setup -----------------------------------------------------------

# MongoDB Configurations
DATABASE_URL = "mongodb://localhost:27017"
client = motor.motor_asyncio.AsyncIOMotorClient(
  DATABASE_URL, uuidRepresentation="standard"
)
# MongoDB database instance ("DB" by default, can be changed)
database = client["DB"]

class Collections:
  users: AsyncIOMotorCollection = database["users"]
  lobbies: AsyncIOMotorCollection = database["lobbies"]

