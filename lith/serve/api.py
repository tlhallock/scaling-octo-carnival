#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from fastapi import FastAPI, Depends
import serve.routes.users as user_routes
from fastapi.middleware.cors import CORSMiddleware
import serve.routes.lobbies as lobby_routes 



# --- FastAPI Server Initialization -------------------------------------------

# Learn more https://frankie567.github.io/fastapi-users/configuration/routers/

# Initiating FastAPI Server
app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)



app.include_router(
    user_routes.auth,
    prefix="/auth",
    tags=["auth"]
)
app.include_router(
    user_routes.register,
    prefix="/auth",
    tags=["auth"]
)

app.include_router(
    user_routes.users,
    prefix="/auth/users",
    tags=["auth"]
)
app.include_router(
    user_routes.reset,
    prefix="/auth/users",
    tags=["auth"]
)



app.include_router(
    lobby_routes.router,
    prefix="",
    tags=["lobbies"]
)
