import os
from sqlalchemy import Column, String, Integer, event
from flask_sqlalchemy import SQLAlchemy
import json
from flask_migrate import Migrate

database_name = "coffeerank"
database_path = f"postgres://localhost:5432/{database_name}"

db = SQLAlchemy()

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    migrate = Migrate(app, db)
    db.init_app(app)
    db.create_all()
    

class Coffee(db.Model):
    id = Column(Integer, primary_key=True)
    origin = Column(String)
    roaster = Column(String)
    brewing_method = Column(Integer, db.ForeignKey('method.id'))

    def __init__(self, origin, roaster, brewing_method):
        self.origin = origin
        self.roaster = roaster
        self.brewing_method = brewing_method

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'origin': self.origin,
            'roaster': self.roaster,  
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


@event.listens_for(Method.__table__, 'after_create')
def insert_initial_values(*args, **kwargs):
    method1 = Method(name='espresso')
    method2 = Method(name='alternative')
    method3 = Method(name='espresso & alternative')
    
    db.session.add_all([method1, method2, method3])
    db.session.commit()