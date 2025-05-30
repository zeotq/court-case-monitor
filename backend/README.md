# Backend

- [English](#how-to-run)
- [Русский](#как-запустить)

## How to run?

### 1. Create and activate virtual environment  
Create a virtual environment in the `/backend` directory:  
```bash
python -m venv venv
```
#### Activate the virtual environment:

Linux/macOS:
```bash
source venv/bin/activate
```
Windows:
```bash
.\venv\Scripts\activate
```
### 2. Install dependencies
Install all dependencies listed in requirements.txt:
```bash
pip install -r requirements.txt
```
### 3. Start the server
Run the following command to start the FastAPI server:
```bash
uvicorn app:app --host 0.0.0.0 --port 8080 --reload
```
Alternatively, you can run main.py directly:
```
python main.py
```
---
<br>
<br>

## Как запустить?  

### 1. Создайте и активируйте виртуальное окружение  
Создайте виртуальное окружение в директории `/backend`:  
```bash
python -m venv venv
```

Активируйте виртуальное окружение:  
- **Linux/macOS:**  
```bash
source venv/bin/activate
```
- **Windows:**  
```bash
.\venv\Scripts\activate
```

### 2. Установите зависимости  
Установите все зависимости, указанные в [`requirements.txt`](/backend/requirements.txt):  
```bash
pip install -r requirements.txt
```

### 3. Запустите сервер  
Запустите сервер FastAPI с помощью команды:  
```bash
uvicorn app:app --host 0.0.0.0 --port 8080 --reload
```
Или запустите файл [`main.py`](/backend/main.py) напрямую:  
```bash
python main.py
```