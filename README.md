<<<<<<< HEAD
#StackOverflow-lite
This is pre-bootcamp challenge project that creates a Flask-api that allows a user to create a question and post answer to the question
#gh-pages link
https://alovega.github.io/StackOverflow-Lite/UI
=======
[![Build Status](https://travis-ci.com/alovega/StackOverflow-Lite.svg?branch=develop)](https://travis-ci.com/alovega/StackOverflow-Lite) [![Coverage Status](https://coveralls.io/repos/github/alovega/StackOverflow-Lite/badge.svg?branch=develop)](https://coveralls.io/github/alovega/StackOverflow-Lite?branch=develop) [![Maintainability](https://api.codeclimate.com/v1/badges/1af8345792e8e28e40cd/maintainability)](https://codeclimate.com/github/alovega/StackOverflow-Lite/maintainability)

# StackOverflow-lite
This is pre-bootcamp challenge project that creates a Flask-api that allows a user to create a question and post answer to the question also retrieve a question
<br>
#### Endpoints available:
| http methods |    Endpoint route                          |   Endpoint functionality                                     |
| ------------ | ----------------------------------         | ------------------------------------------------------------ |
| POST         | /auth/signup                        |   Creates a user account                                     |
| POST         | /auth/login                         |   Logs in a user                                             |
| GET          | /questions                          |   Get all questions on platform                              |
| POST         | /questions                          |   Post a new question                                        |
| GET          | /questions/<question_id>            |   Get a single question                                      |
| DELETE       | /questions/<question_id>            |   Delete a question                                          |
| POST         | /questions/<question_id>/answers    |   Post an answer                                             |
| GET          | /questions/<question_id>/answers    |   Get all answers for a question                             |
| PUT          | /questions/<question_id>/answers/<answer_id>           |   Edit or accept an answer                |
## Prerequisites
    pip
    virtualenv
    python 3.6
    postgresql

## Setting up database
#### To create the databases through the command line:
      ```
      $ psql postgres
      postgres=# CREATE DATABASE app_database;
      postgres=#CREATE DATABASE test_db;
    
## installation
    clone this repo:
    ```
    git clone https://github.com/alovega/StackOverflow-Lite.git
    ```
    create virtual environment:
    ```
    virtualenv <name of your env>
    ```
    activate your virtualnv:
    ```
    $source <name of your env>/Scripts/activate (in bash)
    ```
    install dependencies:
   ```
   $pip install -r requirements.txt
   ```
   To run the application:
   ```
   $python run.py
   ```
      

## Running the tests
  The tests for StackOverflow-lite  are written using the python module unittests. The tests are found in the folder test
  .<br>
  To run the tests:<br>
    on Your Terminal:
   ```
    $export APP_SETTINGS=testing
   ```
   ```
   $nosetests test/
   ```
  To show coverage:
   ```
   $nosetests test/ --with-coverage
   ```

## Built with 
   Flask-restful, a python framework
   
## Authors
[Alwavega Kevin](https://github.com/alovega)
