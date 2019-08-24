# Python Training Project

This is a training project to understand how to structure a python project and learn about various libs, connecting to db, making POST request and other important concepts that we should keep in mind while while writing a flask application.

Application is expected to meet below requirements:

* /register endpoint which will be post request and takes argument as username, password, email, and phone.
* /login endpoint which will take username and password and sends a token back to user if it is correct.
* /users if token is correct send and display all the user details.

Application is expected to have proper:
* Logging
* Monitoring
* Tests

Let's name this learning project as pythontraining.

# Starting app
To start the Flask application please follow below steps
* git clone `git@github.com:GarimaDamani/user_registration_python.git`
* Create a virtualenv inside pythontraining directory. Installation steps [here](https://medium.com/@garimajdamani/https-medium-com-garimajdamani-installing-virtualenv-on-ubuntu-16-04-108c366e4430)
* Execute the below steps

```
cd pythontraining
pip3 install -r requirements.txt
export FLASK_APP=run.py
export FLASK_ENV=development
flask run
```
* Visit http://127.0.0.1:5000

# Todo
* Writing test cases
* Monitoring

