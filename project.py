from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Meal, MealIngredient
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)
APPLICATION_NAME = "Item Catalog Project"

CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Restaurant Menu Application"

engine = create_engine('sqlite:///mealingredients.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route("/")
@app.route("/meals/")
def showMeals():
    meals = session.query(Meal).order_by(Meal.name)
    return render_template("publicmeals.html", meals=meals)


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)

@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output

@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response

@app.route("/meals/new/", methods=["GET","POST"])
def newMeal():
    if "username" not in login_session:
        return redirect ("/login")
    if request.method == "POST":
        newMeal = Meal(name = request.form["gericht"], recipe = request.form["rezept"])
        session.add(newMeal)
        session.commit()
        return redirect(url_for("showMeals"))
    else:
        return render_template("newmeal.html")

@app.route("/meals/<int:meal_id>/delete", methods=["GET","POST"])
def deleteMeal(meal_id):
    deletedMeal = session.query(Meal).filter_by(id=meal_id).one()
    meals = session.query(Meal).filter_by(id=meal_id).one()
    deletedIngredient = session.query(MealIngredient).filter_by(meal_id=meal_id).all()
    if request.method == "POST":
        session.delete(deletedMeal)
        for d in deletedIngredient:
            session.delete(d)
        session.commit()
        return redirect(url_for("showMeals"))
    else:
        return render_template("deletemeal.html", i=deletedMeal)

@app.route("/meals/<int:meal_id>/ingredients/")
def showIngredients(meal_id):
    meals = session.query(Meal).filter_by(id=meal_id).one()
    ingredients = session.query(MealIngredient).filter_by(meal_id=meal_id).all()
    return render_template("publicrecipe.html", meals=meals, ingredients=ingredients)


@app.route("/meals/<int:meal_id>/ingredients/new", methods=["GET","POST"])
def newIngredient(meal_id):
    meals = session.query(Meal).filter_by(id=meal_id).one()
    ingredients = session.query(MealIngredient).filter_by(meal_id=meal_id).all()
    if request.method == "POST":
        if request.form["zutat1"] or request.form["preis1"] or request.form["supermarkt1"]:
            newIngredient1 = MealIngredient(name = request.form["zutat1"], price = request.form["preis1"], supermarket = request.form["supermarkt1"], meal_id = meal_id)
            session.add(newIngredient1)

        if request.form["zutat2"] or request.form["preis2"] or request.form["supermarkt2"]:
            newIngredient2 = MealIngredient(name = request.form["zutat2"], price = request.form["preis2"], supermarket = request.form["supermarkt2"], meal_id = meal_id)
            session.add(newIngredient2)

        if request.form["zutat3"] or request.form["preis3"] or request.form["supermarkt3"]:
            newIngredient3 = MealIngredient(name = request.form["zutat3"], price = request.form["preis3"], supermarket = request.form["supermarkt3"], meal_id = meal_id)
            session.add(newIngredient3)

        session.commit()
        return redirect(url_for("showIngredients", meal_id = meal_id))
    else:
        return render_template("newingredient.html", ingredients=ingredients, meals = meals)

@app.route("/meals/<int:meal_id>/ingredients/edit", methods=["GET","POST"])
def editMeal(meal_id):
    meals = session.query(Meal).filter_by(id=meal_id).one()
    editedMeal = session.query(Meal).filter_by(id=meal_id).one()
    if request.method == "POST":
        if request.form["gericht"]:
            editedMeal.name = request.form["gericht"]

        if request.form["rezept"]:
            editedMeal.recipe = request.form["rezept"]
        session.add(editedMeal)
        session.commit()
        return redirect(url_for("showIngredients", meal_id=meal_id))
    else:
        return render_template("editmeal.html", i=editedMeal)

@app.route("/meals/<int:meal_id>/ingredients/<int:ingredient_id>/", methods=["GET","POST"])
def ingredientInfo(meal_id, ingredient_id):
    meals = session.query(Meal).filter_by(id=meal_id).one()
    ingredients = session.query(MealIngredient).filter_by(meal_id=meal_id, id=ingredient_id).one()
    return render_template("publicincredient.html", meals=meals, ingredients=ingredients)

@app.route("/meals/<int:meal_id>/ingredients/<int:ingredient_id>/edit", methods=["GET","POST"])
def editIngredient(meal_id, ingredient_id):
    meals = session.query(Meal).filter_by(id=meal_id).one()
    ingredients = session.query(MealIngredient).filter_by(meal_id=meal_id, id=ingredient_id).one()
    if request.method == "POST":
        if request.form["zutat"]:
            ingredients.name = request.form["zutat"]

        if request.form["preis"]:
            ingredients.price = request.form["preis"]

        if request.form["supermarkt"]:
            ingredients.supermarket = request.form["supermarkt"]

        session.add(ingredients)
        session.commit()
        return redirect(url_for("showIngredients", meal_id=meal_id))
    else:
        return render_template("editingredient.html", i=ingredients, meals=meals)

@app.route("/meals/<int:meal_id>/ingredients/<int:ingredient_id>/delete", methods=["GET","POST"])
def deleteIngredient(meal_id, ingredient_id):
    meals = session.query(Meal).filter_by(id=meal_id).one()
    deletedIngredient = session.query(MealIngredient).filter_by(id=ingredient_id).one()
    if request.method == "POST":
        session.delete(deletedIngredient)
        session.commit()
        return redirect(url_for("showIngredients", meal_id=meals.id))
    else:
        return render_template("deleteingredient.html", i=deletedIngredient)



@app.route("/meals/<int:meal_id>/ingredients/JSON")
def mealJSON(meal_id):
    meal = session.query(Meal).filter_by(id=meal_id).one()
    ingredients = session.query(MealIngredient).filter_by(meal_id=meal_id).all()
    return jsonify(Dish=meal.serialize, Ingredients=[i.serialize for i in ingredients])

@app.route("/meals/<int:meal_id>/ingredients/<int:ingredient_id>/JSON")
def ingredientJSON(meal_id, ingredient_id):
    ingredients = session.query(MealIngredient).filter_by(meal_id=meal_id, id=ingredient_id).one()
    return jsonify(Ingredients_Data=ingredients.serialize)






if __name__ == "__main__":
    app.secret_key = CLIENT_ID
    app.debug = True
    app.run(host = "0.0.0.0", port = 5000)
