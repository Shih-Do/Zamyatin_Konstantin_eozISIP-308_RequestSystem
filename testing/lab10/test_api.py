import pytest
from fastapi.testclient import TestClient
from src.main import app

# Создаем тестовый клиент, который обращается к нашему приложению напрямую
client = TestClient(app)

# ==========================================
# 1. ТЕСТЫ БИЗНЕС-ЛОГИКИ И ОСНОВНЫХ ФУНКЦИЙ (Минимум 3)
# ==========================================

def test_create_request_generates_number():
    """Проверяем, что при создании заявки генерируется уникальный номер формата #YYYY-NNNN"""
    response = client.post("/api/v1/requests/", json={
        "title": "Тест генерации номера",
        "category_id": 1,
        "author_id": 1,
        "priority": "Средний"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["number"].startswith("#202")
    assert len(data["number"]) == 10 # #YYYY-NNNN

def test_get_all_requests():
    """Проверяем получение списка заявок"""
    response = client.get("/api/v1/requests/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_update_request_status():
    """Проверяем смену статуса заявки (бизнес-процесс)"""
    # Сначала создадим заявку
    create_resp = client.post("/api/v1/requests/", json={
        "title": "Тест смены статуса", "category_id": 1, "author_id": 1
    })
    req_id = create_resp.json()["id"]
    
    # Меняем статус на 2 (В работе)
    update_resp = client.patch(f"/api/v1/requests/{req_id}", json={"status_id": 2})
    assert update_resp.status_code == 200
    assert update_resp.json()["status_id"] == 2

# ==========================================
# 2. ТЕСТЫ API (Минимум 3: успех, ошибка ввода, отсутствие)
# ==========================================

def test_api_success_creation():
    """Успешный запрос: создание заявки"""
    response = client.post("/api/v1/requests/", json={
        "title": "Успешный API тест", "category_id": 1, "author_id": 1
    })
    assert response.status_code == 201

def test_api_bad_input():
    """Ошибочный ввод: передача строки вместо числа в category_id"""
    response = client.post("/api/v1/requests/", json={
        "title": "Ошибка", "category_id": "abc", "author_id": 1
    })
    assert response.status_code == 422

def test_api_missing_resource():
    """Отсутствующий ресурс: получение заявки по ID, которого нет"""
    response = client.get("/api/v1/requests/99999")
    assert response.status_code == 404

# ==========================================
# 3. ТЕСТЫ ВАЛИДАЦИИ И НЕГАТИВНЫЕ (Минимум 2)
# ==========================================

def test_validation_empty_title():
    """Отсутствие обязательного поля title"""
    response = client.post("/api/v1/requests/", json={
        "category_id": 1, "author_id": 1
    })
    assert response.status_code == 422

def test_validation_short_title():
    """Граничное значение: слишком короткий title (меньше 3 символов)"""
    response = client.post("/api/v1/requests/", json={
        "title": "ab", "category_id": 1, "author_id": 1
    })
    assert response.status_code == 422

# ==========================================
# 4. РЕГРЕССИОННЫЕ ТЕСТЫ (Минимум 2)
# ==========================================

def test_regression_filter_by_status():
    """Регрессия: проверяем, что фильтрация по статусу не сломалась"""
    response = client.get("/api/v1/requests/?status_id=1")
    assert response.status_code == 200
    data = response.json()
    for req in data:
        assert req["status_id"] == 1

def test_regression_get_users():
    """Регрессия: проверяем, что справочник пользователей доступен"""
    response = client.get("/api/v1/users")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_health_check():
    """Проверка Health-check"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"