from flask import Flask, jsonify, request

app = Flask(__name__)
tasks = []
task_counter = 1

# Create a new task
@app.route('/v1/tasks', methods=['POST'])
def create_task():
    global task_counter

    data = request.get_json()
    title = data.get('title')

    task = {'id': task_counter, 'title': title, 'is_completed': False}
    tasks.append(task)

    task_counter += 1

    return jsonify({'id': task['id']}), 201

# List all tasks
@app.route('/v1/tasks', methods=['GET'])
def list_tasks():
    formatted_tasks = [{'id': task['id'], 'title': task['title'], 'is_completed': task['is_completed']} for task in tasks]
    return jsonify({'tasks': formatted_tasks}), 200

# Get a specific task
@app.route('/v1/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = next((task for task in tasks if task['id'] == task_id), None)

    if task:
        return jsonify({'id': task['id'], 'title': task['title'], 'is_completed': task['is_completed']}), 200
    else:
        return jsonify({'error': 'There is no task at that id'}), 404

# Delete a specific task
@app.route('/v1/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks

    tasks = [task for task in tasks if task['id'] != task_id]

    return '', 204

# Edit the title or completion of a specific task
@app.route('/v1/tasks/<int:task_id>', methods=['PUT'])
def edit_task(task_id):
    data = request.get_json()
    title = data.get('title')
    is_completed = data.get('is_completed')

    for task in tasks:
        if task['id'] == task_id:
            task['title'] = title
            task['is_completed'] = is_completed
            return '', 204

    return jsonify({'error': 'There is no task at that id'}), 404

# Extra Credit: Bulk add tasks
@app.route('/v1/tasks/bulk', methods=['POST'])
def bulk_add_tasks():
    global task_counter

    data = request.get_json()
    new_tasks = data.get('tasks')

    inserted_ids = []
    for task_data in new_tasks:
        task = {'id': task_counter, 'title': task_data.get('title'), 'is_completed': task_data.get('is_completed')}
        tasks.append(task)
        inserted_ids.append({'id': task['id']})
        task_counter += 1

    return jsonify({'tasks': inserted_ids}), 201

# Extra Credit: Bulk delete tasks
@app.route('/v1/tasks/bulk', methods=['DELETE'])
def bulk_delete_tasks():
    global tasks

    data = request.get_json()
    task_ids = [task.get('id') for task in data.get('tasks')]

    tasks = [task for task in tasks if task['id'] not in task_ids]

    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
