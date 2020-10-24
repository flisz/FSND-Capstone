# Full Stack Capstone Project "Mymed"

## Application Purpose:
* Create a web service to keep track of medical information

### Main Files: Project Structure

  ```sh
  ├── README.md
  ├── config.yaml
  ├── db-info.yaml
  ├── requirements.txt *** pip dependencies  
  ├── migrations       *** database migration files
  ├── mymed
  │   ├── app
  │   ├── lib
  │   ├── models
  │   ├── setup
  │   ├── views
  │   ├── static
  │   │   ├── css 
  │   │   ├── font
  │   │   ├── ico
  │   │   ├── img
  │   │   └── js
  │   └── templates
  │       ├── errors
  │       ├── forms
  │       ├── layouts
  │       └── pages  
  ├── conftest.py *** configuration file for pytest
  ├── setup.cfg   *** application setup (primarily for pytest) 
  └── tdd         *** folder for tests
      ├── fixtures 
      │   ├── static *** directory for static test configuration files
      │   └── *.py   *** module specific pytest fixtures
      └── tdd_*.py *** pytest files
  
  ```

## Getting Started

### Install Python and Dependencies

#### Python 3.8
#### Virtual Environment
We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies
Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:
```bash
pip install -r requirements.txt
```
##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.
- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 
- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Configure Application:

Application environment variables are set using the `/config.yaml` file. 

1) Copy `/temp.config.yaml` to `/config.yaml`
2) Edit `/config.yaml` to set `port`, `mode`, `secret_key` and `jwt_secret`

## Database Setup: 

1) Install postrgesql and set up permissions.
    1) ##TODO: ADD postgres install commands! 
2) Copy /temp.db-info.yaml to /db-info.yaml and edit permissions.  
    1) To use defaults, leave username/password alone. 
        1) `username:default --> postgres`
        2) `password:default --> no password`
3) Initialize application databases.
4) Create application and testing databases: 

```bash
initdb db_mymed
initdb db_mymed_testing
```

## Testing deployment: 

#TODO --> FILL THIS SECTION OUT!!!!!!!

## Running the server

To run the server, execute:

In Linux:
```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

In Windows: 
```bash
set FLASK_APP=flaskr
set FLASK_ENV=development
flask run
```

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## API Errors
#### 404 Resource Not Found
Server could not find requested resource.
#### 422 Unprocessable
Method used incorrectly on the target resource.
#### 405 Method Not Allowed
Request Method cannot be used on the target resource.
#### 500 Internal Server Error
Server encountered an issue while processing the request.  

# TODO --> Update this!!!!!! API Reference 
### GET /api/categories
#### General
* Retrieves all available question categories in json format
#### Sample Request
```bash
curl -X GET --url http://localhost:5000/api/categories
```
#### Sample Response
```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true,
  "total_categories": 6
}
```


### GET /api/questions
#### General
* Get a page of 10 questions from all categories.
* To request a specific page of questions, use 'page' arg in get request. 
* Returns fields: success, categories, current_category, page, questions, total_questions
#### Sample Request
```bash
curl -X GET --url http://localhost:5000/api/questions
curl -X GET --url http://localhost:5000/api/questions?page=1
```
#### Sample Response
```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": "ALL",
  "page": 1,
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ],
  "success": true,
  "total_questions": 19
}
```

### POST /api/questions (add new question)
#### General
* Adds a question to the list of available questions.
* Requires fields 'answer', 'category', 'difficulty', 'question'.
* (optional) 'id' field may be specified and will be used if it does not already exist. 
#### Sample Request
```bash
curl --url http://localhost:5000/api/questions --data "{\"category\": \"5\", \"answer\": \"Nowhere\", \"question\": \"There is a Korean Film titled \\\"The Man From _________\\\"\", \"difficulty\": 3}" -H "Content-Type: application/json"
```
#### Sample Response
```json
{
  "question": {
    "answer": "Nowhere",
    "category": 5,
    "difficulty": 3,
    "id": 26,
    "question": "There is a Korean Film titled \"The Man From _________\""
  },
  "success": true
}
```

### POST /api/questions (search)
#### General
* Search for questions containing the provided 'searchTerm' 
#### Sample Request
```bash
 curl --url http://localhost:5000/api/questions --data "{\"searchTerm\": \"Lestat\"}" -H "Content-Type: application/json"
```
#### Sample Response
```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": "ALL",
  "page": 1,
  "questions": [
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }
  ],
  "success": true,
  "total_questions": 1
}
```  

### DELETE /api/questions/#
#### General
* Deletes the question with an id=#
#### Sample Request
```bash
curl --url http://localhost:5000/api/questions/25 -X DELETE
```
#### Sample Response
```json
{
  "deleted": 25,
  "success": true
}
``` 

### GET /api/questions/#
#### General
* Retrieves data on the question with id=#
#### Sample Request
```bash
curl --url http://localhost:5000/api/questions/5
```
#### Sample Response
```json
{
  "question": {
    "answer": "Maya Angelou",
    "category": 4,
    "difficulty": 2,
    "id": 5,
    "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
  },
  "success": true
}
``` 



### TEMPLATE /api/
#### General
* 
#### Sample Request
```bash

```
#### Sample Response
```json

``` 

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```