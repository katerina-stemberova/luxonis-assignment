from flask import Flask, render_template
import psycopg2

# create an instance of the Flask class using the name of the application’s module or package
app = Flask(__name__)

# what URL should trigger our function
@app.route("/")
def get_data():
    # connect to the postgres DB
    conn = psycopg2.connect(
        host="postgres",
        user="scrapy",
        password="scrapy",
        dbname="template1"
    )
    cursor = conn.cursor()
    # get the data we are interested in...
    cursor.execute("SELECT title, url FROM sreality")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    # ...and feed them to the webpage that will be displayed to the user
    # on localhost on port defined in docker-compose.yml
    return render_template('sreality_template.html', data=data)


if __name__ == '__main__':
    # externally visible server
    app.run(host='0.0.0.0', port=5000)
