import sqlalchemy as sa
from database import Base


class Birthday(Base):
    __tablename__ = "birth_day_body"

    id: int = sa.Column(sa.Integer, primary_key=True, index=True)
    title: str = sa.Column(sa.String)
    description: str = sa.Column(sa.String)
    priority: int = sa.Column(sa.Integer)
    complete: bool = sa.Column(sa.Boolean, default=False)
