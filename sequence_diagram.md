@startuml
title UML-диаграмма последовательности Сайт "База доступных видеоигр"

actor Пользователь
participant "Интерфейс\n(браузер)" as UI
participant "Flask-сервер" as Server
participant "UserService"
participant "GameService"
database "БД (SQLite)" as DB

== Регистрация ==
Пользователь -> UI : Открывает форму регистрации
UI -> Пользователь : Отображает поля (почта, логин, пароль)
Пользователь -> UI : Вводит данные
UI -> Server : POST /register (email, username, password)
Server -> UserService : Проверить почту (на уникальность)
UserService -> DB : SELECT * FROM users WHERE email=email
DB --> UserService : [есть/нет]
alt почта уже есть в базе, но с другим логином
    Server -> UI : Ошибка "почта уже используется"
else новая почта
    UserService -> UserService : hashPassword()
    UserService -> DB : INSERT INTO users(email, username, hashed_password)
    DB --> UserService : OK
    Server -> UI : Перенаправление на /login
end

== Вход ==
Пользователь -> UI : Открывает форму входа, вводит логин и пароль
UI -> Server : POST /login (username, password)
Server -> UserService : Проверить логин и пароль
UserService -> DB : SELECT * FROM users WHERE username=username
DB --> UserService : user data
alt Неверные данные
    Server -> UI : Ошибка "Неверные данные"
else Успешный вход
    Server -> UI : Перенаправление на главную страницу
end

== Главная страница ==
UI -> Server : GET /
Server -> UI : Отображает описание, ссылки: “Игры”, “Вход”, “Регистрация” / “Добавить игру”, “Выйти”

== Каталог игр и поиск ==
Пользователь -> UI : Переходит в “Игры”
UI -> Server : GET /games
Server -> GameService : Получить список игр (с фильтрацией по поиску)
GameService -> DB : SELECT * FROM games [WHERE title LIKE ...]
DB --> GameService : список игр
Server -> UI : Список игр (названия, ссылки)

== Просмотр информации об игре ==
Пользователь -> UI : Кликает по названию игры
UI -> Server : GET /game/<id>
Server -> GameService : Получить данные игры
GameService -> DB : SELECT * FROM games WHERE id=id
DB --> GameService : данные игры
Server -> UI : Отображает детальную информацию

== Добавление новой игры ==
Пользователь -> UI : Открывает форму “Добавить игру”
UI -> Пользователь : Форма (название, жанр, ссылка, доступность, детали)
Пользователь -> UI : Заполняет и отправляет
UI -> Server : POST /add-game (поля)
Server -> GameService : Проверить и сохранить игру
GameService -> DB : INSERT INTO games (...)
DB --> GameService : OK
Server -> UI : Перенаправление в каталог

== Редактирование и удаление игры ==
Пользователь -> UI : Открывает свою игру
UI -> Server : GET /edit-game/<id>
Server -> GameService : Проверить права, получить данные
GameService -> DB : SELECT * FROM games WHERE id=id
DB --> GameService : данные
UI -> Пользователь : Отображает форму для редактирования
Пользователь -> UI : Вносит правки
UI -> Server : POST /edit-game/<id> (поля)
Server -> GameService : Проверить права, обновить
GameService -> DB : UPDATE games SET ... WHERE id=id
DB --> GameService : OK
Server -> UI : Перенаправление на игру

Пользователь -> UI : Нажимает “Удалить”
UI -> Server : POST /delete-game/<id>
Server -> GameService : Проверить права, удалить
GameService -> DB : DELETE FROM games WHERE id=id
DB --> GameService : OK
Server -> UI : Перенаправление в каталог

== Восстановление пароля ==
Пользователь -> UI : Открывает “Забыли пароль?”
UI -> Пользователь : Форма почта
Пользователь -> UI : Вводит почту
UI -> Server : POST /forgot-password (email)
Server -> UserService : Проверить почту
UserService -> DB : SELECT * FROM users WHERE email=email
DB --> UserService : [есть/нет]
alt почта найдена
    Server -> UI : Сообщение "Письмо отправлено"
else Не найден
    Server -> UI : Сообщение "Пользователь не найден"
end

== Выход ==
Пользователь -> UI : Нажимает “Выйти”
UI -> Server : GET /logout
Server -> UI : Перенаправление на главную страницу

@enduml
