from flask import Blueprint, request, abort, jsonify
from models import Coffee
from auth.auth import requires_auth

coffee = Blueprint('coffee', __name__)

@coffee.route('/coffee')
def get_coffee():
    all_drinks = Coffee.query.all()
    return jsonify(success=True, coffee=[drink.format_short() for drink in all_drinks])


@coffee.route('/coffee/<int:coffee_id>')
@requires_auth('get:coffee')
def get_coffee_details(payload, coffee_id):
    print(coffee_id)
    coffee_details = Coffee.query.filter_by(id=coffee_id).first()
    return jsonify(success=True, coffee=coffee_details.format_long())


@coffee.route('/coffee', methods=['POST'])
@requires_auth('create:coffee')
def create_coffee(payload):
    print(payload)
    body = request.get_json()
    name = body['name']
    origin = body.get('origin', None)
    roaster = body.get('roaster', None)
    description = body.get('description', None)
    brewing_method = body.get('brewing_method', None)
    
    new_coffee = Coffee(name=name, origin=origin, roaster=roaster, description=description, brewing_method=brewing_method)
    
    try:
        Coffee.insert(new_coffee)
    except:
        abort(500)
    
    return jsonify(success=True, coffee=new_coffee.format_long())

    
@coffee.route('/coffee/<int:coffee_id>', methods=['PATCH'])
@requires_auth('edit:coffee')
def edit_coffee(payload, coffee_id):
    coffee_to_edit = Coffee.query.filter_by(id=coffee_id).first()
    body = request.get_json()
    origin = body.get('origin', None)
    roaster = body.get('roaster', None)
    brewing_method = body.get('brewing_method', None)
    
    if origin:
        coffee_to_edit.origin = origin
        
    if roaster:
        coffee_to_edit.roaster = roaster
    
    if brewing_method:
        coffee_to_edit.brewing_method = brewing_method
        
    try:
        Coffee.update(coffee_to_edit)
    except:
        abort(500)
    
    return jsonify(success=True, coffee=coffee_to_edit.format_long())


@coffee.route('/coffee/<int:coffee_id>', methods=['DELETE'])
@requires_auth('delete:coffee')
def delete_coffee(payload, coffee_id):
    coffee_to_delete = Coffee.query.filter_by(id=coffee_id).first()
    deleted_id = coffee_to_delete.id

    try:
        Coffee.delete(coffee_to_delete)
    except:
        abort(500)

    return jsonify(success=True, coffee=deleted_id)
