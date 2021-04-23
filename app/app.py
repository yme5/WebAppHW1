from typing import List, Dict
import simplejson as json
from flask import Flask, request, Response, redirect
from flask import render_template
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor

app = Flask(__name__)
mysql = MySQL(cursorclass=DictCursor)

app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = 'treesData'
mysql.init_app(app)


@app.route('/', methods=['GET'])
def index():
    user = {'username': 'Yousuf'}
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblTreesImport')
    result = cursor.fetchall()
    return render_template('index.html', title='Home', user=user, trees=result)

@app.route('/view/<int:tree_id>', methods=['GET'])
def record_view(tree_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblTreesImport WHERE id=%s', tree_id)
    result = cursor.fetchall()
    return render_template('view.html', title='View Form', tree=result[0])

@app.route('/api/v1/trees', methods=['GET'])
def api_browse() -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblTreesImport')
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp

@app.route('/trees/new', methods=['GET'])
def form_insert_get():
    return render_template('new.html', title='New Tree Form')

@app.route('/trees/new', methods=['POST'])
def form_insert_post():
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('id'), request.form.get('Girth_in'), request.form.get('Height_ft'),
                 request.form.get('Volume_ft_3'))
    sql_insert_query = """INSERT INTO tblTreesImport (id,Girth_in,Height_ft,Volume_ft_3) VALUES (%s, %s,%s, %s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)

if __name__ == '__main__':
    app.run(host='0.0.0.0')