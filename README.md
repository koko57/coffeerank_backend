# CoffeeRank API

CoffeeRank is a database of speciality coffee where logged users can rate the coffee and see the average rating of each coffee.

To test the app use cURL or [Postman](https://www.postman.com)

The app is deployed on Heroku [link]().

## Getting Started (Locally)

### Installing Dependencies

#### Python 3.7

Make sure you have the latest version of python installed on your machine, to check run 
```
python -V
```
in your terminal.

If you do not have Python installed yet follow the instructions in [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


#### Virtual Enviornment

To set up virtual environment follow [this guide](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by running:

```bash
pip3 install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we use to handle cross origin requests from the frontend server.

## Running the server

First ensure that you are working in the created virtual environment.

To run the server, execute:

```bash
source setup.sh
```
Sourcing `setup.sh` sets some environment variables used by the app.

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

You can run this API locally at the default `http://127.0.0.1:5000/`

## Testing

Before running the tests create the database:
```
createdb coffeerank_test
```

If you already have a database named 'coffeerank_test' before the previous command run:

```
dropdb coffeerank_test
```

You can restore the database used for this project 
```
psql coffeerank_test < coffeerank_test.psql
```

To run the tests, run
```
python test_app.py
```

## API Reference

- Base URL: [link](https://fsndcapstone.herokuapp.com)

### Endpoints

- GET '/coffee'
	- Fetch all coffee from the db
	- Request Argument: page (integer)
	- Returns: JSON response containing 10 coffees with their info and average users rating, pages and results count and request status

	```

        {
            "coffee": [
                {
                    "brewing_method": 2, 
                    "id": 1, 
                    "name": "Ethiopia Guji", 
                    "rating": 4.5, 
                    "roaster": "Fjord Coffee"
                }, 
                {
                    "brewing_method": 2, 
                    "id": 2, 
                    "name": "Tanzania Ilomba", 
                    "rating": 3.0, 
                    "roaster": "The Barn"
                }, 
                {
                    "brewing_method": 1, 
                    "id": 3, 
                    "name": "Arcaffe Roma", 
                    "rating": null, 
                    "roaster": "Arcaffe"
                }
            ], 
            "pages": 1, 
            "results_count": 3, 
            "success": true
        }

	```

- GET '/coffee/:id'
	- Get a chosen coffee
	- Request Argument: coffee id (integer)
    - Required permissions: 'get:coffee'
	- Returns: JSON response - chosen coffee details + logged user's rating and request status
	- example
	```
        {
            "coffee": {
                "brewing_method": 2,
                "description": null,
                "id": 1,
                "name": "Ethiopia Guji",
                "origin": "Ethiopia",
                "roaster": "Fjord Coffee"
            },
            "rating": null,
            "success": true
        }
	```
- POST '/coffee/:id/rate'
	- Rate a chosen coffee
	- Request Argument: coffee id (integer)
    - Reqyest Body:
    ```
        {
            "value": 3 (integer 1-5)
        }

    ```
    - Required permissions: 'get:coffee'
	- Returns: JSON response user's rating and request status
	- example
	```
        {
            "rating": 3,
            "success": true
        }
	```

- POST '/coffee'
	- Insert Actor info into DB
	- Request Body:  
    ```
        {
            "name": "Arcaffe Roma",
            "origin": "Brazil",
            "roaster": "Arcaffe",
            "brewing_method": 1 (brewing method id)
        }

    ```
	- Returns: JSON response containing new coffee info andrequest status
	- example
	```

        {
            "coffee": {
                "brewing_method": 1,
                "description": null,
                "id": 3,
                "name": "Arcaffe Roma",
                "origin": "Brazil",
                "roaster": "Arcaffe"
            },
            "success": true
        }

	```

- PATCH '/coffee/:id'
	- Updtae coffee info
	- Request Body: 
    ```

        {
            "roaster": "Arcaffe Italy"
        }

        or 

        {
            "name": "Arcaffe Roma",
            "origin": "Brazil",
            "roaster": "Arcaffe Italy",
            "brewing_method": 1
        }

    ```
    (You can change all the fields or chosen fields only)
    - Required permissions: 'edit:coffee'
	- Returns: JSON response containing changed entry and request status
	- example
	```

        {
            "coffee": {
                "brewing_method": 1,
                "description": null,
                "id": 4,
                "name": "Arcaffe Roma",
                "origin": "Brazil",
                "roaster": "Arcaffe Italy"
            },
            "success": true
        }

	```

- DELETE '/coffee/id'
	- Delete chosen coffee from the db
	- Request Argument: coffee id
    - Required permissions: 'delete:coffee'
	- Returns : JSON response containing deleted coffee id and request status
	- example
    ```
        {
            "coffee": 4,
            "success": true
        }
	```


### Roles and Permissions

To interact with the app users are granted permissions:
- 'get:coffee'
- 'create:coffee'
- 'edit:coffee'
- 'delete:coffee'

There are 2 types of roles for the logged in users with permissions:

- Admin
	- all the permissions

- User
	- 'get:coffee' - access to coffee details and rating chosen coffee
