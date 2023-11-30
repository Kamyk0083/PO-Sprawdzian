from flask import Flask, Response, request, jsonify, abort
import json

app = Flask(__name__)
users_file = 'users.json'

def read_users():
    try:
        with open(users_file, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def write_users(users):
    with open(users_file, 'w') as file:
        json.dump(users, file, indent=4)

@app.get("/users")
def get_users() -> Response:
    users = read_users()
    return jsonify(users), 200

@app.get("/users/<int:user_id>")
def get_user(user_id: int) -> Response:
    users = read_users()
    user = next((u for u in users if u['id'] == user_id), None)
    if user is None:
        abort(404)
    return jsonify(user), 200

@app.post("/users")
def create_user() -> Response:
    users = read_users()
    user = request.json
    if 'name' not in user or 'lastname' not in user:
        abort(400)
    new_id = max([u['id'] for u in users], default=0) + 1
    user['id'] = new_id
    users.append(user)
    write_users(users)
    return jsonify(user), 201

@app.patch("/users/<int:user_id>")
def update_user(user_id: int) -> Response:
    users = read_users()
    user = next((u for u in users if u['id'] == user_id), None)
    if user is None:
        abort(400)
    data = request.json
    user.update(data)
    write_users(users)
    return '', 204

@app.put("/users/<int:user_id>")
def replace_user(user_id: int) -> Response:
    users = read_users()
    user = next((u for u in users if u['id'] == user_id), None)
    data = request.json
    if 'name' not in data or 'lastname' not in data:
        abort(400)
    if user:
        user.update(data)
    else:
        data['id'] = user_id
        users.append(data)
    write_users(users)
    return '', 204

@app.delete("/users/<int:user_id>")
def delete_user(user_id: int) -> Response:
    users = read_users()
    if any(u for u in users if u['id'] == user_id):
        users = [u for u in users if u['id'] != user_id]
        write_users(users)
        return '', 204
    else:
        abort(400)

if __name__ == '__main__':
    app.run(debug=True)
