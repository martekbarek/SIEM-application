![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)


## Deployment

1. Configure .env.example and App/.env.example files
2. Simply run
```bash 
docker compose --env-file .env.example up --build --remove-orphans
 ```



## Running django app locally:

1. Activate your previously created virtual environment 
```bash
source venv/bin/activate
```
2. Comment 13,14,15 lines in speedy7/core/models.py

3. run 
```bash
py App\speedy7\manage.py runserver
```

## Helpful commands:

```bash
# shows open connections
lsof -i
# track service
strace <service>
# test message
logger -p local0.info --server 127.0.0.1 --tcp --port 514 "Test message"
# list proccesses
ps -aux | grep -i syslog
# attach to db
psql -h localhost -p 5432 -U syslog
# conntect to db
\c syslog
# show tables
\dt
# show record
select * from messages_ubuntu_client
# Create virtual environment
python -m venv venv
echo venv/ >> .gitignore
source venv/bin/activate
pip install -r requirements.txt
```


