# API Development and Documentation for the Trivia App

## Overview

I implemented, tested and documented the APIs for the trivia app with the following features:

1. Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.

## Tech Stack (Dependencies)

### Backend
The [./backend](https://github.com/iDataist/trivia_api/tree/main/backend) directory contains a Flask and SQLAlchemy server with the following dependencies. 
1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python).
2. **Virtual Enviornment** - Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/).
3. **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:
    ```bash
    pip install -r requirements.txt
    ```
4. **Other Dependencies**
 - [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.
 - [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. 
 - [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

### Frontend

The [./frontend](hhttps://github.com/iDataist/trivia_api/tree/main/frontend) directory contains a React frontend to consume the data from the Flask server with the following dependencies.
1. **Node and NPM**<br>
This project depends on Nodejs and Node Package Manager (NPM). Before continuing, you must download and install Node (the download includes NPM) from [https://nodejs.com/en/download](https://nodejs.org/en/download/).

2. **Other Dependencies**<br>
This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the `frontend` directory of this repository. After cloning, open your terminal and run:
    ```bash
    npm install
    ```
## Getting Started
Run the following commands to spin up the database, backend and frontend in the local environment:

Database: In pgAdmin4, create a new database `triviadb` and run the queries in `schema.sql` and `seed.sql` to create and populate the tables. 

Backend:
```
cd backend
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```
Frontend:
```
cd frontend
npm start
```
## Endpoints
```js
GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains an object of id: category_string key:value pairs. 
{
    'categories': { '1' : "Science",
    '2' : "Art",
    '3' : "Geography",
    '4' : "History",
    '5' : "Entertainment",
    '6' : "Sports" }
}
```


```js
GET '/questions?page=${integer}'
- Fetches a paginated set of questions, a total number of questions, all categories and current category string. 
- Request Arguments: page - integer
- Returns: An object with 10 paginated questions, total questions, object including all categories, and current category string
{
    'questions': [
        {
            'id': 1,
            'question': 'This is a question',
            'answer': 'This is an answer', 
            'difficulty': 5,
            'category': 2
        },
    ],
    'totalQuestions': 100,
    'categories': { '1' : "Science",
    '2' : "Art",
    '3' : "Geography",
    '4' : "History",
    '5' : "Entertainment",
    '6' : "Sports" },
    'currentCategory': 'History'
}
```

```js
GET '/categories/${id}/questions'
- Fetches questions for a cateogry specified by id request argument 
- Request Arguments: id - integer
- Returns: An object with questions for the specified category, total questions, and current category string 
{
    'questions': [
        {
            'id': 1,
            'question': 'This is a question',
            'answer': 'This is an answer', 
            'difficulty': 5,
            'category': 4
        },
    ],
    'totalQuestions': 100,
    'currentCategory': 'History'
}
```

```js
DELETE '/questions/${id}'
- Deletes a specified question using the id of the question
- Request Arguments: id - integer
- Returns: Does not need to return anything besides the appropriate HTTP status code. Optionally can return the id of the question. If you are able to modify the frontend, you can have it remove the question using the id instead of refetching the questions. 
```

```js
POST '/quizzes'
- Sends a post request in order to get the next question 
- Request Body: 
{'previous_questions':  an array of question id's such as [1, 4, 20, 15]
'quiz_category': a string of the current category }
- Returns: a single new question object 
{
    'question': {
        'id': 1,
        'question': 'This is a question',
        'answer': 'This is an answer', 
        'difficulty': 5,
        'category': 4
    }
}
```

```js
POST '/questions'
- Sends a post request in order to add a new question
- Request Body: 
{
    'question':  'Heres a new question string',
    'answer':  'Heres a new answer string',
    'difficulty': 1,
    'category': 3,
}
- Returns: Does not return any new data
```

```js
POST '/questions'
- Sends a post request in order to search for a specific question by search term 
- Request Body: 
{
    'searchTerm': 'this is the term the user is looking for'
}
- Returns: any array of questions, a number of totalQuestions that met the search term and the current category string 
{
    'questions': [
        {
            'id': 1,
            'question': 'This is a question',
            'answer': 'This is an answer', 
            'difficulty': 5,
            'category': 5
        },
    ],
    'totalQuestions': 100,
    'currentCategory': 'Entertainment'
}
```
