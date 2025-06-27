# FastAPI Todo App Developed By Avishek Das

Usrs can add, edit, list and delete Todo. JWT authentication for user login.
***

## Technologies Used
+ FastAPI
+ PostgreSQL
+ SQLAlchemy
+ Alembic

## Running locally
* Clone the Github repository

		git clone https://github.com/davishek7/fastapi-todo-app

* Create and activate virtual environment

		cd fatapi-todo-app
		python3 -m venv env
		source env/bin/activate

* Install dependencies using pip

      pip install requirements.txt

* Copy the .env.example file to .env and change the values

      cp .env.example .env

* Running the dev server

      uvicorn app.main:app
