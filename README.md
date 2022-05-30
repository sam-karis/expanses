# Expenses API

[Postman Documentation](https://documenter.getpostman.com/view/4000258/Uz5DocTx)

|Endpoints and methods      | Functionality
|---------------------------|---------------------------------------
|/ (GET)                    |Index
|/expanses_data(GET)        |Get expenses details with filter and sort by
|/aggregates(GET)           |Get expenses aggregates by (department, memberName", project, date)

**Prequisites**

```
Python - version 3.6.8
Postgress database
postman - To run various endponts
```

Perform the following simple steps:

- Git clone the this repository  
- Set up a virtual eniviroment and Install the apps dependencies by running the following commands
```
python -m venv .venv
python -m pip install -r requirements.txt
```
- Create postgres database and set all environment variables defined in the `env.example` by creating a `.env`

- To create database tables run  
```
flask db upgrade
```
- To seed data from `expanses.csv` into the database 
```
flask data seed
```
- To run the application
```
flask run
```
