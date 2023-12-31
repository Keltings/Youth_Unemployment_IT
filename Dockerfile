# app/Dockerfile

FROM python:3.11.3 

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# RUN git clone https://github.com/Keltings/Youth_Unemployment_IT.git .
COPY ./ /app

RUN pip install streamlit

RUN pip install -r requirements.txt

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "streamlit_app.py", "--server.port=80", "--server.address=0.0.0.0"]

# CMD source /app/.venv/bin/activate && exec streamlit run ...