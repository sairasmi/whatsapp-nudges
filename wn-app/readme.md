## Project Setup
- Follow the below steps to setup the backend
Python Version Required: 3.10.7
```
cd /var/www/html
git clone git@github.com:piyushh-singhal/whatsapp-nudges.git
cd wn-app/
apt install python3.10-venv
python -m venv venv
source venv/bin/activate
cd src/
sudo apt-get install python3 python3-pip ipython3 build-essential python3-dev
sudo apt install libcairo2-dev pkg-config python3-dev
pip3 install -r requirements.txt
```
- Copy `.env.sample` to `.env` and add the required values.
- Create database and tables in mysql from `whatsapp_nudge.sql` file

## How to run
### Development Environment
```
uvicorn main:app --reload
```

```
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```
(for dev and run it on the ip_address instead of 127.0.0.1)

### Production Environment

#### Using Uvicorn

Run using Uvicorn **without reverse proxy** on Nginx

```
cd /var/www/html/whatsapp-nudges/wn-app/src && /var/www/html/whatsapp-nudges/wn-app/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000 &

# uvicorn main:app --host 0.0.0.0 --port 8000
```

Run using Uvicorn and reverse proxy on Nginx

```
cd /var/www/html/whatsapp-nudges/wn-app/src && /var/www/html/whatsapp-nudges/wn-app/venv/bin/uvicorn main:app --host 127.0.0.1 --port 8000 &
```


#### Using Gunicorn

Run using Gunicorn **without reverse proxy** on Nginx
```
cd /var/www/html/whatsapp-nudges/wn-app/src && /var/www/html/whatsapp-nudges/wn-app/venv/bin/gunicorn -w 4 -k uvicorn.workers.UvicornWorker --log-file /var/www/html/whatsapp-nudges/wn-app/nudges.log main:app --bind 0.0.0.0:8000 &
```

Run using Gunicorn and reverse proxy on Nginx
```
cd /var/www/html/whatsapp-nudges/wn-app/src && /var/www/html/whatsapp-nudges/wn-app/venv/bin/gunicorn -w 4 -k uvicorn.workers.UvicornWorker --log-file /var/www/html/whatsapp-nudges/wn-app/nudges.log main:app &
```

### Load Message history data for a particular date:

- Open http://127.0.0.1:8000/docs
- `[POST]` wn/whatsapp-history-manually    - this is the API, you need to hit - range date support - if want to fetch single date then start_date=end_date
