# app.py
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)

# Connect to MongoDB Atlas
client = MongoClient("mongodb+srv://user2:12345@cluster0.htjod7q.mongodb.net/?retryWrites=true&w=majority")
db = client.todoapp

@app.route('/')
def index():
    tasks = db.tasks.find()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    task = request.form.get('task')
    db.tasks.insert_one({'task': task, 'done': False})
    return redirect(url_for('index'))

@app.route('/complete/<string:task_id>')
def complete(task_id):
    db.tasks.update_one({'_id': ObjectId(task_id)}, {'$set': {'done': True}})
    return redirect(url_for('index'))

@app.route('/delete/<string:task_id>')
def delete(task_id):
    db.tasks.delete_one({'_id': ObjectId(task_id)})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)