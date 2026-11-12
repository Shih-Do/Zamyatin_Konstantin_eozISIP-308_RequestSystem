# Тест-кейсы для RequestSystem (ЛР №9)

| ID | Название | Тип | Шаги / Входные данные | Ожидаемый результат | Фактический результат | Статус |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | Создание заявки с валидными данными | Позитивный | POST /api/v1/requests/ <br> `{"title": "Test request", "category_id": 1, "author_id": 1, "priority": "Средний"}` | 201 Created | 201 Created | PASS |
| 2 | Создание заявки с title длиной 3 символа | Граничный | POST /api/v1/requests/ <br> `{"title": "abc", "category_id": 1, "author_id": 1}` | 201 Created | 201 Created | PASS |
| 3 | Создание заявки с title длиной 100 символов | Граничный | POST /api/v1/requests/ <br> `{"title": "<100 символов>", "category_id": 1, "author_id": 1}` | 201 Created | 201 Created | PASS |
| 4 | Создание заявки с title длиной 2 символа | Граничный негативный | POST /api/v1/requests/ <br> `{"title": "ab", "category_id": 1, "author_id": 1}` | 422 Unprocessable Entity | 422 Unprocessable Entity | PASS |
| 5 | Создание заявки с title длиной 101 символ | Граничный негативный | POST /api/v1/requests/ <br> `{"title": "<101 символ>", "category_id": 1, "author_id": 1}` | 422 Unprocessable Entity | 422 Unprocessable Entity | PASS |
| 6 | Создание заявки без поля title | Негативный | POST /api/v1/requests/ <br> `{"category_id": 1, "author_id": 1}` | 422 Unprocessable Entity | 422 Unprocessable Entity | PASS |
| 7 | Создание заявки без поля category_id | Негативный | POST /api/v1/requests/ <br> `{"title": "Test", "author_id": 1}` | 422 Unprocessable Entity | 422 Unprocessable Entity | PASS |
| 8 | Создание заявки без поля author_id | Негативный | POST /api/v1/requests/ <br> `{"title": "Test", "category_id": 1}` | 422 Unprocessable Entity | 422 Unprocessable Entity | PASS |
| 9 | Создание заявки без поля priority | Негативный | POST /api/v1/requests/ <br> `{"title": "Test", "category_id": 1, "author_id": 1}` | 201 Created | 201 Created | PASS |
| 10 | Создание заявки с title не строкового типа | Негативный | POST /api/v1/requests/ <br> `{"title": 123, "category_id": 1, "author_id": 1}` | 422 Unprocessable Entity | 422 Unprocessable Entity | PASS |
| 11 | Создание заявки с category_id не числового типа | Негативный | POST /api/v1/requests/ <br> `{"title": "Test", "category_id": "abc", "author_id": 1}` | 422 Unprocessable Entity | 422 Unprocessable Entity | PASS |
| 12 | Получение списка заявок без фильтров | Позитивный | GET /api/v1/requests/ | 200 OK | 200 OK | PASS |
| 13 | Получение списка заявок с фильтром по status_id | Позитивный | GET /api/v1/requests/?status_id=1 | 200 OK | 200 OK | PASS |
| 14 | Получение списка заявок с поиском q | Позитивный | GET /api/v1/requests/?q=test | 200 OK | 200 OK | PASS |
| 15 | Получение списка заявок с неверным типом status_id | Негативный | GET /api/v1/requests/?status_id=abc | 422 Unprocessable Entity | 422 Unprocessable Entity | PASS |
| 16 | Получение заявки по существующему ID | Позитивный | GET /api/v1/requests/1 | 200 OK | 200 OK | PASS |
| 17 | Получение заявки по несуществующему ID | Негативный | GET /api/v1/requests/9999 | 404 Not Found | 404 Not Found | PASS |
| 18 | Изменение статуса существующей заявки | Позитивный | PATCH /api/v1/requests/1 <br> `{"status_id": 2}` | 200 OK | 200 OK | PASS |
| 19 | Изменение несуществующей заявки | Негативный | PATCH /api/v1/requests/9999 <br> `{"status_id": 2}` | 404 Not Found | 404 Not Found | PASS |
| 20 | Архивация существующей заявки | Позитивный | DELETE /api/v1/requests/1 | 204 No Content | 204 No Content | PASS |