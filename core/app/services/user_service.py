from core.app.repositories import UserRepository
from core.models import User


class UserService:
    repository = UserRepository()

    def create(self, name: str) -> User:
        return self.repository.create(name=name)
