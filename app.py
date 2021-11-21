from flask import Flask,request
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)



app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class Drink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False) 
    description = db.Column(db.String(120))

    def __repr__(self):
        return f"{self.name}  {self.description}"

@app.route('/')
def index():
    return 'Hello!'

@app.route('/drinks')
def getDrinks():
    drinks = Drink.query.all()
    output=[]
    for drink in drinks:
        drinkInfo = {'name':drink.name, 'description':drink.description}
        output.append(drinkInfo)
    return {"drinks": output}

@app.route('/drinks/<id>')
def getDrink(id):
    drink = Drink.query.get_or_404(id)
    #return jsonify({"name":,"description"})
    return {"name":drink.name, "description":drink.description}

@app.route('/drinks', methods=['POST'])
def addDrink():
    drink = Drink(name=request.json['name'], description=request.json['description'])
    db.session.add(drink)
    db.session.commit()
    return {"id": drink.id}

@app.route('/drinks/<id>', methods=['DELETE'])
def deleteDrink(id):
    drink = Drink.query.get(id)
    if drink is None:
        return {"error": 404}
    db.session.delete(drink)
    db.session.commit()
    return {"message": "success"}