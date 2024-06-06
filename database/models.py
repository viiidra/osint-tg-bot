from datetime import datetime, UTC
from typing import Optional, Literal
import enum

import sqlalchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import (
    Column,
    Enum,
    ForeignKey,
    Index,
    Integer,
    MetaData,
    PrimaryKeyConstraint,
    String,
    Table,
    text, BigInteger,
    DateTime,
    func
)
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import Mapped, mapped_column


class Base(AsyncAttrs, DeclarativeBase):
    repr_cols_num = 6
    repr_cols = tuple()

    def __repr__(self):
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")

        return f"<{self.__class__.__name__} {', '.join(cols)}>"


class SearchType(enum.Enum):
    flp_name = "last name, first name and patronymic"
    fl_name = "last and first name"
    last_name = "last name"
    nickname = "nickname"


class UserRequest(Base):
    __tablename__ = "requests"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger)
    tg_username: Mapped[str] = mapped_column(String(256))
    search_type: Mapped[SearchType]
    search_str: Mapped[str] = mapped_column(String(512))
    search_time: Mapped[datetime]
    report_url: Mapped[str] = mapped_column(String(512))


class Ban(Base):
    __tablename__ = "banned_users"

    # id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True)
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger)
    banned_at: Mapped[datetime]
    banned_to: Mapped[Optional[datetime]]
