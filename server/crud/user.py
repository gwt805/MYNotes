from loguru import logger
from datetime import datetime
from db.model import engine, User
from sqlmodel import Session, select
from utils.password import verify_password

# login
async def db_login(username: str, password: str) -> tuple:
    if not await db_user_isexist(username=username): return False, "该用户不存在"
    else:
        with Session(engine) as session:
            sql = select(User).where(User.username==username)
            res = session.exec(sql).first()
            flag = verify_password(password, res.password)
        if flag: return True, "登录成功", res
        else: return False, "密码错误", None

# register
async def db_register(username: str, password: str):
    if await db_user_isexist(username=username): return False, "该用户已存在"
    else:
        with Session(engine) as session:
            user = User(username=username, password=password)
            session.add(user)
            session.commit()
        return True, "注册成功"

# user is exist
async def db_user_isexist(username: str) -> bool:
    with Session(engine) as session:
        sql = select(User).where(User.username==username)
        res = session.exec(sql).first()
        if res: return True
        else: return False

# update password
async def db_update_pwd(id: int , pwd: str):
    with Session(engine) as session:
        user = session.get(User, id)
        user.password = pwd
        user.updated_at = datetime.now()
        session.commit()
        session.refresh(user)

# update avatar
async def db_update_avatar(id: int, avatar: str):
    with Session(engine) as session:
        user = session.get(User, id)
        user.avatar = avatar
        user.updated_at = datetime.now()
        session.commit()
        session.refresh(user)

# delete
async def db_del_data(id: int):
    with Session(engine) as session:
        user = session.get(User, id)
        session.delete(user)
        session.commit()

