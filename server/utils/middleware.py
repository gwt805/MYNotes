from crud.user import db_user_isexist
from utils.token import decode_access_token
from jose import JWTError, ExpiredSignatureError

async def request_before(token: str):
    try:
        payload = await decode_access_token(token)
        if not await db_user_isexist(payload['username']):
            return False, {"code": -2, "status": "error", "msg": "用户身份异常"}
        else:
            return True, {"code": -2, "status": "error", "msg": "用户身份异常"}
    except ExpiredSignatureError:
        return False, {"code": -2, "status": "error", "msg": "用户身份过期"}
    except JWTError:
        return False, {"code": -2, "status": "error", "msg": "异常Token"}