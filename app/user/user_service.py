from abc import ABC, abstractmethod
from app.user.user_request import UserRequest
from app.user.user_model import User
import jwt


class UserService(ABC):
    
    @abstractmethod
    def get_user_by_username(self, user_request:UserRequest) -> User:
        pass
    
    @abstractmethod
    def get_user_by_token(self, token:str) -> User:
        pass
    
    
class DefaultUserService(UserService):
    
    async def get_user_by_username(self, user_request: UserRequest) -> User:
        user = await User.get(username=user_request.username)

        if not user.verify_password(user_request.password):
            raise PasswordIncorrectException()
        return user
    
    
    async def get_user_by_token(self, token:str) -> User:
        payload = jwt.decode(token, 'my_secret', algorithms=['HS256'])
        uuid=payload.get('uuid')
        return await User.get(uuid=uuid)

    
class PasswordIncorrectException(Exception):
    pass