from fastapi import APIRouter, status, Response, Request
from schemas import *
from services import Product

router = APIRouter(tags=["Product"], prefix="/product")

