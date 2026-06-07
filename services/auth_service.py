from models import RegisterRequest, LoginRequest

# TODO: realize it
class AuthService:
    def __init__(self, users, redis, kafka):
        self.users
        self.redis
        self.kafka

    async def register(self, body: RegisterRequest):
        pass

    async def login(self, body: LoginRequest):
        pass