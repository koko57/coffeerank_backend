from flask import Blueprint, request, abort, jsonify
from sqlalchemy.sql import func
from models import db, Coffee, Rating
from auth.auth import requires_auth
from utils import paginate_results

coffee = Blueprint('coffee', __name__)


@coffee.route('/coffee')
def get_coffee():
    page = request.args.get('page', 1, type=int)
    results = Coffee.query.all()
    pagination = paginate_results(page, results)

    all_drinks = pagination['coffees']
    
    if page > pagination['pages']:
        abort(404)

    coffees = [drink.format_short() for drink in all_drinks]

    for coffee_item in coffees:
        rating = db.session.query(func.avg(Rating.value).label('Coffee rating')
                                  ).filter(Rating.coffee_id == coffee_item['id']).first()
        if rating[0]:
            coffee_item['rating'] = float(rating[0])
        else:
            coffee_item['rating'] = None

    return jsonify(success=True, coffee=coffees, pages=pagination['pages'], results_count=pagination['results_count'])


@coffee.route('/coffee/<int:coffee_id>')
@requires_auth('get:coffee')
def get_coffee_details(payload, coffee_id):
    coffee_details = Coffee.query.filter_by(id=coffee_id).first()

    if not coffee_details:
        abort(404)

    value = None
    rating = Rating.query.filter(
        Rating.coffee_id == coffee_id, Rating.user_id == payload['sub']).first()

    if rating:
        value = rating.value

    return jsonify(success=True, coffee=coffee_details.format_long(), rating=value)


@coffee.route('/coffee/<int:coffee_id>/rate', methods=['POST'])
@requires_auth('get:coffee')
def rate_coffee(payload, coffee_id):
    body = request.get_json()
    value = body['value']
    rating = Rating(value=value, coffee_id=coffee_id, user_id=payload['sub'])

    try:
        Rating.insert(rating)
    except:
        abort(500)

    return jsonify(success=True, rating=rating.value)


@coffee.route('/coffee', methods=['POST'])
@requires_auth('create:coffee')
def create_coffee(payload):
    body = request.get_json()
    name = body['name']
    origin = body.get('origin', None)
    roaster = body.get('roaster', None)
    description = body.get('description', None)
    brewing_method = body.get('brewing_method', None)

    new_coffee = Coffee(name=name, origin=origin, roaster=roaster,
                        description=description, brewing_method=brewing_method)

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
