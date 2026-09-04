from fastapi import APIRouter

from database.connection import get_connection

from pydantic import BaseModel

router = APIRouter(prefix="/signup", tags=["Create User"])




