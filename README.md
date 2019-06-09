# C1-Backend-Challenge
A Python and Flask backend application that mimics correlation one's current data science assessment for potential new hires.

## Getting Started

Follow the following instructions to run the backend and ensure that you have the necessary packages and tools installed first.

### Prerequisites

- virtualenv
- Ensure port 5000 is available and free to use.
-- lsof -t -i :5000 (Shows if the port is in use)
-- kill $(lsof -t -i :5000) (If the port is being used, use the following command to kill it) 

### Tools Required

- Python 2.7 or later
- pip install virtualenv
- pip install flask

### Installing

Clone the repo and cd into the root directory and run the following commands in order.

Create a virtual environment in the project's root directory.

`virtualenv .venv`  (Note: ".venv" is the virtual environment name, it can be set to whatever you'd like)

Activate the virtual environment.

`source .venv/bin/activate`

Install project dependencies.

`pip install -r requirements.txt`

cd into the app directory.

`cd app`

Create a db file.

`touch c1.db`

Specify Flask's entrypoint.

`export FLASK_APP=main.py`

Run the project.

`flask run`

That's it! You're ready to hit the specified endpoints.

Run the example test! It uses every available endpoint.
`python ../test.py`


## API Specification
If you are using Postman to test this interface, ensure that you
raw json as your body type.
The general approach to this API ensures:
1) a user can continue their assesment from a different browser page
2) a user will not be served a question if they have exceeded the alloted time
3) as in the example test, at the end of the asssessment a user will be able to view and change all answers if time permits

### Create a user
```
POST http://localhost:5000/user/create_session
```
Request body:
```
{
    "email": "", 
    "first_name": "", 
    "last_name": ""
}
```

Returns:
```
{
    "timeLeft": ,
    "first_name": "",
    "last_name": "",
    "UUID": ""
}
```

### Get next question for a user(UUID)
```
GET http://localhost:5000/assessment/<UUID>
```

This is a unique url which serves the user the next available question,
if any.

Returns:
```
{
    "status": "", 
    "body": "",
    "answers": "{}",
    "question_type": "", 
    "question_id": 
}
```

Where "status" is one of ("NO TIME LEFT", "QUESTION", "NO QUESTIONS LEFT").

### POST an answer to a question
```
POST http://localhost:5000/assessment/<UUID>
```

Request body:
```
{
    "question_id": "", 
    "answer": ""
}
```
Returns:
```
{
    "status": ""
}
```

Where "status" is one of ("SUBMITTED", "NO TIME LEFT").

### GET all questions with user answers
```
GET http://localhost:5000/answers/<UUID>
```

This endpoint is used at the end of the test to return a list of all questions with answers to the user.

Returns:
```
{
    "status": "",
    "data":
        [
             {
                 "question_id": ,
                 "question_type": "",
                 "body": "",
                 "answers": "",
                 "user_answer": ""
             },
             ...
         ]
}
```
Where "status" is one of ("QUESTIONS", "NO TIME LEFT"). 
Note: if "status" = "NO TIME LEFT", data will be an empty list.
### POST all questions with user answers

```
POST http://localhost:5000/answers/<UUID>
```

This endpoint is used at the end of the test to submit modifications to several questions.

Request body:
```
{
    "data" : 
       [
          {
             "question_id": "", 
             "updated_user_answer": ""
          }
          ...
       ]
}
```

Returns:
```
{
    "status": ""
}
```

Where "status" is one of ("SUBMITTED", "NO TIME LEFT").
