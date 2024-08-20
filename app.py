from flask import Flask, render_template, request
import psycopg2

app = Flask(__name__)


@app.route('/')
def index():

    x = getListsData()
    return render_template('lists.html',lists=x)


@app.route('/list')
def lists():
    listdata = getIndividualListData()
    listID = request.args.get('id')

    return render_template('list view.html')


def getListsData():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM movielist""")
    lists = cursor.fetchall()
    listDictionary = [lists]
    return(listDictionary)

def getIndividualListData():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM movielist WHERE movielist."movielistID" = 4""")
    lists = cursor.fetchone()
    listDictionary = {}
    listDictionary['movielistID']=lists[0]
    listDictionary['title']=lists[1]
    listDictionary['url']=lists[2]
    moviedata = cursor.execute("""SELECT movie."movieID", movie.title, movie.watches FROM movie JOIN movie_movielist ON movie."movieID"=movie_movielist."movieID" JOIN movielist ON movielist."movielistID"=movie_movielist."movielistID" WHERE movielist."movielistID" = %s;""", (4,))
    listDictionary['movies']=cursor.fetchall()
    print(listDictionary)
    return(listDictionary)


def get_db_connection():
    conn = psycopg2.connect(
        host='localhost',
        database='postgres',
        user='postgres',
        password='bossbaby'
    )
    return conn


if __name__ == '__main__':
    app.run(debug=True)