# Capstone API Backend

The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. As an Executive Producer within the company, I decided to create a system to simplify and streamline this process.

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

I recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages I selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

## Database Setup

The Development Database is hosted on heroku and requires no set up:

```
AUTH0_DOMAIN = 'capstone-project-satas.eu.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'capstone'
```

## Running the server

The Development Application is hosted on heroku and requires no set up, underlying repository can be found here:
[Capstone Code - Satas](https://github.com/u21sk11/capstone-backend-satas)

To update the app, you would need to commit the updated code to the repository, pass the tests, pass a PR and redeploy the code on heroku. Details for this can be shared separately.

Endpoints (I suggest using the postman collections for testing the app. These can be found in postman_tests folder):

Base URL - https://capstone-project-satas.herokuapp.com

- GET `/actors`
- GET `/movies`
- DELETE `/actors/<int:id>`
- DELETE `/movies/<int:id>`
- POST `/actors`
- POST `/movies`
- PATCH `/actors/<int:id>`
- PATCH `/movies/<int:id>`

### Roles

Casting Assistant

- Can view actors and movies

Casting Director

- All permissions a Casting Assistant has and…
- Add or delete an actor from the database
- Modify actors or movies

Executive Producer

- All permissions a Casting Director has and…
- Add or delete a movie from the database

---

GET `/actors`

- Fetches an array of actors paginated by 10
- Request Arguments: None
- Returns: An array of actor objects that contain the following: age (int), gender (String), id (int) and name (String).

```

[
    {
        "age": 67,
        "gender": "M",
        "id": 16,
        "name": "Satas"
    },
    {
        "age": 28,
        "gender": "M",
        "id": 17,
        "name": "Kapocius"
    }
]

```

---

GET `/movies`

- Fetches an array of movies paginated by 10
- Request Arguments: None
- Returns: An array of movie objects that contain the following: title (String), release_date (String) and id (int).

```

[
    {
        "id": 2,
        "release_date": "Thu, 21 May 2020 00:00:00 GMT",
        "title": "Movie Title 1"
    },
    {
        "id": 3,
        "release_date": "Thu, 21 May 2020 00:00:00 GMT",
        "title": "Movie Title 2"
    },
    {
        "id": 36,
        "release_date": "Tue, 11 Jan 2011 00:00:00 GMT",
        "title": "Movie Title 3"
    }
]

```

---

DELETE `/actors/1`

- Deletes an actor with a specific ID
- Request Arguments: actor id - part of the url
- Returns: success key as the outcome of the delete and deleted actor's id.

```

{
    "success": true,
    "deleted_id": 1
}

```

---

DELETE `/movies/1`

- Deletes a movie with a specific ID
- Request Arguments: movie id - part of the url
- Returns: success key as the outcome of the delete and deleted movie's id.

```

{
    "success": true,
    "deleted_id": 1
}

```

---

POST `/actors`

```
{
	"name": "Satas Kapocius",
	"age": 67,
	"gender": "M"
}
```

- Creates a new actor
- Request Arguments: and object with a name, age and gender
- Returns: success key as the outcome of the post and the name of the added actor

```

{
    "success": true,
    "actor": "Satas Kapocius"
}

```

---

POST `/movies`

```
{
	"title": "A movie of Satas",
	"release_date": "21 May, 2020"
}
```

- Creates a new movie
- Request Arguments: and object with a title and release date
- Returns: success key as the outcome of the post and the title of the added movie

```

{
    "success": true,
    "movie": "A movie of Satas"
}

```

---

PATCH `/actors/1`

```

{
"name": "New Satas Kapocius",
"age": 67,
"gender": "M"
}

```

- Updates an existing actor
- Request Arguments: and object with a name, age and gender
- Returns: success key as the outcome of the post and the name of the updated actor

```

{
"success": true,
"actor": "New Satas Kapocius"
}

```

---

PATCH `/movies/1`

```

{
"title": "A new movie of Satas",
"release_date": "21 May, 2020"
}

```

- Updates an existing movie
- Request Arguments: and object with a title and release_date
- Returns: success key as the outcome of the post and the title of the updated movie

```

{
"success": true,
"movie": "A new movie of Satas"
}

```

---

Error Handlers:

- 503
- 404
- AuthError

503 `Service Unavailable`

- Fetched when the connectivity to the database is not working.
- Application: applicable to all CRUD operations

```

{
'success': false,
'error': 503,
'message': 'issues communicating with the database'
}

```

404 `Not Found`

- Fetched when the resource requested does not exist
- Application: applicable to requests for specific entities (e.g. movies that do no exist)

```

{
'success': false,
'error': 404,
'message': 'resource not found'
}

```

AuthError `Authorisation Error`

- Fetched when there is an issue with Authorisation
- Application: applicable to all requests

An example:

```

{
'code': 'invalid_claims',
'description': 'Permissions not included in JWT.'
}

```

## Testing

To run the tests, run

```

python test_flaskr.py

```

Run the postman collections in postman to perfom RBAC tests -> postman_tests

```

```
