new_project/
├── bot/
│   ├── handlers/
│   │   ├── __init__.py
│   │   ├── auth_handlers.py         # Авторизация и привязка аккаунта
│   │   ├── password_handlers.py     # Сброс пароля
│   │   └── states.py                # Состояния FSM
│   ├── services/
│   │   ├── __init__.py
│   │   ├── database.py              # Работа с SQLite (если нужно логировать пользователей/запросы)
│   │   ├── ldap_service.py          # Взаимодействие с Active Directory
│   │   └── email_service.py         # Отправка email с кодами/паролями
│   └── main.py                      # Точка входа
├── logs/
│   └── password_reset.log           # Логи работы бота
├── .env                             # Конфигурация окружения
├── docker-compose.yml               # Оркестрация контейнеров
├── Dockerfile                       # Конфигурация Docker
└── requirements.txt                 # Зависимости Python





ПЕРЕИМЕНУЙТЕ e.nenv в .env

'
🖥 Локальный запуск (без Docker)
1. Требования:
Python 3.9+

Установленные зависимости:

bash
Копировать
Редактировать
pip install -r requirements.txt
2. Настройка окружения:
Создайте .env файл на основе .env.example

Заполните переменные:

ini
Копировать
Редактировать
TOKEN=ваш_токен_бота
LDAP_SERVER=ваш_ldap_сервер
LDAP_BIND_USER=логин_администратора_AD
LDAP_BIND_PASSWORD=пароль_администратора_AD
LDAP_BASE_DN=dc=example,dc=com

SMTP_USER=ваш_email@gmail.com
SMTP_PASSWORD=пароль_приложения_email
Важно:
В main.py нужно указать SMTP-сервер, например:

python
Копировать
Редактировать
'SMTP_SERVER': "smtp.office365.com"
Также:

Email-аккаунт должен быть настроен с двухфакторной аутентификацией (2FA/MFA)

Используйте пароль приложения, а не обычный пароль

3. Запуск бота:
bash
python -m bot.main

🚀 Продакшен-развертывание
1. Требования:
Сервер с установленным Docker и Docker Compose

Доступ к Active Directory по LDAPS (порт 636)

SSL-сертификаты для защищённого подключения

2. Настройка LDAPS:
Установите SSL-сертификат от AD-сервера на сервер с ботом

Убедитесь, что порт 636 открыт

В .env укажите FQDN сервера:

ini
LDAP_SERVER=dc01.example.com

3. Запуск через Docker:
bash
docker-compose up -d --build

4. Рекомендации по инфраструктуре:
Настройте systemd-сервис, если работаете вне Docker

Используйте nginx как reverse proxy для TLS (если требуется внешний доступ)

Обновляйте SSL-сертификаты регулярно

⚠ Важные примечания
Работа с AD:
Используется LDAPS (обязательно, для безопасного подключения)

Указанный в .env пользователь AD должен иметь права на сброс паролей

Политики безопасности AD должны позволять установку паролей, которые генерирует бот

Безопасность:
Используйте отдельный сервисный аккаунт AD для бота

Ограничьте доступ к .env

Настройте ротацию логов (например, через logrotate)

Минимизируйте права SMTP- и LDAP-учёток

Мониторинг:
Следите за логом logs/password_reset.log

Внедрите оповещения при ошибках подключения к LDAP/SMTP

Можно дополнительно отправлять алерты в Telegram/Slack при сбоях

