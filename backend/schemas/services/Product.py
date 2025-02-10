import os
from datetime import date
from typing import Sequence
from fastapi import UploadFile, HTTPException, status, Request
from fastapi.responses import FileResponse
from database import new_session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, delete, Select
from schemas import AddProductInform
from Function import Functions
from uuid import uuid4
import shutil



class ProductService:
    @classmethod
    async def add_inform_product(cls, request: Request, data: AddProductInform):
        pass


