from fastapi import APIRouter, Depends, HTTPException, status

from app.user.user_model import User
from app.user.user_request import UserRequest
from app.user.user_response import UserResponse
from app.user.user_service import UserService
from app.config import Container

from dependency_injector.wiring import inject, Provide

from passlib.hash import bcrypt

import uuid
import jwt


SECRET = 'my_secret'
router = APIRouter(prefix='/users', tags=["UserService"])


async def try_authenticate(user_request: UserRequest):
    try:
        user = await User.get(username=user_request.username)
        if not user:
            return False

        if not user.verify_password(user_request.password):
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail= 'Not found') 
        return user
    except:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail= 'Not found')
    

async def get_user(token:str) -> User:
    try:
        payload = jwt.decode(token, SECRET, algorithms=['HS256'])
        uuid=payload.get('uuid')
        user = await User.get(uuid=uuid)
        return user
    except:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail= 'Not authorized')
    
async def check_user(username:str, password: str):
 
    try:
        user = await User.get(username=username)
        if user:
            raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail= 'Already exists')
    except:
        return UserRequest(username= username, password= password)



@router.post('/authorize')
async def authorize_user(user_request: UserRequest):
    user = await try_authenticate(user_request)
    payload = {
        "uuid":user.uuid.__str__()
    }

    token = jwt.encode(payload, SECRET)
    
    return {
        'access-token': token
    }
    
@router.post('/me')
@inject
async def get_current_user(token:str, service: UserService = Depends(Provide[Container.user_service])):
    user = await service.get_user_by_token(token)
    return UserResponse(uuid= user.uuid.__str__(), username= user.username)


@router.post('')
async def create_user(user_request: UserRequest = Depends(check_user)):
    password_hash = bcrypt.hash(user_request.password)
    user_uuid = str(uuid.uuid4())
    user = User(username=user_request.username, 
                password=password_hash, 
                uuid=user_uuid)
    await user.save()
    return UserResponse(username=user.username,
                        uuid=user.uuid.__str__())