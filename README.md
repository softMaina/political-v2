[![Build Status](https://travis-ci.org/softMaina/political-v2.svg?branch=develop)](https://travis-ci.org/softMaina/political-v2)
[![Maintainability](https://api.codeclimate.com/v1/badges/903b8f4c158d90de0833/maintainability)](https://codeclimate.com/github/softMaina/political-v2/maintainability)
[![Coverage Status](https://coveralls.io/repos/github/softMaina/political-v2/badge.svg)](https://coveralls.io/github/softMaina/political-v2)

# political-api

This is an application to help electral commisions to register voters and candidates online and carry out the voting exercise with transparency

## EndPoints

| Http method  | EndPoint | Functionality |
| ------------- | ------------- |---------|
| Get  | api/v1/office  | used by user and admin to get all offices |
| Post  | api/v1/office/add  | used by admin to add office |
| Get | api/v1/office/getoffice/:id| used by admin to get a specific office |
| Put | api/v1/office/update/:id | used by admin to update office|
| Get | api/v1/party | used by admin and user to get all parties |
| Get | api/v1/party/getparty/:id | used by user and admin to get a specific party |
| Post | api/v1/party/add | used by admin to add new party |
| Put | api/v1/party/update/:id | used by admin to patch a party |
| Delete | api/v1/party/delete/:id | used by admin to delete a party |

## Installing The Application
- 1. open terminal in your preferred folder
- 2. clone this repo `git clone https://github.com/softMaina/political-api.git` to have a copy locally
- 3. `cd political-api`
- 4. create a virtual environment for the repo `virtualenv venv`
- 5. activate your virtual environment `source venv/bin/activate`
- 5. Install dependencies from the requirements.txt file `pip3 install -r requirements.txt`
- 6. Export environment variables to your environment `export FLASK_APP="run.py"`
- 7. Run the application using flask command `flask run`

## Running tests
Inside the virtual environment created above, run command: `coverage run --source=app.api.v1 -m pytest app/tests/v1 -v -W error::UserWarning && coverage report`

## Party Endpoints
For this endpoint, minimum data required are as follows

 ```
 {
    "name":string,
    "hqaddress":string,
    "logoUrl":string
 }
 ```

## Office Endpoints
For this endpoint, minimum data required are as follows

```
{
    "name" : String, 
    "office_type" : String
 }
 ```

## Technologies used
- 1. Pytests for running tests
- 2. Flask python framework

## Deployment
 https://political-api-v1.herokuapp.com

## Author
Allan Maina

## Credits
This api was build as a part of andela cycle 37 challenge
