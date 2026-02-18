from enum import Enum

# задаем роли пользователям, в дальнейшем можно будет расширить список ролей, если потребуется
class UserRole(str, Enum):
    user = "user"
    admin = "admin"
