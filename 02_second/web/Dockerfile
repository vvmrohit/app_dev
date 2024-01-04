FROM python:3
  # checkov:skip=CKV_DOCKER_3: ADD REASON
  # checkov:skip=CKV_DOCKER_2: ADD REASON

WORKDIR /usr/src/app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "app.py"]