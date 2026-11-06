-- Включаем поддержку внешних ключей (обязательно для SQLite)
PRAGMA foreign_keys = ON;

-- Таблица пользователей
CREATE TABLE IF NOT EXISTS Users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('applicant', 'operator', 'executor', 'admin'))
);

-- Справочник статусов
CREATE TABLE IF NOT EXISTS Statuses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);

-- Справочник категорий (с иерархией parent_id)
CREATE TABLE IF NOT EXISTS Categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    parent_id INTEGER,
    FOREIGN KEY (parent_id) REFERENCES Categories(id) ON DELETE SET NULL
);

-- Таблица заявок
CREATE TABLE IF NOT EXISTS Requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    number TEXT UNIQUE NOT NULL, -- Формат #YYYY-NNNN
    title TEXT NOT NULL,
    description TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    deadline DATETIME,
    
    -- Внешние ключи
    author_id INTEGER NOT NULL,
    assignee_id INTEGER,
    status_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    
    FOREIGN KEY (author_id) REFERENCES Users(id) ON DELETE CASCADE,
    FOREIGN KEY (assignee_id) REFERENCES Users(id) ON DELETE SET NULL,
    FOREIGN KEY (status_id) REFERENCES Statuses(id),
    FOREIGN KEY (category_id) REFERENCES Categories(id)
);

-- Таблица комментариев
CREATE TABLE IF NOT EXISTS Comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    author_id INTEGER NOT NULL,
    request_id INTEGER NOT NULL,
    
    FOREIGN KEY (author_id) REFERENCES Users(id) ON DELETE CASCADE,
    FOREIGN KEY (request_id) REFERENCES Requests(id) ON DELETE CASCADE
);

-- Таблица вложений
CREATE TABLE IF NOT EXISTS Attachments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT NOT NULL,
    filepath TEXT NOT NULL,
    mime_type TEXT,
    size INTEGER,
    
    request_id INTEGER NOT NULL,
    
    FOREIGN KEY (request_id) REFERENCES Requests(id) ON DELETE CASCADE
);

-- Триггер для автоматического обновления даты изменения заявки
CREATE TRIGGER IF NOT EXISTS update_request_timestamp
AFTER UPDATE ON Requests
FOR EACH ROW
BEGIN
    UPDATE Requests SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;