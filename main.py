from flask import Flask, render_template
import util

# create an application instance
# all requests it receives from clients to this object for handling
# we are instantiating a Flask object by passing __name__ argument to the Flask constructor. 
# The Flask constructor has one required argument which is the name of the application package. 
# Most of the time __name__ is the correct value. The name of the application package is used 
# by Flask to find static assets, templates and so on.
app = Flask(__name__)

# evil global variables
# can be placed in a config file
# here is a possible tutorial how you can do this
username='shannengeller'
password='test'
host='127.0.0.1'
port='5432'
database='dvdrental'

# route is used to map a URL with a Python function
# complete address: ip:port/
# 127.0.0.1:5000/
@app.route('/')
# this is how you define a function in Python
def index():
    # this is your index page
    # connect to DB
    cursor, connection = util.connect_to_db(username,password,host,port,database)
    # execute SQL commands
    record = util.run_and_fetch_sql(cursor, "Select fruit_a, fruit_b from basket_a, basket_b;")
    if record == -1:
        # you can replace this part with a 404 page
        print('Something is wrong with the SQL command')
    else:
        # this will return all column names of the select result table
        # ['customer_id','store_id','first_name','last_name','email','address_id','activebool','create_date','last_update','active']
        col_names = [desc[0] for desc in cursor.description]
        # only use the first five rows
        log = record[:5]
        # log=[[1,2],[3,4]]
    # disconnect from database
    util.disconnect_from_db(connection,cursor)
    # using render_template function, Flask will search
    # the file named index.html under templates folder
    return render_template('index.html', sql_table = log, table_title=col_names)


@app.route('/api/update_basket_a')
def add_cherry():
    cursor, connection = util.connect_to_db(username,password,host,port,database)
    # execute SQL commands
    record = util.run_and_commit_sql(cursor, connection ,"INSERT INTO basket_a (a, fruit_a)VALUES (5,'Cherry');")
    if record == -1:
        # you can replace this part with a 404 page
        print('Errors in SQL command')
    else:
        log = 'Success'
        connection.commit()

    # disconnect from database
    util.disconnect_from_db(connection,cursor)
    # using render_template function, Flask will search
    # the file named index.html under templates folder
    return render_template('api/update_basket_a.html', log_html = log)
    

@app.route('/api/unique')
def unique():
    cursor, connection = util.connect_to_db(username,password,host,port,database)
    # execute SQL commands
    record = util.run_and_fetch_sql(cursor, "select fruit_a, fruit_b from basket_a Full Outer Join basket_b on basket_a.fruit_a=basket_b.fruit_b Where basket_a.a is NULL or basket_b.b is Null")
    if record == -1:
        print('Errors in SQL command')
    else:
        connection.commit()
        column_names = [desc[0] for desc in cursor.description]
        log = record[:5]
        util.disconnect_from_db(connection,cursor)
        return render_template('api/unique.html', sql_table = log, table_title=column_names)

    

if __name__ == '__main__':
	# set debug mode
    app.debug = True
    # your local machine ip
    ip = '127.0.0.1'
    app.run(host=ip)
