# ServiceDesk-Lite
ServiceDesk Lite API
Это REST API для системы учета заявок, разработанный на Django и Django REST Framework.

Функционал
-Регистрация и JWT-аутентификация пользователей.
-CRUD-операции для заявок (Tickets) и комментариев (Comments).
-Ролевая модель доступа (user, admin). Только автор или администратор могут изменять и удалять заявки.
-Фильтрация заявок по статусу.
-Полнотекстовый поиск по заголовку и описанию.
-Сортировка по дате создания и статусу.
-Пагинация для списков объектов.
-Ограничение частоты запросов (throttling).
-Интерактивная документация API (Swagger/ReDoc).
-Проект полностью контейнеризован с помощью Docker.


Стек технологий
-Python 3.11
-Django 4.2
-Django REST Framework
-PostgreSQL 15
-Docker & Docker Compose
-djangorestframework-simplejwt (JWT)
-drf-yasg (Swagger)
-pytest (для тестирования)
