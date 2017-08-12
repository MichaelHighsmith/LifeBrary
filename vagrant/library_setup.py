import sys

from sqlalchemy import Column, ForeignKey, Integer, String

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship

from sqlalchemy import create_engine

Base = declarative_base()

class Genre(Base):

	__tablename__ = 'genre'

	id = Column(Integer, primary_key=True)
	name = Column(String(250), nullable=False)

	@property
	def serialize(self):
		return {
			'name' : self.name,
			'id' : self.id,
		}

class Book(Base):

	__tablename__ = 'book'

	name = Column(String(80), nullable = False)
	id = Column(Integer, primary_key=True)
	author = Column(String(250))
	description = Column(String(250))
	date = Column(String(250))
	genre_id = Column(Integer, ForeignKey('genre.id'))
	genre = relationship(Genre)

	@property
	def serialize(self):
		#return object data in easily serializable formate
		return {
			'name' : self.name,
			'author' : self.author,
			'id' : self.id,
			'description' : self.description,
			'date' : self.date,
		}



engine = create_engine('sqlite:///library.db')

Base.metadata.create_all(engine) #goes into the database and adds the classes we will create as new tables in the db