import sqlalchemy as sa
from database import Base


class Users(Base):
    __tablename__ = "users"
    id: int = sa.Column(sa.Integer, primary_key=True, index=True)
    username: str = sa.Column(sa.String, unique=True)
    email: str = sa.Column(sa.String, unique=True)
    hashed_password: str = sa.Column(sa.String)
    first_name: str = sa.Column(sa.String)
    last_name: str = sa.Column(sa.String)
    is_active: bool = sa.Column(sa.Boolean, default=True)
    role: str = sa.Column(sa.String)


class Birthday(Base):
    __tablename__ = "birth_day_body"

    id: int = sa.Column(sa.Integer, primary_key=True, index=True)
    title: str = sa.Column(sa.String)
    description: str = sa.Column(sa.String)
    priority: int = sa.Column(sa.Integer)
    complete: bool = sa.Column(sa.Boolean, default=False)
