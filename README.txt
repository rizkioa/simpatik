4. Buat Database simpatik untuk user simpatik dengan password tertentu

-  Masuk mysql console

mysql -u root -p

- Buat user simpatik

CREATE USER 'simpatik'@'localhost' IDENTIFIED BY '!QAZ@WSX';

- Buat database simpatik

create database simpatik;

- Beri akses untuk user simpatik

grant usage on *.* to simpatik@localhost identified by '!QAZ@WSX';

grant all privileges on simpatik.* to simpatik@localhost;

FLUSH PRIVILEGES;

5. Migrasi Database

sudo python manage.py makemigrations
sudo python manage.py migrate

6. Buat superuser
python manage.py createsuperuser


############################# postgres database ##############################
1. create database

CREATE DATABASE simpatik;

2. create user

CREATE USER simpatik WITH PASSWORD '!QAZ@WSX';

3. beri akses

ALTER ROLE simpatik SET client_encoding TO 'utf8';
ALTER ROLE simpatik SET default_transaction_isolation TO 'read committed';
ALTER ROLE simpatik SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE simpatik TO simpatik;
############################# postgres database ##############################

############################# import export database #########################
#### import ####
sudo psql -U simpatik -h localhost simpatik < simpatik.psql
#### export ####
sudo pg_dump -U simpatik -h localhost simpatik > simpatik.psql
############################# import export database #########################
