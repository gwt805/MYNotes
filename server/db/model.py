import os
from typing import Optional
from datetime import datetime
from sqlalchemy import BigInteger, TEXT, DATETIME
from sqlmodel import Field, SQLModel, create_engine

engine = create_engine(f"mysql+pymysql://root:{os.getenv('MYSQL_PASSWORD', 'blog')}@localhost:3306/blog?charset=utf8mb4", echo=False)

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, sa_type=BigInteger(), primary_key=True, index=True)
    username: str = Field(unique=True, nullable=False)
    password: str = Field(nullable=False)
    avatar: str = Field(nullable=True, sa_type=TEXT())
    created_at: str = Field(default=datetime.now(), sa_type=DATETIME(), nullable=False)
    updated_at: str = Field(default=datetime.now(), sa_type=DATETIME(), nullable=False)

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, password={self.password}), avatar={self.avatar}, created_at={self.created_at.strftime("%Y-%d-%m %H:%M:%S")}, updated_at={self.updated_at.strftime("%Y-%d-%m %H:%M:%S")}>"

class Blog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, sa_type=BigInteger(), primary_key=True, index=True)
    title: str = Field(nullable=False)
    content: str = Field(nullable=False, sa_type=TEXT())
    created_at: str = Field(default=datetime.now(), sa_type=DATETIME(), nullable=False)
    updated_at: str = Field(default=datetime.now(), sa_type=DATETIME(), nullable=False)

    def __repr__(self):
        return f"<Blog(id={self.id}, title={self.title}, content={self.content}), created_at={self.created_at.strftime("%Y-%d-%m %H:%M:%S")}, updated_at={self.updated_at.strftime("%Y-%d-%m %H:%M:%S")}>"