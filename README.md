
---

# 📝 TO DO LIST

This project is a task management application where users can create, edit, delete, and view tasks. The app includes authentication and role-based access control (RBAC) to manage permissions and user roles.

🔗 [**Trello Board**](https://trello.com/w/espaciodetrabajo21533214)

## 🚀 Features

### 🔐 User Authentication & Management
- **User Registration and Login**: Users can register and log in with an email and password.
- **JWT Authentication**: JSON Web Tokens (JWT) manage session authentication.
- **User Roles**: The roles "Regular User" and "Administrator" control access to various functions.

### 📝 Task Management
- **Create Tasks**: Users can create tasks with a title, description, due date, and status (to-do, in-progress, completed).
- **Edit Tasks**: Users can update information for existing tasks.
- **Delete Tasks**: Users can delete specific tasks.
- **List Tasks**: Users can view all their tasks with options to filter by status and due date.

### 🔒 Role-Based Access Control (RBAC)
- **Restricted Access**: Regular users can only view and manage their own tasks.
- **Admin Permissions**: Admins can manage all users' tasks and edit or delete registered users.

### 🌟 Additional Features
- **Change History**: A log of changes for each task (creation, edits, status changes).
- **Favorite Tasks**: Users can mark tasks as "Favorites" to highlight them in their list.

## ⚙ Project Requirements

### 📌 Core Technologies
- **Backend**: Python / FastAPI 
- **Database**: MySQL
- **Authentication**: JWT implementation

### 📋 Additional Requirements
- **Version Control**: Git and GitHub for code management.
- **Code Quality**: Pylint (Python) or ESLint (JavaScript) to ensure code quality.
- **Documentation**: Clear instructions to deploy the project and configure JWT and database.

## 👥 Roles and Permissions

| Role            | Permissions                                                                       |
|-----------------|-----------------------------------------------------------------------------------|
| Regular User    | Create, view, edit, and delete their own tasks                                    |
| Administrator   | Create, view, edit, and delete tasks for all users; manage registered users       |

## 🔧 Installation and Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/STXVXN06/To-do-List.git
   ```
2. Navigate to the project directory:
   ```bash
   cd To-do-List
   ```
3. **Activate the virtual environment:**
   ```bash
   python -m venv venv
   ```
   Then, activate the environment:
   ```bash
   # Windows:
   venv\Scripts\activate

   # macOS/Linux:
   source venv/bin/activate
   ```
4. Navigate to the app directory:
   ```bash
   cd FastAPI/app
   ```
5. Install project dependencies:
   ```bash
   pip install -r requirements.txt
   ```
6. Navigate back to the project root directory:
   ```bash
   cd ../..  # Goes two levels up
   ```

7. Start the Docker containers:
   ```bash
   docker-compose up --build
   ```
8. Run database migrations:
   ```bash
   docker-compose exec fastapi alembic upgrade head
   ```

*IMPORTANT:* If the migration command fails for any reason, try running it with `sudo`:
   ```bash
   sudo docker-compose exec fastapi alembic upgrade head
   ```
Here's the final addition to the README with details on backend navigation, port information, and a recommendation to use Postman:

---

## 🌐 Backend Navigation

- **Database**: Accessible on port **8080**
- **Swagger UI**: Accessible on port **8000** for API documentation and testing.

You can explore and test all functionalities directly from the Swagger UI on port 8000. Alternatively, it’s recommended to use **Postman** for more detailed API testing and request management.

--- 
