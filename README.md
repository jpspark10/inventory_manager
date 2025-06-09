# 📦 Inventory Manager

Инвентаризационное веб-приложение на Flask с поддержкой:
- регистрации и логина пользователей
- добавления, редактирования и удаления предметов
- отслеживания действий через лог-систему
- REST API с авторизацией по API-ключу

## 🚀 Возможности

- 👤 Аутентификация через Flask-Login
- 📝 Журнал изменений с привязкой к пользователю
- 🔑 API с защитой по `x-api-key`
- 🌐 Веб-интерфейс + JSON API

---

## 🛠 Установка

```bash
sudo apt update && sudo apt install python3-venv git -y
git clone https://github.com/jpspark10/inventory-manager.git
cd inventory-manager
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py
```
---

## 🔐 Работа с API
### Получение API-ключа
1. Зарегистрируйся и войди в веб-интерфейс.

2. Перейди на страницу /auth/api_key и сгенерируй ключ.

Пример запроса к API.
```bash
curl -H "x-api-key: YOUR_API_KEY" http://localhost:5000/api/logs
```
