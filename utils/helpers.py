from config import OWNER_ID
from database import get_sudos

async def is_owner(user_id: int):
    return user_id == OWNER_ID

async def is_sudo(user_id: int):
    sudos = await get_sudos()
    return user_id in sudos or await is_owner(user_id)
