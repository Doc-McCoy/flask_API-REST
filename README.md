# flask_API-REST

API simples feita em Python usando flask, seguindo [este](https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask) tutorial.

Trata-se de uma lista todo, onde você pode visualisar, inserir, editar, e apagar tasks.

Necessita de user e senha para autenticação.

Exemplos de uso:

- Visualisar todas as tasks:
`curl -u renan:python -i http://localhost:5000/todo/api/v1.0/tasks/`

- Visualisar a task com um id específico: `curl -u renan:python -i http://localhost:5000/todo/api/v1.0/tasks/<id>`

- Criar uma task: `curl -u renan:python -i -H "Content-Type: application/json" -X POST -d '{"title":"Read a book"}' http://localhost:5000/todo/api/v1.0/tasks`

- Update em uma task: `curl -u renan:python -i -H "Content-Type: application/json" -X PUT -d '{"done":true}' http://localhost:5000/todo/api/v1.0/tasks/<id>`

- Apagar uma task: `curl -u renan:python -i -H "Content-Type: application/json" -X DELETE -d '{"done":true}' http://localhost:5000/todo/api/v1.0/tasks/<id>`
