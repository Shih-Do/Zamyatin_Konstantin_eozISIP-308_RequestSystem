-- Очищаем данные (если пересоздаем)
DELETE FROM Attachments;
DELETE FROM Comments;
DELETE FROM Requests;
DELETE FROM Users;
DELETE FROM Statuses;
DELETE FROM Categories;

-- Сброс счетчиков (для красоты ID)
DELETE FROM sqlite_sequence;

-- Вставляем статусы
INSERT INTO Statuses (name) VALUES 
('Новая'), ('В работе'), ('Выполнена'), ('Закрыта');

-- Вставляем категории (пример иерархии)
INSERT INTO Categories (name, parent_id) VALUES 
('Оборудование', NULL),
('Принтер', 1),
('Компьютер', 1),
('Доступы', NULL),
('Пароль', 4);

-- Вставляем пользователей
INSERT INTO Users (name, email, password_hash, role) VALUES 
('Администратор', 'admin@system.ru', 'hash1', 'admin'),
('Оператор', 'operator@system.ru', 'hash2', 'operator'),
('Исполнитель', 'executor@system.ru', 'hash3', 'executor'),
('Студент', 'student@system.ru', 'hash4', 'applicant');

-- Вставляем заявки (номер генерируем вручную для примера)
INSERT INTO Requests (number, title, description, author_id, assignee_id, status_id, category_id) VALUES 
('#2026-0001', 'Не печатает принтер', 'Нужна замена картриджа', 4, 3, 1, 2),
('#2026-0002', 'Забыл пароль от почты', 'Восстановление доступа', 4, 2, 2, 5);

-- Комментарии
INSERT INTO Comments (text, author_id, request_id) VALUES 
('Принят в работу, проверю картридж', 3, 1),
('Пароль сброшен, проверьте почту', 2, 2);

-- Вложения
INSERT INTO Attachments (filename, filepath, mime_type, size, request_id) VALUES 
('error_log.txt', '/storage/1.txt', 'text/plain', 1024, 1);