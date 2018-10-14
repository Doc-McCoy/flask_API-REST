#!python3
from flask import Flask, jsonify, abort, make_response, request, url_for
from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy

app  = Flask(__name__)
auth = HTTPBasicAuth()

# Informaçoes do banco de dados para o SQLAlchemy fazer a conexao
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="DocMcCoy",
    password="senha123",
    hostname="DocMcCoy.mysql.pythonanywhere-services.com",
    databasename="DocMcCoy$tasks",
)
# Configuracoes do SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Instanciar o DB
db = SQLAlchemy(app)

# Classe que sera armazenada no banco, com seus respectivos campos
class Tasks(db.Model):
    __tablename__   = "tasks"
    id              = db.Column(db.Integer, primary_key=True)
    title           = db.Column(db.VARCHAR(length=50), nullable=False)
    description     = db.Column(db.TEXT(), nullable=True)
    done            = db.Column(db.Integer(), nullable=False)

def make_public_task(task):
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_task', task_id=task['id'], _external=True)
        else:
            new_task[field] = task[field]
    return new_task

@app.route('/todo/api/v1.0/tasks/')
@auth.login_required
def get_tasks():
    # return jsonify({'tasks': [make_public_task(task) for task in tasks]})
    return jsonify(Tasks.query.all())

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
@auth.login_required
def get_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    return jsonify({'tasks' : task[0]})

@app.route('/todo/api/v1.0/tasks', methods=['POST'])
@auth.login_required
def create_task():
    if not request.json or not 'title' in request.json:
        abort(404)
    task = {
        'id'            : tasks[-1]['id'] + 1,
        'title'         : request.json['title'],
        'description'   : request.json.get('description', ""),
        'done'          : False,
    }
    tasks.append(task)
    return jsonify({'task' : task}), 201

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
@auth.login_required
def update_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify({'task': task[0]})

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
@auth.login_required
def delete_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    return jsonify({'result': True})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error' : 'Not found'}), 404)

@auth.get_password
def get_password(username):
    if username == 'renan':
        return 'python'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

if __name__ == '__main__':
    app.run()
