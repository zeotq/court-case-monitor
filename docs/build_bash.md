# 📄 Инструкция по запуску скрипта `build.sh`

## Описание

Скрипт `build.sh` предназначен для запуска проекта **Court Case Monitor** в одном из двух режимов:

- **Режим разработки (`dev`)**
- **Продуктовый режим (`prod`)**

Скрипт использует утилиту `docker-compose` для сборки и запуска контейнеров, описанных в соответствующих конфигурационных файлах.

---

## 🛠 Требования

Перед запуском убедитесь, что на вашей системе установлены следующие компоненты:

| Компонент | Версия / Примечание |
|----------|----------------------|
| **Bash** | Оболочка должен быть доступен в терминале |
| **Docker** | Установлен и запущен (Linux) или через Docker Desktop (macOS/WSL) |
| **docker-compose** | Установлен, поддерживается версия 2.x или выше |

> 💡 Рекомендуемая версия: [Docker Engine](https://docs.docker.com/engine/install/) + [Docker Compose Plugin](https://docs.docker.com/compose/install/linux/)

---

## 🧪 Проверка установки

Выполните следующие команды в терминале:

```bash
docker --version
docker compose version || docker-compose --version
```

Если вывод содержит информацию о версии — Docker установлен корректно.

---

## 🔧 Подготовка к запуску

1. Перейдите в директорию проекта:
   ```bash
   cd /путь/к/проекту
   ```

2. Убедитесь, что файл `build.sh` имеет права на исполнение:
   ```bash
   chmod +x build.sh
   ```

3. Убедитесь, что в папке проекта находятся необходимые файлы:
   - `docker-compose.yml`
   - `docker-compose.override.yml` *(рекомендуется для разработки)*
   - `docker-compose.prod.yml` *(только для production)*

---

## ▶️ Запуск скрипта

### Режим разработки
```bash
./build.sh dev
```
Этот режим:
- Использует стандартный `docker-compose.yml` и при наличии `docker-compose.override.yml`
- Строит образы и запускает контейнеры в интерактивном режиме

### Продуктовый режим
```bash
./build.sh prod
```
Этот режим:
- Использует комбинацию `docker-compose.yml` и `docker-compose.prod.yml`
- Запускает контейнеры в фоновом режиме (`-d`)

---

## ❗ Возможные проблемы и их решение

### 1. **Ошибка: "Permission denied" при запуске скрипта**

#### Причина:
Файл не имеет прав на исполнение.

#### Решение:
Установите исполняемые права:
```bash
chmod +x build.sh
```

---

### 2. **Ошибка: "command not found: docker-compose" или "docker compose: command not found"**

#### Причина:
`docker-compose` не установлен или используется старая версия.

#### Решение:
Установите актуальную версию Docker Compose:

**Для Linux:**
```bash
sudo apt update && sudo apt install docker-compose-plugin
```

**Или вручную:**
```bash
DOCKER_CONFIG=${DOCKER_CONFIG:-~/.docker}
mkdir -p $DOCKER_CONFIG/cli-plugins
curl -SL https://github.com/docker/compose/releases/download/v2.23.0/docker-compose-linux-x86_64 -o ~/.docker/cli-plugins/docker-compose
chmod +x ~/.docker/cli-plugins/docker-compose
```

Проверьте:
```bash
docker compose version
```

---

### 3. **Ошибка: "File not found" или "can't find docker-compose.yml"**

#### Причина:
Не хватает необходимых файлов конфигурации.

#### Решение:
Убедитесь, что в текущей директории присутствуют файлы:
- `docker-compose.yml`
- `docker-compose.prod.yml` *(для production режима)*

---

### 4. **Ошибка: "permission denied" при работе с Docker**

#### Причина:
Текущий пользователь не добавлен в группу `docker`.

#### Решение:
Добавьте пользователя в группу `docker`:
```bash
sudo usermod -aG docker $USER
```
Затем выйдите из системы и войдите снова.
