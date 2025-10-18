from .exceptions import PasswordsDontMatch, UserAlreadyExists, UserDontExists, UserRolesNotCreated, WrongPassword
from .models import LogInAnswer, LogInRequest, SignUpRequest
from src.postgre_module.repository import UserRepository, RoleRepository
from src.redis_module import RedisRepository
from src.redis_module.models import SessionData
import uuid


class UserService():
    def __init__(self,
                 user_repository: UserRepository,
                 redis_repository: RedisRepository,
                 role_repository: RoleRepository):
        self.user_repository = user_repository
        self.redis_repository = redis_repository
        self.role_repository = role_repository

    async def signup(self, data: SignUpRequest):
        if data.password != data.repeat_password:
            raise PasswordsDontMatch
        username_checking = await self.user_repository.get_by_username(data.username)
        if username_checking is not None:
            raise UserAlreadyExists
        role = await self.role_repository.get_by_name(data.role)
        if role is None:
            raise UserRolesNotCreated
        await self.user_repository.create(data.username, data.password, role)

    async def login(self, data: LogInRequest) -> LogInAnswer:
        user = await self.user_repository.get_by_username(data.username)
        if user is None:
            raise UserDontExists
        if not await self.user_repository.check_password(user, data.password):
            raise WrongPassword
        token = uuid.uuid4().hex
        permissions = await self.role_repository.get_permissions(user.role)
        permissions = list(map(lambda x: x.name, permissions))

        await self.redis_repository.set_user_cookie(token,
                                                        SessionData(
                                                            user_id=user.id,
                                                            token=token,
                                                            permissions=permissions,
                                                            role=user.role.name,
                                                            user_name=user.username
                                                        )
                                                    )
        return LogInAnswer(token, user)

    async def logout(self, session_token: str):
        await self.redis_repository.remove_user_cookie(session_token)

    async def get_user_json(self, session_token: str) -> SessionData:
        return await self.redis_repository.get_session_data_cookie(session_token)

