import asyncio

from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from config_reader import config


engine = create_async_engine(url=config.db_url.get_secret_value())

new_session = async_sessionmaker(engine, expire_on_commit=False)


class Model(DeclarativeBase):
    pass


class Users(Model):
    __tablename__ = "users"

    tg_id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]


class Images(Model):
    __tablename__ = "images"

    id: Mapped[int] = mapped_column(primary_key=True)
    file_id: Mapped[str]
    file_key: Mapped[str]
    file_name: Mapped[str]
    file_tg_id: Mapped[str]
    file_used: Mapped[int]
    rate: Mapped[float]


class UserImageRate(Model):
    __tablename__ = "pic_user_rate"

    id: Mapped[int] = mapped_column(primary_key=True)
    pic_id: Mapped[str]
    user_id: Mapped[str]
    rate: Mapped[int]
