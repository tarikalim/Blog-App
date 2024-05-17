# BlogApp

This project is a attempt to develop moduler full stack web application with Python and Flask. The project is a blog
application that allows users to create, read, update, and delete blog posts. Backend developed using RESful API principle and
frontend developed using HTML, CSS, and JavaScript.

## Technologies Used
Backend:
- Python
- Flask
- SQLAlchemy
- SQLite
- Marshmallow
- Flask-Mail
- Flask-Migrate
- Flask-RESTx
- Flask-JWT-Extended
- Swagger UI

Frontend:
- HTML
- CSS
- JavaScript

## About the Project
- Main objective of the project is to develop a modern backend API that securely handles user authentication and authorization for
a blog application.
- Flask factory pattern is used to create the application instance.
- The project is developed with a modular structure that allows for easy scaling and maintenance. 
- ORM (Object Relational Mapping) is used to interact with the database.
- DTO (Data Transfer Object) pattern is used to transfer data between the frontend and backend.
- Services are used to handle business logic and separate it from the controllers.
- API layer is used to handle requests and responses.
- Specified exception handlers are used to handle exceptions and errors.
- Custom decorators are used to handle user authentication and authorization.
- JWT (JSON Web Token) is used to securely handle user authentication and authorization.
## Features
- User registration and login
- User authentication and authorization
- Create, read, update, and delete blog posts
- Create, read, update, and delete comments on blog posts
- Favorite blog posts and view favorite blog posts
- Like blog posts and view liked blog posts
- Search blog posts by title and category
- User profile management
- User password reset and email verification
- 28 different endpoints for the API
- Simple UI for the blog application
- Swagger UI for API documentation


## Step by Step Installation

This project developed with

```
Pyton 3.12.0
```

Clone repository with following command in your terminal:

```bash
git clone $repository_link
```

Create environment to run code

```bash
python3 -m venv venv
```

Use the package manager [pip](https://pip.pypa.io/en/stable/) to run requirements file.

```bash
pip install -r requirements.txt
```
* Create a .env file in the root directory of the project and add the environment variables given in the .env.example file.


* To instructor run and test the project, necessary environment variables are provided in the submission. Please use them.


* Ensure that your code editor or IDE is set to use the Python interpreter from the virtual environment. This setting is
usually found in the preferences or settings menu under "Python Interpreter" or similar. Choose the interpreter located
inside your virtual environment directory.

## Usage

After you set the environment variables, you can run the project with the following command:

```bash
python3 app.py
```
* You can access the Swagger UI documentation at http://localhost:5000/ and test the API endpoints.


* You can access the blog application at http://localhost:5000/static/index.html and test the frontend.



