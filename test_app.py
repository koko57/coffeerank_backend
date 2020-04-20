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

        self.user = os.environ['USER_TOKEN']
        self.admin = os.environ['ADMIN_TOKEN']

        self.new_coffee = {
            'name': 'Tanzania Ilomba',
            'origin': 'Tanzania',
            'roaster': 'Java Coffee',
            'brewing_method': 2,
        }

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
        self.assertTrue(data['pages'])
        self.assertTrue(data['results_count'])


    def test_get_paginated_coffee_not_existing(self):
        res = self.client().get('/coffee?page=100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Resource not found')


    def test_get_coffee_no_auth(self):
        res = self.client().get('/coffee/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    def test_get_coffee(self):
        res = self.client().get(
            '/coffee/1', headers={"Authorization": f"Bearer {self.admin}"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_get_coffee_not_existing(self):
        res = self.client().get(
            '/coffee/1000', headers={"Authorization": f"Bearer {self.user}"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])


    def test_add_coffee(self):
        res = self.client().post('/coffee', json=self.new_coffee,
                                 headers={"Authorization": f"Bearer {self.admin}"})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['coffee'])

        
    def test_add_coffee_no_auth(self):
        res = self.client().post('/coffee', json=self.new_coffee)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
    

    def test_add_coffee_user(self):
        res = self.client().post('/coffee', json=self.new_coffee,
                                 headers={"Authorization": f"Bearer {self.user}"})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Access denied')


    def test_edit_coffee(self):
        coffee_to_edit = Coffee.query.order_by(Coffee.id).all()[-1]
        coffee_id = coffee_to_edit.id

        edited_coffee = {
            'roaster': 'Johan & Nystrom'
        }

        res = self.client().patch(
            f'/coffee/{1}', json=edited_coffee, headers={"Authorization": f"Bearer {self.admin}"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['coffee'])


    def test_delete_coffee(self):
        coffee_to_delete = Coffee.query.order_by(Coffee.id).all()[-1]
        coffee_id = coffee_to_delete.id

        res = self.client().delete(
            f'/coffee/{coffee_id}', headers={"Authorization": f"Bearer {self.admin}"})
        data = json.loads(res.data)

        coffee = Coffee.query.filter_by(id=coffee_id).one_or_none()
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(coffee, None)


    def test_delete_coffee_user(self):
        coffee_to_delete = Coffee.query.order_by(Coffee.id).all()[-1]
        coffee_id = coffee_to_delete.id

        res = self.client().delete(
            f'/coffee/{coffee_id}', headers={"Authorization": f"Bearer {self.user}"})
        data = json.loads(res.data)

        coffee = Coffee.query.filter_by(id=coffee_id).one_or_none()
        
        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])
        self.assertTrue(coffee)


if __name__ == "__main__":
    unittest.main()
