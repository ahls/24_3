"""Blogly application."""
from flask import Flask, request, render_template,redirect, flash, session, jsonify

#from flask_debugtoolbar import DebugToolBarExtension
from models import db, connect_db, Cupcake


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'hehe123'
#debug= DebugToolBarExtension(app)
connect_db(app)

with app.app_context():
    db.create_all()

def serializeCupcake(cupcake):
    return {'id':cupcake.id,'flavor':cupcake.flavor,'size':cupcake.size,'rating':cupcake.rating,'image':cupcake.image}

@app.route('/api/cupcakes', methods=['GET'])
def GetAllCupcakes():
    cupcakes = Cupcake.query.all()
    serialized = [serializeCupcake(c) for c in cupcakes]
    return (jsonify(cupcakes=serialized))

@app.route('/api/cupcakes/<int:id>')
def GetCupcakeInfo(id):
    cupcake = Cupcake.query.get_or_404(id)
    return jsonify(cupcake = serializeCupcake(cupcake))

@app.route('/api/cupcakes', methods=['POST'])
def AddCupcake():
    newCupcake = Cupcake(flavor = request.json["flavor"],size = request.json["size"],rating = request.json["rating"],image = request.json["image"])
    db.session.add(newCupcake)
    db.session.commit()
    response_json = jsonify(cupcake=serializeCupcake(newCupcake))
    return (response_json,201)

@app.route('/api/cupcakes/<int:id>', methods=['PATCH'])
def patchCupcake(id):
    cupcake = Cupcake.query.get_or_404(id)
    cupcake.flavor = request.json['flavor']
    cupcake.size = request.json['size']
    cupcake.rating = request.json['rating']
    cupcake.image = request.json['image']
    db.session.commit()
    return jsonify(cupcake = serializeCupcake(cupcake))

    
@app.route('/api/cupcakes/<int:id>', methods=['DELETE'])
def deleteCupcake(id):
    cupcake = Cupcake.query.get_or_404(id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify()

@app.route('/')
def homepage():
    return render_template('home.html')