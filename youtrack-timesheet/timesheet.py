from datetime import date, timedelta
import requests
import json
import os
from dotenv import load_dotenv

# Загружаем переменные окружения из файла .env
load_dotenv()

# Укажите URL вашего YouTrack и токен доступа из переменных окружения
base_url = os.getenv('YOUTRACK_URL')
token = os.getenv('YOUTRACK_TOKEN')

# Путь к файлу конфигурации
config_file_path = 'tasks.json'

# Проверяем, существует ли файл конфигурации
if not os.path.exists(config_file_path):
    print(f"Файл конфигурации {config_file_path} не найден")
    exit(1)

# Читаем конфигурацию из файла
with open(config_file_path, 'r') as config_file:
    tasks = json.load(config_file)

# Создаем объект date для текущей даты
today = date.today()

# Определяем текущую неделю
start_of_week = today - timedelta(days=today.weekday())

# Заголовки запроса
headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
}

# Отправка запросов для каждой задачи
for task in tasks:
    issue_id = task['id']
    time_spent_hours = task['time_spent_hours']
    time_spent_minutes = int(time_spent_hours * 60)  # Преобразуем часы в минуты
    work_type_id = task['work_type']
    comment = task['comment']
    day_of_week = task['day_of_week']

    # Определяем дату для указанного дня недели на текущей неделе
    days_until_day_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'].index(day_of_week)
    task_date = start_of_week + timedelta(days=days_until_day_of_week)

    # Данные для запроса
    data = {
        "issueId": issue_id,
        "duration": {
                "minutes": time_spent_minutes
            },
        "date": int(task_date.strftime("%s")) * 1000,  # Дата в миллисекундах
        "text": comment,
        "type": {
                "id": work_type_id
            }
    }

    # URL для добавления времени
    url = f'{base_url}/issues/{issue_id}/timeTracking/workItems'

    # Отправка запроса
    response = requests.post(url, headers=headers, data=json.dumps(data))

    # Проверка ответа
    if response.status_code == 200:
        print(f"Время успешно списано для задачи {issue_id} на дату {task_date} с комментарием '{comment}'")
    else:
        print(f"Ошибка для задачи {issue_id}: {response.status_code}")
        print(response.text)