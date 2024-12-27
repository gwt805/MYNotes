from loguru import logger
from datetime import datetime
from db.model import engine, Blog
from sqlmodel import Session, select, or_, func

# get single blog
def db_get_blog_single(id: int):
    with Session(engine) as session:
        sql = select(Blog).where(Blog.id==id)
        res = session.exec(sql).first()
        return res

# create blog
def db_create_blog(title: str, content: str):
    with Session(engine) as session:
        blog = Blog(title=title, content=content)
        session.add(blog)
        session.commit()
        session.refresh(blog)

# 根据每页数量和页码获取博客列表及搜索条件及总数
def db_get_blog_list_by_condition(page: int, size: int, search: str):
    with Session(engine) as session:
        sql = select(Blog).where(or_(Blog.title.like(f'%{search}%'), Blog.content.like(f'%{search}%'))).offset((page-1)*size).limit(size)
        res = session.exec(sql).all()
        sql = select(func.count()).select_from(Blog).where(or_(Blog.title.like(f'%{search}%'), Blog.content.like(f'%{search}%')))
        count = session.exec(sql).first()
        return res, count

# 根据 ID 修改博客的标题和内容
def db_update_blog(id: int, title: str, content: str):
    with Session(engine) as session:
        blog = session.get(Blog, id)
        blog.title = title
        blog.content = content
        blog.updated_at = datetime.now()
        session.commit()
        session.refresh(blog)

# 根据 ID 删除博客
def db_delete_blog(id: int):
    with Session(engine) as session:
        blog = session.get(Blog, id)
        session.delete(blog)
        session.commit()