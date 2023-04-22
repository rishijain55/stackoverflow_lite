import os
from flask import Flask
import psycopg2
#render template
from flask import render_template
#from queries.py file, import queries dictornary
from .queries import queries
from datetime import datetime
from dateutil.relativedelta import relativedelta



def get_db_connection():
    conn = psycopg2.connect(
        host="10.17.50.91",
        database="group_9",
        user="group_9",
        password="6xKbIOpdFFobZr"
    )
    return conn

def create_app():
    app=Flask(__name__)
    # I just want to connect to the remote db on server
    conn = get_db_connection()
    cursor = conn.cursor()

    @app.route('/')
    def welcome():
        #fetch data from db and return
        #What was the date one year ago?
        one_year_ago = datetime.now() - relativedelta(years=1)
        cursor.execute(queries["welcome"], (one_year_ago,))
        rows = cursor.fetchall()

        #print rows in terminal
        for row in rows:
            print(row)

        return '''
        <h1> Welcome to StackOverflow </h1>
        '''
        return render_template('test.html', rows=rows)
    
    @app.route('/test')
    def test():
        cursor.execute("SELECT * FROM votes")
        rows = cursor.fetchall()
        return render_template('test.html', rows=rows)
    

    
    #close the connection
    return app

app=create_app()
    

