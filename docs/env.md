## 📁 Инструкция по созданию файлов окружения `env.dev` и `env.prod`

Проект использует разделение переменных окружения по модулям: `backend`, `frontend` и `database`. Для каждого из них необходимо создать два файла окружения:

* `.env.dev` — переменные для среды **разработки**
* `.env.prod` — переменные для **продакшн-среды**

Файлы должны быть расположены в соответствующих папках модулей.

---

### 📂 Backend - [example](../backend/.env.example)

**Расположение файлов:**

```
backend/.env.dev  
backend/.env.prod
```

**Пример содержимого `backend/.env.dev`:**

```dotenv
# Подключение к базе данных Postgres
DATABASE_URL=postgresql+asyncpg://postgres:password@db:5432/mydatabase
DATABASE_DROP_ALL=true
DATABASE_ECHO=true

# URL внешних сервисов
ARBITR_URL=https://kad.arbitr.ru  
COOKIE_SERVICE_URL=http://cookie:8041

# Разрешённые источники для CORS
FRONTEND_ORIGINS=http://localhost,http://localhost:3000

# Настройки JWT
SECRET_KEY=dev_secret_key
ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=5
REFRESH_TOKEN_EXPIRE_DAYS=30
```

**Пример содержимого `backend/.env.prod`:**

```dotenv
# Подключение к базе данных Postgres
DATABASE_URL=postgresql+asyncpg://user:secure_password@db:5432/prod_db
DATABASE_DROP_ALL=false
DATABASE_ECHO=false

# URL внешних сервисов
ARBITR_URL=https://kad.arbitr.ru
COOKIE_SERVICE_URL=http://cookie:8041

# Разрешённые источники для CORS
FRONTEND_ORIGINS=https://my-production-site.com

# Настройки JWT
SECRET_KEY=prod_secret_key
ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=5
REFRESH_TOKEN_EXPIRE_DAYS=30
```

---

### 📂 Frontend - [example](../frontend/.env.example)

**Расположение файлов:**

```
frontend/.env.dev  
frontend/.env.prod
```

**Пример содержимого `frontend/.env.dev` (для локального запуска без Docker использовать - `.env.local`):**

```dotenv
NEXT_PUBLIC_API_URL=http://localhost:8080
```

**Пример содержимого `frontend/.env.prod`:**

```dotenv
NEXT_PUBLIC_API_URL=https://api.my-production-site.com
```

---

### 📂 Database - [example](../.env.db.example)

**Расположение файлов:**

```
.env.db (корневая папка проекта)
```

**Пример содержимого `.env.db`:**

```dotenv
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_DB=mydatabase
```
