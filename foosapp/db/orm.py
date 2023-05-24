from datetime import datetime
from typing import List, Optional, Union

from flask import g
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, String, create_engine, DateTime, func, Table, Column, Boolean, null
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session
from uuid import uuid4

db_hook = SQLAlchemy()


def get_db():
    if 'db' not in g:
        g.db = db_hook

    return g.db


def now(): return datetime.now()


class UserGame(db_hook.Model):
    __tablename__ = "users_games"
    is_left: Mapped[bool] = mapped_column()

    users_id: Mapped[bytes] = mapped_column(ForeignKey("users.id"), primary_key=True)
    games_id: Mapped[bytes] = mapped_column(ForeignKey("games.id"), primary_key=True)
    user: Mapped["User"] = relationship(back_populates="games")
    game: Mapped["Game"] = relationship(back_populates="users")


class User(db_hook.Model):
    __tablename__ = "users"

    id: Mapped[bytes] = mapped_column(primary_key=True, default=uuid4().bytes)
    games: Mapped[List['UserGame']] = relationship(back_populates="user")
    goals: Mapped[List['Goal']] = relationship(back_populates="scored_by")

    nickname: Mapped[str] = mapped_column(unique=True)
    pin: Mapped[int] = mapped_column()


class Game(db_hook.Model):
    __tablename__ = "games"

    id: Mapped[bytes] = mapped_column(primary_key=True, default=uuid4().bytes)
    users: Mapped[List[UserGame]] = relationship(back_populates="game")

    goals: Mapped[List['Goal']] = relationship(back_populates="owning_game")

    started_at: Mapped[datetime] = mapped_column(default=now)
    ended_at: Mapped[Optional[datetime]] = mapped_column()


class Goal(db_hook.Model):
    __tablename__ = "goals"

    id: Mapped[bytes] = mapped_column(primary_key=True, default=uuid4().bytes)

    game_id: Mapped[bytes] = mapped_column(ForeignKey('games.id'))
    owning_game: Mapped[Game] = relationship(back_populates="goals")

    user_id: Mapped[bytes] = mapped_column(ForeignKey('users.id'))
    scored_by: Mapped[User] = relationship(back_populates="goals")

    scored_at: Mapped[datetime] = mapped_column(default=now)


# engine = create_engine("sqlite+pysqlite:///fb_database.db")
# db_hook.Model.metadata.drop_all(engine)
# db_hook.Model.metadata.create_all(engine)
# with Session(engine) as session:
#     session.add(User(nickname="test", pin=1234))
#     session.commit()


def get_user(uid: str) -> Union[User, None]:
    return db_hook.session.execute(db_hook.select(User).where(User.id == uid)).scalar_one() or None


def get_current_game_orm() -> Game:
    try:
        game = db_hook.session.execute(db_hook.select(Game).where(Game.ended_at.is_(None))).scalar_one()
    except NoResultFound:
        game = create_new_game_orm()
    return game


def create_new_game_orm():
    current_game = Game()
    db_hook.session.add(current_game)
    db_hook.session.commit()
    return current_game


