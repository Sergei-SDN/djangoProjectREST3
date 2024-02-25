# Используем базовый образ Python 3 из официального репозитория Docker Hub
FROM python:3

# Устанавливаем рабочую директорию контейнера в /code
WORKDIR /code

# Копируем файл requirements.txt из локальной директории проекта в /code/ внутри контейнера
COPY ./requirements.txt /code/

# Устанавливаем зависимости Python, указанные в requirements.txt, внутри контейнера
RUN pip install -r /code/requirements.txt

# Копируем все файлы из локальной директории проекта внутрь контейнера в /code/
COPY . .


