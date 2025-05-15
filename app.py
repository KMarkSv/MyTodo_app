from flask import Flask, render_template, request, redirect, url_for  # Importing necessary modules from Flask / Импорт необходимых модулей из Flask
from datetime import datetime  # Importing datetime to handle timestamps / Импорт datetime для работы с временными метками
from config import Config  # Importing configuration settings from the Config object / Импорт конфигурационных настроек из объекта Config
from model import Todo, db  # Importing the Todo model and db instance for database interaction / Импорт модели Todo и экземпляра db для взаимодействия с базой данных

app = Flask(__name__)  # Create a Flask application instance / Создание экземпляра приложения Flask
app.config.from_object(Config)  # Load configuration from the Config class / Загрузка конфигурации из класса Config
db.init_app(app)  # Initialize the database with the app / Инициализация базы данных с приложением

# Create the necessary database tables if they don't already exist / Создание необходимых таблиц в базе данных, если они ещё не существуют
with app.app_context():  # Ensures this happens within the Flask app context / Убедиться, что всё происходит в контексте приложения Flask
    db.create_all()  # Create all tables defined by SQLAlchemy models (Todo) / Создать все таблицы, определённые в моделях SQLAlchemy (например, Todo)

@app.route("/", methods=["GET", "POST"])  # Defining the route for the home page / Определение маршрута для главной страницы
def index():
    if request.method == "POST":  # Check if the request is a POST request (form submission) / Проверка, является ли запрос POST-запросом (отправка формы)
        title = request.form.get("title")  # Get the title from the form / Получить заголовок из формы
        desc = request.form.get("desc")  # Get the description from the form / Получить описание из формы
        if title and desc:  # Ensure both title and description are provided / Убедиться, что и заголовок, и описание заполнены
            new_todo = Todo(title=title, desc=desc, date_created=datetime.now())  # Create a new Todo object / Создать новый объект Todo
            db.session.add(new_todo)  # Add the new todo to the session / Добавить новую задачу в сессию
            db.session.commit()  # Commit the session to save the new todo to the database / Подтвердить транзакцию для сохранения задачи в базе данных
            return redirect(url_for("index"))  # Redirect to the home page after adding the todo to avoid form resubmission / Перенаправить на главную страницу после добавления задачи, чтобы избежать повторной отправки формы

    # Fetch all todos from the database, ordered by the date created (most recent first) / Получить все задачи из базы данных, отсортированные по дате создания (сначала самые новые)
    all_todos = Todo.query.order_by(Todo.date_created.desc()).all()
    return render_template("index.html", all_todos=all_todos)  # Render the home page with the todos / Отобразить главную страницу со списком задач



@app.route("/update/<int:sno>", methods=["GET", "POST"])  # Defining the route for updating a specific todo / Определение маршрута для обновления конкретной задачи
def update(sno):
    todo = Todo.query.get_or_404(sno)  # Get the todo by its serial number (sno), or return a 404 if not found / Получить задачу по её идентификатору или вернуть 404, если не найдена
    if request.method == "POST":  # Check if the request is a POST request (form submission) / Проверка, является ли запрос POST-запросом (отправка формы)
        todo.title = request.form.get("title")  # Update the title with the new value from the form / Обновить заголовок новым значением из формы
        todo.desc = request.form.get("desc")  # Update the description with the new value from the form / Обновить описание новым значением из формы
        db.session.commit()  # Commit the changes to the database / Подтвердить изменения в базе данных
        return redirect(url_for("index"))  # Redirect to the home page after updating the todo / Перенаправить на главную страницу после обновления задачи

    return render_template("update.html", todo=todo)  # Render the update page with the current todo information / Отобразить страницу обновления с текущими данными задачи

@app.route("/delete/<int:sno>")  # Defining the route for deleting a specific todo / Определение маршрута для удаления конкретной задачи
def delete(sno):
    todo = Todo.query.get_or_404(sno)  # Get the todo by its serial number (sno), or return a 404 if not found / Получить задачу по её идентификатору или вернуть 404, если не найдена
    db.session.delete(todo)  # Delete the todo from the session / Удалить задачу из сессии
    db.session.commit()  # Commit the deletion to the database / Подтвердить удаление в базе данных
    return redirect(url_for("index"))  # Redirect to the home page after deletion / Перенаправить на главную страницу после удаления задачи

@app.route('/about')  # Defining the route for the About page / Определение маршрута для страницы "О нас"
def about():
    return render_template('about.html')  # Render the about page / Отобразить страницу "О нас"

if __name__ == "__main__":  # Check if the script is run directly / Проверка, запущен ли скрипт напрямую
    app.run(debug=True)  # Start the Flask application in debug mode (auto reload on code changes) / Запустить приложение Flask в режиме отладки (автоматическая перезагрузка при изменении кода)
