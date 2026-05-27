# Ozon_test

## Требования

- Python 3.10+
- Git

**Проверка:**
```
python --version
git --version
```
## Быстрый старт

### 1. Клонирование репозитория
```bash
git clone https://github.com/NNikolaiN/Ozon_test
cd Ozon_test
```

### 2. Установка зависимостей
```bash
pip install -r requirements.txt
```
### 3. Запуск тестов
```bash
pytest test_hero.py --alluredir=allure-results
```

### 4. Просмотр Allure-отчета
```bash
allure generate allure-results -o allure-report --clean
allure open allure-report     
```