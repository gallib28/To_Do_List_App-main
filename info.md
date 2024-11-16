# To-Do List App Development Roadmap

## 1. Planning and Setup
**Objective**: Host the app on your Raspberry Pi (RPI) and enable user authentication.

### Server Setup:
- Install an operating system on the RPI (e.g., Raspbian OS).
- Install and configure MySQL Server to manage the database on the RPI.
- Set up a web server (e.g., Apache or Nginx) to handle HTTP requests.

## 2. Database Design

### Tables:
- **users**: Contains user details (user ID, username, hashed password).
- **tasks**: Contains task information (task ID, task name, description, due date, task type, task status).
- **sub_tasks**: Inherits from tasks (sub-task ID, parent task ID, sub-task description).

### Relationships:
- One-to-many relationship between `users` and `tasks`.
- One-to-many relationship between `tasks` and `sub_tasks`.

### Steps:
1. Create your database schema in MySQL with tables: `users`, `tasks`, `sub_tasks`.
2. Add relationships and constraints (e.g., `FOREIGN KEY` for user-task, task-sub-task relationships).

## 3. Backend (Python)
**Objective**: Handle user authentication, task management, and interaction with the database.

### Framework: 
Use Flask or Django to build the backend API.

### Tasks:

#### User Authentication:
- Implement user registration and login functionality (password hashing and storage using libraries like `bcrypt`).
- Create session management or JWT tokens for logged-in users.

#### Task Management:
- Implement APIs to allow users to view, create, update, and delete tasks.
- Create functions for managing sub-tasks under tasks.

#### Database Operations:
- Write functions for SQL queries: `INSERT`, `SELECT`, `UPDATE`, and `DELETE` for tasks and sub-tasks.

## 4. Frontend (HTML/CSS/JavaScript)
**Objective**: Design the user interface for task management and interaction.

### Design Components:

- **Login Page**: Simple form to input username and password.
- **Task Overview Page**:
  - List of tasks associated with the logged-in user.
  - Each task will show details like due date, description, and a list of sub-tasks.
- **Task Creation/Editing Page**:
  - Form to add or edit tasks and sub-tasks.
  - Options for task type and status selection.
- **Sub-task Management**:
  - Display sub-tasks under each task, with options to add, edit, or delete them.

### JavaScript Features:
- Use Fetch API or AJAX to communicate with the backend (retrieve task lists, create new tasks, etc.).
- Form validation on the client side.
- Use `localStorage` or `sessionStorage` for managing sessions if you don’t implement JWT on the frontend.

## 5. Application Logic and Flow

### User Authentication Logic:
- On login, verify user credentials and create a session (JWT or session token).
- Restrict task management actions to the logged-in user’s tasks.

### Task Management Logic:

#### Viewing Tasks:
- On the dashboard, display the tasks related to the current user.
- Fetch the data from the backend (using the user’s ID stored in the session).

#### Creating/Editing Tasks:
- Use forms to allow users to add new tasks, with fields for task name, due date, description, type, and status.
- Allow adding sub-tasks within tasks using dynamic form fields.

#### Updating Task Status:
- Allow users to mark tasks as complete/incomplete by toggling the status field.

### Data Validation:
- Backend validation for all form inputs (e.g., task due date, task name length).
- Check that tasks belong to the logged-in user before allowing updates or deletion.

## 6. Testing

### Unit Tests:
- Write tests for each API endpoint (e.g., login, task creation, task viewing).
- Ensure correct user authentication and task ownership validation.

### Frontend Tests:
- Test that all forms (login, task creation) work as expected.
- Ensure that tasks and sub-tasks are displayed correctly for each user.

## 7. Deployment

### Server Setup:
- Deploy your Flask/Django app to the RPI.
- Set up MySQL to work with your backend.
- Use `gunicorn` (Flask) or `uWSGI` (Django) as the WSGI server, and configure Nginx to serve the frontend.

### Domain & SSL:
- Purchase a domain (optional) and configure DNS to point to your RPI.
- Install an SSL certificate using Let's Encrypt for HTTPS.

## 8. Maintenance

### Error Logging:
- Set up error logging for the backend (using libraries like `loguru` or `logging` in Python).

### Backups:
- Automate MySQL database backups (e.g., using cron jobs on the RPI).
