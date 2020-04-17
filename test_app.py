import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Coffee, Method

class CoffeeTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "coffeerank_test"
        self.database_path = f"postgres://localhost:5432/{self.database_name}"
        setup_db(self.app, self.database_path)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()
    
    def tearDown(self):
        pass
    
    def test_get_paginated_coffee(self):
        res = self.client().get('/coffee')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
    
    def test_add_coffee(self):
        new_coffee = {
            'origin': 'Tanzania',
            'roaster': 'Java Coffee',
            'brewing_method': 2,
        }
        res = self.client().post('/coffee', json=new_coffee)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['coffee'])
    
    def test_edit_coffee(self):
        coffee_to_edit = Coffee.query.order_by(Coffee.id).all()[-1]
        coffee_id = coffee_to_edit.id
        
        new_coffee = {
            'roaster': 'Johan & Nystrom'
        }
        
        res = self.client().patch(f'/coffee/{1}', json=new_coffee)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['coffee'])
        
    def test_delete_coffee(self):
        coffee_to_delete = Coffee.query.order_by(Coffee.id).all()[-1]
        coffee_id = coffee_to_delete.id
        
        res = self.client().delete(f'/coffee/{coffee_id}')
        data = json.loads(res.data)
        
        coffee = Coffee.query.filter_by(id=coffee_id).one_or_none()
        print(coffee)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(coffee, None)
        
        
if __name__ == "__main__":
    unittest.main()