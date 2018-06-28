import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Meal(Base):
    __tablename__ = 'meal'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    recipe = Column(String(1500))


    @property
    def serialize(self):
        return {

            'id': self.id,
            'name': self.name,
            'recipe': self.recipe,
        }

class MealIngredient(Base):
    __tablename__ = 'meal_ingredient'

    name =Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    price = Column(String(8))
    supermarket = Column(String(250))
    meal_id = Column(Integer,ForeignKey('meal.id'))
    meal = relationship(Meal)

# We added this serialize function to be able to send JSON objects in a
# serializable format
    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'supermarket': self.supermarket,
            'price': self.price,
        }

engine = create_engine('sqlite:///mealingredients.db')
Base.metadata.create_all(engine)
