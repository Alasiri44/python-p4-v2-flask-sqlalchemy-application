# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Pet

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

# add views here 
@app.route('/')
def index():
    response = make_response(
        '<h1>Welcome to the pet directory</h1>',
        200
    )
    return response

@app.route('/pets/<int:id>')
def pet_by_id(id):
    pet = Pet.query.filter(Pet.id == id).first()
    if pet:
        response_body = f'<p>{pet.name} {pet.species}</p>'
        response_status = 200
    else:
        response_body = f'<p>Pet {id} not found</p>'
        response_status = 404
        
    response = make_response(response_body, response_status)
    return response

@app.route('/species/<string:species>')
def pet_by_species(species):
    pet = Pet.query.filter(Pet.species == species).all()
    
    size = len(pet)
    response_body = f'<h2>There are {size} {species}s</h2>'
    if pet:
        for p in pet:
            response_body += f'<p>{p.name}</p>' 
        response_status = 200

    return make_response(response_body, response_status)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
