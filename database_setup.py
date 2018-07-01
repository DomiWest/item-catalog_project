'''
============================================
#import of all the necessary files and modules
============================================
'''

import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id=Column(Integer, primary_key=True)
    name=Column(String(250), nullable=False)
    email=Column(String(250), nullable=False)
    picture=Column(String(250))

class Meal(Base):
    __tablename__ = 'meal'

    id=Column(Integer, primary_key=True)
    name=Column(String(250), nullable=False)
    recipe=Column(String(1500))
    user_id=Column(Integer, ForeignKey('user.id'))
    user=relationship(User)


    @property
    def serialize(self):
        return {

            'id': self.id,
            'name': self.name,
            'recipe': self.recipe,
        }

class MealIngredient(Base):
    __tablename__ = 'meal_ingredient'

    name=Column(String(80), nullable=False)
    id=Column(Integer, primary_key=True)
    price=Column(String(8))
    supermarket=Column(String(250))
    meal_id=Column(Integer,ForeignKey('meal.id'))
    meal=relationship(Meal)
    user_id=Column(Integer, ForeignKey('user.id'))
    user=relationship(User)


    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'supermarket': self.supermarket,
            'price': self.price,
        }

engine = create_engine('sqlite:///mealingredients.db')
'''Bind the engine to the metadata of the Base class so that the declaratives
can be accessed through a DBSession instance'''
Base.metadata.create_all(engine)
