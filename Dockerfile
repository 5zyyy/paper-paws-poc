FROM python:3.13

LABEL name="paper-paws-app"
LABEL version="1.0.0"
LABEL description="Paper trading for meme coins. POC by Paperpaws."

WORKDIR /app

COPY .streamlit .streamlit
COPY requirements.txt .
COPY setup.py .
COPY src src

RUN pip install .

EXPOSE 8501

CMD ["streamlit", "run", "src/app.py"]