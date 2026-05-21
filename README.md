Django Task Manager
A simple open-source task manager built with Django.

The system allows users to organize their work using workspaces, projects, and tasks.

This project is still under development but is already functional and usable.

Features
Workspace management
Project organization inside workspaces
Task creation and management
Basic task tracking structure
Django-based backend
Project Structure
The application is organized in three main layers:

Workspace – top-level container for organizing work
Project – belongs to a workspace and groups related tasks
Task – individual work items inside projects
This structure makes it easy to scale the system and manage multiple projects efficiently.

Tech Stack
Python
Django
SQLite (default database)
Installation
Clone the repository:


git clone https://github.com/njannati1991/django-task_manager.git
Move into the project directory:


cd django-task-manager
Create a virtual environment:
python -m venv venv

Activate the virtual environment:
Linux / macOS:
source venv/bin/activate

Windows:
venv\Scripts\activate

Install dependencies:
pip install -r requirements.txt

Run migrations:
python manage.py migrate

Start the development server:
python manage.py runserver

Open in browser:
http://127.0.0.1:8000

Current Status
The project is not fully finished yet, but the core structure is implemented and usable.
Future improvements will include more features and refinements.


Contributions are welcome.
If you have suggestions, improvements, or bug fixes, feel free to open an issue or submit a pull request.

License
This project is open-source and available under the MIT License.
