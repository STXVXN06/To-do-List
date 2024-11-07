
# 📝 TO DO LIST

This project aims to develop a task management application where users can create, edit, delete, and view tasks. The app includes authentication and role-based access control (RBAC) to manage permissions and users.

🔗 [**Trello Board**](https://trello.com/w/espaciodetrabajo21533214)

## 🚀 Features

### 🔐 User Authentication & Management
- **User Registration and Login**: Users can register and log in with an email and password.
- **JWT Authentication**: JSON Web Tokens (JWT) are used to manage session authentication.
- **User Roles**: The roles "Regular User" and "Administrator" control access to different functions.

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

## ⚙️ Project Requirements

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
   cd FastApi
   ```
3. Configure environment variables for the database and JWT.
4. Install dependencies and run the server.
5. 
   For FastAPI:
   ```bash
   pip install -r requirements.txt
   uvicorn main:app --reload
   ```

---
