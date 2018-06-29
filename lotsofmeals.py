#!/usr/bin/python
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Meal, Base, MealIngredient

engine = create_engine('sqlite:///mealingredients.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

#Create a user in the databank
User1 = User(name="Nada Baynom",
              email="nbaynom0@skype.com",
              picture='http://dummyimage.com/200x200.png/ff4444/ffffff')
session.add(User1)
session.commit()

#Ingredients for Domi's Homemade Cheeseburger
meal1 = Meal(name="Domis Homemade Cheeseburger", recipe="Den Grill auf ca. 250 Grad vorheizen. Zwiebeln in Ringe schneiden, Kaese reiben und bereitstellen. Tomaten in Scheiben schneiden, Salat waschen. Aus Ketchup, Senf und BBQ-Sauce zu gleichen Teilen eine Burgersauce herstellen. Aus dem Rindfleisch selbst Hackfleisch drehen oder gekauftes Rinderhack verwenden. Mit Salz und Pfeffer wuerzen und gut vermengen. Daraus ca. 200 g schwere Kugeln formen und dabei ein wenig kneten.")

session.add(meal1)
session.commit()

mealIngredient1 = MealIngredient(name="Rinderhackfleisch", price="6,00", supermarket="Metzgerei Walk", meal=meal1)

session.add(mealIngredient1)
session.commit()

mealIngredient2 = MealIngredient(name="Burger Buns", price="1,99", supermarket="Rewe", meal=meal1)

session.add(mealIngredient2)
session.commit()

mealIngredient3 = MealIngredient(name="Scheiblettenkaese", price="1,29", supermarket="Edeka", meal=meal1)

session.add(mealIngredient3)
session.commit()

mealIngredient4 = MealIngredient(name="Bacon", price="2,50", supermarket="Aldi", meal=meal1)

session.add(mealIngredient4)
session.commit()

mealIngredient5 = MealIngredient(name="Avocado", price="1,49", supermarket="Norma", meal=meal1)

session.add(mealIngredient5)
session.commit()


#Ingredients for Meeresfruechte Risotto
meal2 = Meal(name="Meeresfruechte Risotto", recipe="Zwiebeln und Knoblauch in etwas Butter glasig duensten, unaufgetaute Meeresfruechte zugeben und ebenfalls duensten. Die Haelfte der Petersilie untermengen und nun Reis zufuegen, ebenfalls glasig duensten. Erst mit Wein, dann nach und nach mit Bruehe abloeschen. Zum Schluss Parmesan, Butter und Rest Petersilie unterruehren und nach Geschmack wuerzen.")

session.add(meal2)
session.commit()

mealIngredient1 = MealIngredient(name="Risotto Reis", price="3,29", supermarket="Edeka", meal=meal2)

session.add(mealIngredient1)
session.commit()

mealIngredient2 = MealIngredient(name="Meeresfruechte", price="4,00", supermarket="Rewe", meal=meal2)

session.add(mealIngredient2)
session.commit()

mealIngredient3 = MealIngredient(name="Parmesan", price="1,59", supermarket="Rewe", meal=meal2)

session.add(mealIngredient3)
session.commit()

mealIngredient4 = MealIngredient(name="Butter", price="0,29", supermarket="Aldi", meal=meal2)

session.add(mealIngredient4)
session.commit()


#Ingredients for Spaghetti Bolognese

meal3 = Meal(name="Spaghetti Bolognese", recipe="In einem grossen Topf den Speck und den Rosmarin in Olivenoel goldgelb anbraten. Zwiebeln und Knoblauch zugeben und 3 Minuten unter Ruehren anschmoren. Dann das Hackfleisch zugeben und anbraten. Danach den Wein zugeben und die Fluessigkeit etwas reduzieren lassen. Dann den Oregano, die Moehren und alle Tomaten und n.B. etwas Tomatenmark zugeben. Mit den Gewuerzen, ausser dem Basilikum, gut abschmecken, nochmals aufkochen, die Hitze fast ganz runter nehmen, Deckel drauf und 1,5 bis 2 Stunden leise koecheln lassen. Kurz vor Ende die Nudeln nach Packungsanleitung al dente kochen. In die fertige Sauce das frisch zerkleinerte Basilikum geben und mit frisch geriebenem Parmesan und Rotwein servieren.")

session.add(meal3)
session.commit()

mealIngredient1 = MealIngredient(name="Spaghetti", price="1,29", supermarket="Aldi", meal=meal3)

session.add(mealIngredient1)
session.commit()

mealIngredient2 = MealIngredient(name="Rinderhackfleisch", price="6,00", supermarket="Metzgerei Walk", meal=meal3)

session.add(mealIngredient2)
session.commit()

mealIngredient3 = MealIngredient(name="Passierte Tomaten", price="0,75", supermarket="Rewe", meal=meal3)

session.add(mealIngredient3)
session.commit()

mealIngredient4 = MealIngredient(name="Zwiebel", price="0,29", supermarket="Edeka", meal=meal3)

session.add(mealIngredient4)
session.commit()


print "added Meal ingredients!"
