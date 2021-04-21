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

if __name__ == '__main__':
    app.run(host='0.0.0.0')