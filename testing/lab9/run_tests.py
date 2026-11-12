import requests
import json

# Вставьте сюда ваш публичный URL из Codespaces (без /docs в конце)
BASE_URL = "http://127.0.0.1:8000/api/v1/requests"

def run_test(test_id, name, method, url_suffix, payload=None, expected_status=200):
    url = f"{BASE_URL}{url_suffix}"
    
    if method == "POST":
        response = requests.post(url, json=payload)
    elif method == "GET":
        response = requests.get(url)
    elif method == "PATCH":
        response = requests.patch(url, json=payload)
    elif method == "DELETE":
        response = requests.delete(url)
        
    actual_status = response.status_code
    status_text = "PASS" if actual_status == expected_status else "FAIL"
    
    print(f"[{status_text}] TC-{test_id:02d}: {name} | Ожидали: {expected_status}, Получили: {actual_status}")
    return status_text

print("--- ЗАПУСК ТЕСТОВ ---")

# 1. Создание (валидные данные)
run_test(1, "Создание заявки (валид)", "POST", "/", {"title": "Test request", "category_id": 1, "author_id": 1, "priority": "Средний"}, 201)

# 2-5. Граничные значения title
run_test(2, "Title 3 символа", "POST", "/", {"title": "abc", "category_id": 1, "author_id": 1}, 201)
run_test(3, "Title 100 символов", "POST", "/", {"title": "a"*100, "category_id": 1, "author_id": 1}, 201)
run_test(4, "Title 2 символа", "POST", "/", {"title": "ab", "category_id": 1, "author_id": 1}, 422)
run_test(5, "Title 101 символ", "POST", "/", {"title": "a"*101, "category_id": 1, "author_id": 1}, 422)

# 6-9. Отсутствие полей
run_test(6, "Без title", "POST", "/", {"category_id": 1, "author_id": 1}, 422)
run_test(7, "Без category_id", "POST", "/", {"title": "Test", "author_id": 1}, 422)
run_test(8, "Без author_id", "POST", "/", {"title": "Test", "category_id": 1}, 422)
run_test(9, "Без priority", "POST", "/", {"title": "Test", "category_id": 1, "author_id": 1}, 201)

# 10-11. Неверные типы данных
run_test(10, "Title не строка", "POST", "/", {"title": 123, "category_id": 1, "author_id": 1}, 422)
run_test(11, "Category_id не число", "POST", "/", {"title": "Test", "category_id": "abc", "author_id": 1}, 422)

# 12-15. GET запросы
run_test(12, "Получить все заявки", "GET", "/", None, 200)
run_test(13, "Фильтр по статусу", "GET", "/?status_id=1", None, 200)
run_test(14, "Поиск по тексту", "GET", "/?q=test", None, 200)
run_test(15, "Неверный тип status_id", "GET", "/?status_id=abc", None, 422)

# 16-20. Операции с конкретным ID
# (Используем ID=1, предполагая, что он существует)
run_test(16, "Получить заявку по ID=1", "GET", "/1", None, 200)
run_test(17, "Получить несуществующую ID=9999", "GET", "/9999", None, 404)
run_test(18, "Изменить статус ID=1", "PATCH", "/1", {"status_id": 2}, 200)
run_test(19, "Изменить несуществующую ID=9999", "PATCH", "/9999", {"status_id": 2}, 404)
run_test(20, "Архивировать ID=1", "DELETE", "/1", None, 204)

print("--- ТЕСТИРОВАНИЕ ЗАВЕРШЕНО ---")