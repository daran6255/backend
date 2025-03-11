## Permision for pem file
icacls C:\External-projects\WinVinaya\Yunikee-mobileapp\wvis-signit.pem /grant light:(F)

icacls.exe wvis-signit.pem /reset
whoami
icacls.exe wvis-signit.pem /grant:r dharanidaran\daran:(R)
icacls.exe wvis-signit.pem /inheritance:r

## steps for Deployment

### step-1
sudo apt update
sudo apt upgrade -y

### step-2 Install postgres sql
sudo apt install postgresql postgresql-contrib -y
sudo systemctl start postgresql
sudo systemctl enable postgresql
sudo systemctl status postgresql

#### create user in postgres
sudo -i -u postgres
psql
ALTER USER postgres WITH PASSWORD '12345';
\q
exit

#### create new database 
sudo -u postgres createdb islapp


### push from git to server

git clone https://github.com/daran6255/backend.git


### Install dependency
sudo apt install python3-pip
sudo apt install python3.12-venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install python-dotenv
pip install flask_cors
pip install flask_cors
pip install flask_migrate
pip install jwt
pip install geopy
pip install requests
sudo apt install -y libpq-dev python3-dev gcc
pip install psycopg2

### DB migration
flask db init  # Initializes the migrations folder
flask db migrate -m "Initial migration"  # Creates the migration script
flask db upgrade  # Applies the migration and creates the table

### Pm2 config
sudo apt install -y nodejs npm
sudo npm install -g pm2
cd ~/backend
source venv/bin/activate
pm2 start "venv/bin/python3 run.py" --name flask-backend
pm2 save
pm2 startup
pm2 list
pm2 logs flask-backend

pm2 restart flask-backend - ## for restart
pm2 stop flask-backend - ## for stop


nc -zv 15.206.189.85 5000

### Run application
python -m run