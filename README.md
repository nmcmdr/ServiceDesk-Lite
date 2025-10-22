# ServiceDesk-Lite
Это REST API для системы учета заявок, разработанный на Django и Django REST Framework.

## Функционал

- Регистрация и JWT-аутентификация пользователей.
- CRUD-операции для заявок (Tickets) и комментариев (Comments).
- Ролевая модель доступа (`user`, `admin`). Только автор или администратор могут изменять и удалять заявки.
- Фильтрация заявок по статусу.
- Полнотекстовый поиск по заголовку и описанию.
- Сортировка по дате создания и статусу.
- Пагинация для списков объектов.
- Ограничение частоты запросов (throttling).
- Интерактивная документация API (Swagger/ReDoc).
- Проект полностью контейнеризован с помощью Docker.

## Стек технологий

- Python 3.11
- Django 4.2
- Django REST Framework
- PostgreSQL 15
- Docker & Docker Compose
- djangorestframework-simplejwt (JWT)
- drf-yasg (Swagger)
- pytest (для тестирования)


## Установка и запуск

### Запуск через Docker (рекомендуемый способ)

1.  **Клонируйте репозиторий:**
    ```bash
    git clone <URL_репозитория>
    cd servicedesk_lite
    ```

2.  **Запустите Docker Compose:**
    ```bash
    docker-compose up --build
    ```
    Эта команда соберет образы, запустит контейнеры веб-приложения и базы данных, а также выполнит миграции.

3.  **Создайте суперпользователя (администратора):**
    ```bash
    docker-compose exec web python manage.py createsuperuser
    ```
    Следуйте инструкциям в терминале.

4.  **Назначьте роль администратора:**
    Зайдите в админ-панель (`/admin/`), найдите созданного пользователя и в поле `Role` установите значение `admin`.

Проект будет доступен по следующим адресам:
-   **API:** `http://localhost:8000/api/`
-   **Swagger UI:** `http://localhost:8000/swagger/`
-   **Админ-панель:** `http://localhost:8000/admin/`

---

## Тестовые учетные данные

-   **Admin:**
    -   **username:** `admin_user` (или тот, которого вы создали)
    -   **password:** `password123`
    -   *Необходимо создать через `createsuperuser` и назначить роль `admin`.*

-   **User:**
    -   **username:** `testuser`
    -   **password:** `password123`
    -   *Можно зарегистрировать через API.*

---

## Примеры API-запросов

**Базовый URL:** `http://localhost:8000/api`

### 1. Регистрация пользователя

**POST** `/api/auth/register/`

```json
{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123",
    "password2": "password123"
}
```

### 2. Получение JWT токена (вход)

**POST** `/api/auth/login/`

```json
{
    "username": "testuser",
    "password": "password123"
}
```
*Из ответа скопируйте `access` токен для использования в последующих запросах.*

### 3. Создание заявки

**POST** `/api/tickets/`

**Headers:** `Authorization: Bearer <access_token>`

```json
{
    "title": "Проблема с доступом к сетевому диску",
    "description": "Сетевой диск 'Shared' не открывается, запрашивает пароль."
}
```

### 4. Фильтрация и поиск заявок

**GET** `/api/tickets/?status=in_progress&search=диск&ordering=-created_at`

**Headers:** `Authorization: Bearer <access_token>`

### 5. Добавление комментария

**POST** `/api/tickets/{id}/comments/`

**Headers:** `Authorization: Bearer <access_token>`

```json
{
    "text": "Перезагрузка компьютера не решила проблему."
}
```
