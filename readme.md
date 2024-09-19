# BlogNest

This project is a attempt to develop moduler full stack web application with Flask framework. The project is a blog
application that allows users to create, read, update, and delete blog posts. Backend developed using RESful API
principle and
frontend developed using HTML, CSS, and JavaScript.

## Technologies Used

Backend:

- Python
- Flask
- SQLAlchemy
- SQLite
- Flask-Mail
- Flask-RESTx
- Flask-JWT-Extended

Frontend:

- JavaScript

## About the Project

- Main objective of the project is to develop a modern backend API that securely handles user authentication and
  authorization for
  a blog application.
- Flask factory pattern is used to create the application instance.
- The project is developed with a modular structure that allows for easy scaling and maintenance.
- ORM (Object Relational Mapping) is used to interact with the database.
- DTO (Data Transfer Object) pattern is used to transfer data between the frontend and backend.
- Services are used to handle business logic and separate it from the API layer.
- API layer is used to handle requests and responses.
- Specified exception handlers are used to handle exceptions and errors.
- Custom decorators are used to handle user authentication and authorization.

## Features

- User registration and login
- User authentication and authorization with JWT
- Create, read, update, and delete blog posts
- Create, read, update, and delete comments on blog posts
- Favorite blog posts and view favorite blog posts
- Like blog posts and view total likes
- See the latest liked blog posts
- Search blog posts by title and category
- Search users by username and view their posts
- User profile management
- User password reset and email verification with Flask-Mail
- 30 different endpoints for the API
- Simple UI for the blog application
- Swagger UI for API documentation

## Step by Step Installation

This project developed with:

```
Pyton 3.12.0
```

Clone repository with following command in your terminal:

```bash
git clone $repository_link
```

Create environment and activate it:

```bash
python3 -m venv venv
.\venv\Scripts\activate
```

Use the package manager [pip](https://pip.pypa.io/en/stable/) to run requirements file.

```bash
pip install -r requirements.txt
```

* Create a .env file in the root directory of the project and add the environment variables given in the .env.example
  file.


* To instructor run and test the project, necessary environment variables are provided in the submission. Please use
  them.


* Ensure that your code editor or IDE is set to use the Python interpreter from the virtual environment. This setting is
  usually found in the preferences or settings menu under "Python Interpreter" or similar. Choose the interpreter
  located
  inside your virtual environment directory.

## Usage

After you set the environment variables and install the requirements, Write the following command in the project root

```bash
flask run
```

Application will run your local server. You can access the application with the following URLs:

* Swagger UI is available at: http://localhost:5000


* Blog application is available at: http://localhost:5000/static/index.html

## Additional Notes

* To make testing process easier, example database is provided in the repository. You can use it to test the project.


* Provided server is not suitable for production. It is only for testing purposes provided by Flask.



