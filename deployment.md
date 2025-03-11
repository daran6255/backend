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