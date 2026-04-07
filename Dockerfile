FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN mkdir -p photos
EXPOSE 8080
# Запускаем и бота, и веб-сервер внутри одного контейнера
CMD sh -c "python web.py & python bot.py"