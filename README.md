[![Build Status](https://travis-ci.org/softMaina/political-v2.svg?branch=develop)](https://travis-ci.org/softMaina/political-v2)
[![Maintainability](https://api.codeclimate.com/v1/badges/903b8f4c158d90de0833/maintainability)](https://codeclimate.com/github/softMaina/political-v2/maintainability)
[![Coverage Status](https://coveralls.io/repos/github/softMaina/political-v2/badge.svg)](https://coveralls.io/github/softMaina/political-v2)

# political-api

This is an application to help electral commisions to register voters and candidates online and carry out the voting exercise with transparency

## EndPoints

| Http method  | EndPoint | Functionality |
| ------------- | ------------- |---------|
| Post | api/v2/auth/signup | user can signup into the application|
| Post | api/v2/auth/login | user can signin into the application |
| Get  | api/v2/offices  | used by user and admin to get all offices |
| Post  | api/v2/offices  | used by admin to add office |
| Get | api/v2/offices/:id| used by admin to get a specific office |
| Delete | api/v2/offices/:id | used by admin to delete a specific office|
| Put | api/v2/offices/:id | used by admin to update office|
| Get | api/v2/parties | used by admin and user to get all parties |
| Get | api/v2/parties/:id | used by user and admin to get a specific party |
| Post | api/v2/parties | used by admin to add new party |
| Put | api/v2/parties/:id | used by admin to patch a party |
| Delete | api/v2/parties/:id | used by admin to delete a party |
| Post | api/v2/candidates | used by candidate to register his political aspiration |
| Post | api/v2/votes | used by user to vote|
| Get | api/v2/vote | get vote results |

## Installing The Application
- 1. open terminal in your preferred folder
- 2. clone this repo `git clone https://github.com/softMaina/political-v2.git` to have a copy locally
- 3. `cd political-v2`
- 4. create a virtual environment for the repo `virtualenv venv`
- 5. activate your virtual environment `source venv/bin/activate`
- 5. Install dependencies from the requirements.txt file `pip3 install -r requirements.txt`
- 6. Configure environment `export FLASK_ENV="development"`
- 7. Run application as `python3 run.py`

## Running tests
Set the testing environment in your terminal `export FLASK_ENV="testing"`
Inside the virtual environment created above, run command: `coverage run --source=app.api.v2 -m pytest app/api/v2/tests -v -W error::UserWarning && coverage report`

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
 ## Candidate endpoints
For this endpoint, minimum data requirements are as follows
```
  {
	"office":Integer,
	"party":Integer
 }
```
## Sign up endpoints
For this endpoint, minimum data requirements are as follows
```
 {
    "firstname" : String,
    "lastname" : String,
    "othername": String,
    "email": String,
    "phoneNumber": String,
    "password": String,
    "passportUrl": String
  }

```
## Login Endpoints
For this endpoint, minimum data requirements are as follows
```
 {
	"email":String,
	"password": String
 }
```
## voting endpoints
For this endpoint, minimum data requirements are as follows

```
{
	"candidate":integer
}
```


## Technologies used
- 1. Pytests for running tests
- 2. Flask python framework
- 3. PyJWT

##Deploy
https://heroku-politicalv2.herokuapp.com

## Author
Allan Maina

## Credits
This api was build as a part of andela cycle 37 challenge
