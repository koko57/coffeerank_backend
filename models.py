import os
from sqlalchemy import Column, String, Integer, event
from flask_sqlalchemy import SQLAlchemy
import json
from flask_migrate import Migrate

database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()
    

class Coffee(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    origin = Column(String)
    roaster = Column(String)
    description = Column(String(400))
    brewing_method = Column(Integer, db.ForeignKey('method.id'))

    def __init__(self, name, origin, roaster, description, brewing_method):
        self.name = name
        self.origin = origin
        self.roaster = roaster
        self.description = description
        self.brewing_method = brewing_method

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format_short(self):
        return {
            'id': self.id,
            'name': self.name,
            'roaster': self.roaster,
            'brewing_method': self.brewing_method,
        }
    
    def format_long(self):
        return {
            'id': self.id,
            'name': self.name,
            'origin': self.origin,
            'roaster': self.roaster,
            'description': self.description,
            'brewing_method': self.brewing_method,
        }
        

class Method(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String)
    coffees = db.relationship('Coffee', backref='coffees', lazy=True)
    
    def __init__(self, name):
        self.name = name
    
    def format(self):
        return {
            'id': self.id,
            'name': self.name,
        }


class Rating(db.Model):
    id = Column(Integer, primary_key=True)
    value = Column(Integer, nullable=False)
    user_id = Column(String, nullable=False)
    coffee_id = Column(Integer, db.ForeignKey('coffee.id'))

    def __init__(self, value, user_id, coffee_id):
        self.value = value
        self.user_id = user_id
        self.coffee_id = coffee_id
        
    def insert(self):
        db.session.add(self)
        db.session.commit()


@event.listens_for(Method.__table__, 'after_create')
def insert_initial_values(*args, **kwargs):
    method1 = Method(name='espresso')
    method2 = Method(name='alternative')
    method3 = Method(name='espresso & alternative')
    
    db.session.add_all([method1, method2, method3])
    db.session.commit()
