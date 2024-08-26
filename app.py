from flask import Flask, render_template, request
import psycopg2
import sorting
from scraping import scrape_list

app = Flask(__name__)


@app.route('/')
def index():

    x = getListsData()
    return render_template('lists.html',lists=x)

@app.route('/scraping', methods=['POST'])
def scrape():
    print("asdfoiupqwieotujeqwklas;chfioauf;lkj")
    listurl = request.json['listurl']
    #listurl = request.json['url']
    movies = scrape_list(listurl)
    insert_list(movies)
    return "{}"

def insert_list(movies):
    print("akldjfals;dfjioqwepurlkfdjs;akl")
    print(movies)
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        print(movies["title"])
        print(movies["url"])

        cursor.execute("""INSERT INTO movielist (title, url)
                       VALUES (%s, %s)
                       ON CONFLICT (url)
                       DO UPDATE
                       SET title = EXCLUDED.title
                       RETURNING "movielistID";""", (movies["title"], movies["url"]))
        
        movie_list_id = cursor.fetchone()[0]
        cursor.execute("""DELETE FROM movie_movielist WHERE "movielistID" = %s;""", (movie_list_id))
        for movie in movies["movies"]:
            cursor.execute("""INSERT INTO movie (title, watches)
                           VALUES (%s, %s)
                           ON CONFLICT (title)
                           DO UPDATE
                           SET watches = EXCLUDED.watches
                           RETURNING "movieID";""", (movie.title, movie.watches))





        conn.commit()


        
        
    except Exception as e:
        conn.rollback()
        print(f"An error occurred: {e}")
    finally:
        cursor.close()
        conn.close()

@app.route('/list')
def test():
    listID = request.args.get('id')
    list = getIndividualListData(listID)

    return render_template('list view.html',list=list)

@app.route('/sort', methods=['POST'])
def sort():
    listID = request.args.get('id')
    list = getIndividualListData(listID)
    sorting.sortfilms(list['movies'])
    return list['movies']

def getListsData():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM movielist""")
    lists = cursor.fetchall()
    listDictionary = [lists]
    return(listDictionary)

def getIndividualListData(listID):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM movielist WHERE movielist."movielistID" = %s;""", (listID,))
    lists = cursor.fetchone()
    listDictionary = {}
    listDictionary['movielistID']=lists[0]
    listDictionary['title']=lists[1]
    listDictionary['url']=lists[2]
    cursor.execute("""SELECT movie."movieID", movie.releasedate, movie.title, movie.watches FROM movie JOIN movie_movielist ON movie."movieID"=movie_movielist."movieID" JOIN movielist ON movielist."movielistID"=movie_movielist."movielistID" WHERE movielist."movielistID" = %s;""", (listID,))
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


#original_list = [{'movieID': '3', 'title': 'Elio', 'watches': '175'}, {'movieID': '4', 'title': 'John Wick Presents: Ballerina', 'watches': '350'}]
#sorted_list = [{'movieID': '4', 'title': 'John Wick Presents: Ballerina', 'watches': '350'}, {'movieID': '3', 'title': 'Elio', 'watches': '175'}]

def calculate_differences(original_list, sorted_list):
    original_indices = {movie["movieID"]: i for i, movie in enumerate(original_list)}
    print(original_indices)
    differences = []
    for new_index, movie in enumerate(sorted_list):
        movieID = movie["movieID"]
        print(movieID)
        if movieID in original_indices:
            original_index = original_indices[movieID]
            difference = new_index - original_index
            differences.append(difference)
        else:
            differences.append(None)
    return differences

def generate_changelog(original_list, differences):
    result = ""
    result += "Gained places:\n"
    for i in range(0, len(original_list)):
        if(differences[i]>0):
            result += original_list[i]["title"] + " +" + str(differences[i]) + " \n"

    result += "Lost places:\n"
    for i in range(0, len(original_list)):
        if(differences[i]<0):
            result += original_list[i]["title"] + " " + str(differences[i]) + " \n"
    print(result)
    
#differences = calculate_differences(original_list, sorted_list)
#print(differences)
#generate_changelog(original_list, differences)


if __name__ == '__main__':
    app.run(debug=True)