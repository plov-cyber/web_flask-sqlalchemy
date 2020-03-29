import sqlalchemy
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase

job_to_category = sqlalchemy.Table('job_to_category', SqlAlchemyBase.metadata,
                                   sqlalchemy.Column('job', sqlalchemy.Integer,
                                                     sqlalchemy.ForeignKey('jobs.id')),
                                   sqlalchemy.Column('category', sqlalchemy.Integer,
                                                     sqlalchemy.ForeignKey('categories.id')))


class HazardCategory(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'categories'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
