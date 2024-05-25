FROM python:3.10-slim

ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PIP_NO_CACHE_DIR=off

ENV GOOGLE_OAUTH2_KEY=your_client_id
ENV GOOGLE_OAUTH2_SECRET=your_client_secret
ENV LINKEDIN_OAUTH2_KEY=your_client_id
ENV LINKEDIN_OAUTH2_SECRET=your_client_secret
ENV FACEBOOK_OAUTH2_KEY=your-client-id
ENV FACEBOOK_OAUTH2_SECRET=your-client-secret

WORKDIR /source

COPY . /source/

RUN apt-get update -y && apt-get upgrade -y

RUN pip install -U pip && pip install -r requirements.txt

RUN python manage.py makemigrations && python manage.py migrate

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]