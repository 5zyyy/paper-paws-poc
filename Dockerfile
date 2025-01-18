FROM python:3.13

LABEL name="paper-paws-app"
LABEL version="1.0.0"
LABEL description="Paper trading for meme coins. POC by Paperpaws."

WORKDIR /app

COPY . .

RUN pip install -e .

EXPOSE 8501

CMD ["streamlit", "run", "src/app.py"]