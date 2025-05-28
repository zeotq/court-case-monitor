# Court Case Monitor

Комплекс из нескольких микросервисов для получения и обработки судебных данных с сайта kad.arbitr.ru.
Проект реализует архитектуру на основе REST API с разделением на модули, готов к масштабированию и использованию в продакшене.

## Структура проекта

|                    |                                                                                  |
| -------------------| -------------------------------------------------------------------------------- |
|📁 backend         | основной API-сервис (FastAPI), агрегирует и обрабатывает данные с kad.arbitr     |
|📁 frontend        | frontend-клиент (Next.js), демонстрирует работу с API                            |
|📁 cookie-fetcher  | вспомогательный сервис для получения актуальных cookie с kad.arbitr              |

## Ключевые возможности
- 🔗 Доступ к судебным данным с kad.arbitr.ru через собственный API

- 🍪 Автоматизированное получение cookies для обхода защиты kad.arbitr

- 📡 Модульная архитектура с возможностью масштабирования

- 🌐 REST API, готовый к интеграции с внешними системами

- 📦 Docker-окружение — упрощённый запуск и деплой

- 🧪 Возможность расширения под задачи Data Science / LegalTech / мониторинга судебной активности

## Технологии
| Компонент      | Стек                                             |
| -------------- | ------------------------------------------------ |
| Backend (API)  | Python, FastAPI, Pydantic, httpx                 |
| Frontend       | Next.js, React, Tailwind CSS                     |
| Cookie Service | Python, Requests, Playwright                     |
| Инфраструктура | Docker, Docker Compose                           |

## Инстукция по запуску

### 1. Создать все .env файлы

Инструкция - [env.md](/docs/env.md)

### 2. Запустить проект

#### Запуск через Docker-Compose

| Скрипт                    | Инструкция                                      |
| ------------------------- | ----------------------------------------------- |
| [Bash](build.sh)          | [build_bash.md](docs/build_bash.md)             |
| [PowerShell](./build.ps1) | [build_powershell.md](docs/build_powershell.md) |

#### Инстукция по запуску отдельных сервисов без Docker

- Backend - [README.md](/backend/README.md)

- Frontend - [README.md](/frontend/README.md)

- Cookie-fetcher - [README.md](/cookie-fetcher/README.md)

## 📜 License
Код лицензирован под [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/).  
The code is licensed under [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/).