from datetime import datetime
from typing import List, Optional
from sqlalchemy import ForeignKey, String, create_engine, DateTime, func, Table, Column
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session
from uuid import uuid4


def now(): return datetime.now()


class FoosBase(DeclarativeBase):
    pass


association_table = Table(
    "users_games",
    FoosBase.metadata,
    Column("users_id", ForeignKey("users.id"), primary_key=True),
    Column("games_id", ForeignKey("games.id"), primary_key=True),
)


class User(FoosBase):
    __tablename__ = "users"

    id: Mapped[bytes] = mapped_column(primary_key=True, default=uuid4().bytes)
    games: Mapped[List['Game']] = relationship(
        secondary=association_table, back_populates="users"
    )
    goals: Mapped[List['Goal']] = relationship(back_populates="scored_by")

    nickname: Mapped[str] = mapped_column()
    pin: Mapped[int] = mapped_column()


class Game(FoosBase):
    __tablename__ = "games"

    id: Mapped[bytes] = mapped_column(primary_key=True, default=uuid4().bytes)
    users: Mapped[List[User]] = relationship(
        secondary=association_table, back_populates="games"
    )

    goals: Mapped[List['Goal']] = relationship(back_populates="owning_game")

    started_at: Mapped[datetime] = mapped_column(default=now)


class Goal(FoosBase):
    __tablename__ = "goals"

    id: Mapped[bytes] = mapped_column(primary_key=True, default=uuid4().bytes)

    game_id: Mapped[bytes] = mapped_column(ForeignKey('games.id'))
    owning_game: Mapped[Game] = relationship(back_populates="goals")

    user_id: Mapped[bytes] = mapped_column(ForeignKey('users.id'))
    scored_by: Mapped[User] = relationship(back_populates="goals")

    scored_at: Mapped[datetime] = mapped_column(default=now)


engine = create_engine("sqlite+pysqlite:///fb_database.db")
FoosBase.metadata.drop_all(engine)
FoosBase.metadata.create_all(engine)
with Session(engine) as session:
    session.add(User(nickname="test", pin=1234))
    session.commit()
