
# BlogNest

**BlogNest** is a modular full-stack web application developed using the Flask framework. This project is a blog application that allows users to create, read, update, and delete blog posts. The backend is built following RESTful API principles, while the frontend uses HTML, CSS, and JavaScript.

## Technologies Used

### Backend:
- Python
- Flask
- SQLAlchemy
- SQLite
- Flask-Mail
- Flask-RESTx
- Flask-JWT-Extended

### Frontend:
- JavaScript
- HTML/CSS

## About the Project

The main objective of **BlogNest** is to create a modern backend API that securely handles user authentication and authorization for a blog platform. Key features of the project include:

- Flask factory pattern is used for application instance creation.
- Modular structure for easy scalability and maintainability.
- ORM (Object Relational Mapping) is used with SQLAlchemy for database interactions.
- DTO (Data Transfer Object) pattern is used to transfer data between frontend and backend.
- Business logic is separated using services, ensuring a clean architecture.
- An API layer handles requests and responses efficiently.
- Custom exception handlers manage errors and exceptions gracefully.
- User authentication and authorization are managed using JWT tokens.
- Custom decorators enhance user authentication and authorization handling.

## Features

- User registration and login
- JWT-based user authentication and authorization
- Blog post CRUD (Create, Read, Update, Delete) operations
- Comment CRUD operations on blog posts
- Favoriting blog posts and viewing favorites
- Liking blog posts and tracking total likes
- Viewing the latest liked blog posts
- Searching blog posts by title and category
- Searching users by username and viewing their posts
- User profile management
- Password reset and email verification via Flask-Mail
- 20+ endpoints for various API operations
- Simple frontend UI for the blog
- Swagger UI for API documentation

## Docker Setup for Development

1. Clone the repository:
   ```bash
   git clone https://github.com/tarikalim/BlogNest.git
   ```

2. Create a `.env` file in the root directory based on the example provided in `.env.example`.

3. Build the Docker image:
   ```bash
   docker build -t blognest .
   ```

4. Run the Docker container:
   ```bash
   docker run -d --env-file .env -p 5000:5000 blognest
   ```

## Step-by-Step Installation (without Docker)

This project was developed using:

```
Python 3.12.0
```

1. Clone the repository:
   ```bash
   git clone $repository_link
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   .\venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables by creating a `.env` file in the root directory based on `.env.example`.

5. Start the application:
   ```bash
   flask run
   ```

## Usage

- Swagger UI is available at: `http://localhost:5000`
- Blog application is available at: `http://localhost:5000/static/index.html`

## Additional Notes

- Example database is provided in the repository for easier testing.
- Flask’s built-in server is used for development purposes only and is not suitable for production.
