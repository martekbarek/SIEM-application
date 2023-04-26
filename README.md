![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)

# Speedy7 
is a simple SIEM web application which aggregates **syslog** data from client machines. It allows filtering logs and displaying them in a variety of ways. All the components are deployed in containers.

**Main dashboard consist of 6 cards:**
![Capture-2023-04-16-114059](https://user-images.githubusercontent.com/73181855/232290457-47fb8b30-c854-458a-8ac7-0ed03d71535a.png)

![Capture-2023-04-16-114128](https://user-images.githubusercontent.com/73181855/232290499-98ff37c1-1ccc-4398-83a2-15fa0a7d0d3f.png)

![Capture-2023-04-16-114208](https://user-images.githubusercontent.com/73181855/232290567-fc83d6a5-3c0d-48ba-a27e-8e65b655908f.png)

**Other features:**
- it can verify if host is online,
<img width="1440" alt="image" src="https://user-images.githubusercontent.com/73181855/232289526-97ddf357-e3c0-450b-ad93-9453ea5d7b71.png">

- has ability to grant different scope of access
<img width="1440" alt="image" src="https://user-images.githubusercontent.com/73181855/232289687-3ed240a5-3604-428f-a181-c0d5705d4af7.png">


# Manual

## Running whole project in container environment:

## Deploy using Docker
**1. Configure .env.example and App/.env.example files**

**2. Run command**
```bash 
docker compose --env-file .env.example up --build --remove-orphans
 ```


## Running Django app locally:

**1. Create and activate virtulal environment** 

```bash
python -m venv venv
echo venv/ >> .gitignore
source venv/bin/activate
pip install -r requirements.txt
source venv/bin/activate
```
**2. Comment 13,14,15 lines in speedy7/core/models.py**

**3. Run** 
```bash
py App\speedy7\manage.py runserver
```

# Troubleshooting

```bash
# shows open connections
lsof -i
# track service
strace <service>
# test message
logger -p local0.info --server 127.0.0.1 --tcp --port 514 "Test message"
# grep syslog process
ps -aux | grep -i syslog
```


