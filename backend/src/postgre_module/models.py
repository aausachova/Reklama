from typing import Optional

from sqlalchemy import JSON, PickleType, ForeignKey, Table, Column, DateTime
from uuid import uuid4, UUID
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.mutable import MutableList
from . import Base
from typing import List
from datetime import datetime
from sqlalchemy.dialects.postgresql import ARRAY, TEXT


class User(Base):
    __tablename__ = "user_table"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    hashed_password: Mapped[str]
    username: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True, nullable=True)
    role_id: Mapped[UUID] = mapped_column(
        ForeignKey("role_table.id"))
    role: Mapped["Role"] = relationship(lazy="selectin")

    def __repr__(self) -> str:
        return f"User(id={self.id}, username={self.username}, email={self.email})"


class Permission(Base):
    __tablename__ = "permission_table"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(unique=True)

    def __repr__(self) -> str:
        return f"Permission(id={self.id}, name={self.name})"


class Role(Base):
    __tablename__ = "role_table"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(unique=True)

    def __repr__(self) -> str:
        return f"Role(id={self.id}, name={self.name})"


class RolePerm(Base):
    __tablename__ = "role_perm_table"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    role_id: Mapped[UUID] = mapped_column(ForeignKey("role_table.id"))
    permission_id: Mapped[UUID] = mapped_column(
        ForeignKey("permission_table.id"))

    role: Mapped[Role] = relationship(lazy="selectin")
    perm: Mapped[Permission] = relationship(lazy="selectin")

    def __repr__(self):
        return f"RolePerm(id={self.id}, role_id={self.role_id}, perm_id={self.permission_id})"


class File(Base):
    __tablename__ = "file_table"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    s3_bucket: Mapped[str]
    s3_key: Mapped[str]

    file_name: Mapped[str]

    created_date: Mapped[datetime] = mapped_column(server_default=func.now())
    last_modified_date: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now())

    public_url: Mapped[str | None] = mapped_column(nullable=True)

    owner_id: Mapped[UUID] = mapped_column(ForeignKey("user_table.id"))
    owner: Mapped[User] = relationship(lazy="selectin")


class Company(Base):
    __tablename__ = "company_table"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str]

    logo_id: Mapped[UUID] = mapped_column(ForeignKey("file_table.id"))
    logo: Mapped[File] = relationship(lazy="selectin")


class Vacancy(Base):
    __tablename__ = "vacancy_table"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    title: Mapped[str]
    city: Mapped[str]
    company: Mapped[str]
    type: Mapped[str]
    direction: Mapped[str]
    experience: Mapped[bool]
    requirements: Mapped[list[str]] = mapped_column(ARRAY(TEXT), default=[])
