# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in
   the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This
   keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for
   your platform can be found in
   the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by
   navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle
  requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL
  database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests
  from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createbd trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## APIs

GET `\categories`
Fetches a dictionary of all available categories

- *Request parameters:* none
- *Example response:*

```
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "success": true
}

```

GET `\questions?page=<page_number>`
Fetches a paginated dictionary of questions of all available categories

- *Request parameters (optional):* page:int
- *Example response:*

 ``` {
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": null, 
  "questions": [
     {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 60, 
      "question": "Whose autobiography is entitled \"I Know Why the Caged Bird Sings?\""
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 61, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 62, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
  ], 
  "success": true, 
  "total_questions": 3
}
```

DELETE `/questions/<question_id>`
Delete an existing questions from the repository of available questions

- *Request arguments:* question_id:int
- *Example response:*

```
{
  "deleted": "20", 
  "success": true
}
```

POST `/questions`
Add a new question to the repository of available questions

- *Request body:* {question:string, answer:string, difficulty:int, category:string}
- *Example response:*

```
{
  "created": 21, 
  "success": true,
  'question_created': {
        "question":"Which five colours make up the Olympic rings?",
        "answer":"Black, green, blue, yellow and red",
        "difficulty":"4",
        "category":"6"
    },
  'questions': [{...}]
  'total_questions': 21
}
```

POST `/questions/search`
Fetches all questions where a substring matches the search term (not case-sensitive)

- *Request body:* {searchTerm:string}
- *Example response:*

```
{
  "current_category": null, 
  "search_term: "boxer",
  "questions": [
    {
        answer: "Muhammad Ali",
        category: 4,
        difficulty: 1,
        id: 61,
        question: "What boxer's original name is Cassius Clay?",
    }
  ], 
  "success": true, 
  "total_questions": 1
}
```

GET `/categories/<int:category_id>/questions`
Fetches a dictionary of questions for the specified category

- *Request argument:* category_id:int
- *Example response:*

```
{
  "current_category": 1, 
  "questions": [
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
    {
      "answer": "Alexander Fleming", 
      "category": 1, 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }, 
  ], 
  "success": true, 
  "total_questions": 2
}
```

POST `/quizzes`
Fetches one random question within a specified category. Previously asked questions are not asked again.

- *Request body:* {previous_questions: arr, quiz_category: {id:int, type:string}}
- *Example response*:

```
{
  "question": {
    "answer": "The Liver", 
    "category": 1, 
    "difficulty": 4, 
    "id": 20, 
    "question": "What is the heaviest organ in the human body?"
  }, 
  "success": true
}
```

### Documentation Example

`GET '/api/v1.0/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the
  category
- Request Arguments: None
- Returns: An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs.

```json
{
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
}
```

## Testing

Write at least one test for the success and at least one error behavior of each endpoint using the unittest library.

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
