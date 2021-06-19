from discord import User


def user_name(user: User) -> str:
    return user.nick if user.nick else user.name
