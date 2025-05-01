#!/usr/bin/env bash
set -euo pipefail

# Если где-то остался «мёртвый» lock Xvfb — удаляем
if [ -f /tmp/.X99-lock ]; then
  rm -f /tmp/.X99-lock
fi

# Запускаем Xvfb на дисплее :99
Xvfb :99 -screen 0 1280x720x24 &
XVFB_PID=$!

# Убираем lock-файл для безопасности (ещё раз)
rm -f /tmp/.X99-lock

# Экспортируем DISPLAY
export DISPLAY=:99

# Даем Xvfb 1 секунду на старт
sleep 1

# Когда контейнер падает — убиваем Xvfb
trap "kill $XVFB_PID" EXIT

# Запускаем FastAPI-сервис
exec uvicorn cookie_service:app --host 0.0.0.0 --port 8041
