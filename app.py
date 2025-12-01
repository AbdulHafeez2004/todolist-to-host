from flask import Flask, render_template, request, redirect, url_for

# Initialize the Flask application
app = Flask(__name__)

# In-memory storage for todos (for demo purposes)
# This list holds all todo items as dictionaries with id, task, and completed status
todos = [
    {"id": 1, "task": "Learn Flask", "completed": False},
    {"id": 2, "task": "Build a todo app", "completed": True},
    {"id": 3, "task": "Style with CSS", "completed": False}
]

# Route for the home page
# This displays all todos using the index.html template
@app.route('/')
def index():
    # Render the index.html template and pass the todos list to it
    return render_template('index.html', todos=todos)

# Route to add a new todo item
# Only accepts POST requests (form submissions)
@app.route('/add', methods=['POST'])
def add_todo():
    # Check if the request method is POST
    if request.method == 'POST':
        # Get the task text from the form data
        task = request.form.get('task')
        
        # Only add the todo if task is not empty
        if task:
            # Generate a new unique ID by finding the maximum existing ID and adding 1
            # If todos list is empty, default to 0
            new_id = max([todo['id'] for todo in todos], default=0) + 1
            
            # Append the new todo item to the todos list
            todos.append({
                "id": new_id,
                "task": task,
                "completed": False  # New todos are always uncompleted
            })
    
    # Redirect back to the home page to show the updated list
    return redirect(url_for('index'))

# Route to toggle the completion status of a todo
# Takes the todo_id as a parameter from the URL
@app.route('/complete/<int:todo_id>')
def complete_todo(todo_id):
    # Loop through all todos to find the one with matching id
    for todo in todos:
        if todo['id'] == todo_id:
            # Toggle the completed status (True becomes False, False becomes True)
            todo['completed'] = not todo['completed']
            break  # Exit loop once the todo is found and updated
    
    # Redirect back to the home page
    return redirect(url_for('index'))

# Route to delete a todo item
# Takes the todo_id as a parameter from the URL
@app.route('/delete/<int:todo_id>')
def delete_todo(todo_id):
    global todos  # Access the global todos list
    
    # Create a new list excluding the todo with the matching id
    # This effectively removes the todo from the list
    todos = [todo for todo in todos if todo['id'] != todo_id]
    
    # Redirect back to the home page
    return redirect(url_for('index'))

# Route to edit an existing todo
# Accepts both GET (to display edit form) and POST (to save changes)
@app.route('/edit/<int:todo_id>', methods=['GET', 'POST'])
def edit_todo(todo_id):
    # Find the todo with the matching id using next()
    # Returns None if no matching todo is found
    todo = next((todo for todo in todos if todo['id'] == todo_id), None)
    
    # If todo doesn't exist, redirect to home page
    if not todo:
        return redirect(url_for('index'))
    
    # Handle POST request (when form is submitted)
    if request.method == 'POST':
        # Get the new task text from the form
        new_task = request.form.get('task')
        
        # Update the todo's task if new_task is not empty
        if new_task:
            todo['task'] = new_task
        
        # Redirect back to home page after saving changes
        return redirect(url_for('index'))
    
    # Handle GET request (display the edit form)
    # Render the edit.html template and pass the todo to be edited
    return render_template('edit.html', todo=todo)

# Run the Flask application
# This is only executed when the script is run directly (not imported)
if __name__ == '__main__':
    # Run the app in debug mode (provides detailed error messages and auto-reloads)
    app.run(debug=True)