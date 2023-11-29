import unittest
from src.api import app
from src.db import create_conn

class FlaskUntiTest(unittest.TestCase):
    
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
        
        conn = create_conn()
        conn["users"].drop(ignore=True)
        
    
    def test_404(self):
        response = self.app.get('/none/existent/url')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {'error': 'Not Found', 'message': 'The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.'})
      
    
    def test_get_user(self):
        self.app.put('/users/1', json={"name": "John", "lastname": "Doe"})  # We need to create user with id 1
        
        response = self.app.get('/users/1')
        self.assertEqual(response.status_code, 200)
        self.assertIs(type(response.json), dict)
        
        response = self.app.get('/users/500')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {'error': 'Not Found', 'message': 'User does not exist'})
        
        
    def test_create_user(self):
        response = self.app.post('/users', json={"name": "John", "lastname": "Doe"})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, {'message': 'User created successfully'})
        
        response = self.app.post('/users', json={"name": "John"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {'error': 'Bad Request', 'message': 'Missing values to create user'})
        
        # Creating user with one more field than expected. API should ignore age field
        response = self.app.post('/users', json={"name": "John", "lastname": "Doe", "age": 25})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, {"message": "User created successfully"})
    
    
    def test_update_user(self):
        self.app.put('/users/1', json={"name": "John", "lastname": "Doe"})  # We need to create user with id 1
        
        response = self.app.patch('/users/1', json={"name": "John"})
        self.assertEqual(response.status_code, 204)
        
        response = self.app.patch('/users/1', json={"lastname": "Doe"})
        self.assertEqual(response.status_code, 204)
        
        response = self.app.patch('/users/1', json={"age": 25})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {'error': 'Bad Request', 'message': 'Missing values to update user'})
                
        response = self.app.patch('/users/1000', json={"name": "John", "lastname": "Doe"})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {'error': 'Not Found', 'message': 'User does not exist'})
    
    
    def test_update_add_user(self):
        # Testing PUT with existing user
        self.app.put('/users/1', json={"name": "John", "lastname": "Doe"})  # We need to create user with id 1
        response = self.app.put('/users/1', json={"name": "John", "lastname": "Doe"})
        self.assertEqual(response.status_code, 204)
        
        # Testing PUT with non-existing user
        response = self.app.put('/users/500', json={"name": "John", "lastname": "Doe", "age": 25})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, {"message": "User created successfully"})
        
    
    def test_get_all_users(self):
        self.app.put('/users/1', json={"name": "John", "lastname": "Doe"})  # We need to create user with id 1
        
        response = self.app.get('/users')
        self.assertEqual(response.status_code, 200)
        self.assertIs(type(response.json), list)
            
    
    def test_delete_user(self):
        self.app.put('/users/1', json={"name": "John", "lastname": "Doe"})  # We need to create user with id 1
        
        response = self.app.delete('/users/1')
        self.assertEqual(response.status_code, 204)
        

    
if __name__ == "__main__":    
    unittest.main()
