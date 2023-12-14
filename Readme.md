# Stackoverflow Lite Web Application
Welcome to the Stackoverflow Lite web application! This is a simple web application built with Flask and PostgreSQL, designed to provide a platform for asking and answering questions.

## Installation

### Database Setup
Download the data_dump.sql file from this link: https://drive.google.com/file/d/1EjQhs0AanazTOaf4_AI2ZqkQ-TPJsAAZ/view?usp=sharing

Initialize the PostgreSQL database by running the following command in your terminal:

```yaml
psql -U <your_postgres_user> -d <your_database_name> <   <path to data dump>/data_dump.sql
```

Replace your_postgres_user with your PostgreSQL username and your_database_name with the desired database name.


After running the SQL dump file, you can verify that the table has been created by querying the database. For example:

```
\dt
```
This should display the tables in the database.


### Clone the repository

### Create a virtual environment and install the dependencies

Using a virtual environment helps isolate your project's dependencies using conda or venv. Open a terminal or command prompt and navigate to your project directory:

```yaml
# Create a virtual environment
conda create --name stackoverflow_lite python=3.10
# Activate the virtual environment
conda activate stackoverflow_lite
```

Next, cd into flask_app and install the dependencies:

```yaml
pip install -r requirements.txt
```
Change the database credentials in the routes.py file to match your database credentials.

Now, you can run the application:

```yaml
export FLASK_APP=stackoverflow_lite.py
export FLASK_ENV=development
flask run
```


<!-- Note -->
## Note
>To read about the functioning and sql queries, read the report stackoverflow_lite_report.pdf
