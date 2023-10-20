"""Базовые модели для работы с БД."""
from sqlalchemy import TEXT, VARCHAR, Column
from sqlalchemy.orm import DeclarativeMeta, declarative_base

Base: DeclarativeMeta = declarative_base()


# class UserAlchemyModel(Base):  # type: ignore
#     """Модель для таблицы урлов."""
#
#     __tablename__ = 'urls'
#
#     token = Column(
#         VARCHAR(10),
#         primary_key=True,
#         index=True,
#     )
#     saved_url = Column(
#         TEXT,
#         unique=True,
#         nullable=False,
#         index=True,
#     )
