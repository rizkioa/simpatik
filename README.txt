4. Buat Database simpdu untuk user simpdu dengan password tertentu

-  Masuk mysql console

mysql -u root -p

- Buat user simpdu

CREATE USER 'simpdu'@'localhost' IDENTIFIED BY '!QAZ@WSX';

- Buat database simpdu

create database simpdu;

- Beri akses untuk user simpdu

grant usage on *.* to simpdu@localhost identified by '!QAZ@WSX';

grant all privileges on simpdu.* to simpdu@localhost;

FLUSH PRIVILEGES;

5. Migrasi Database

sudo python manage.py makemigrations
sudo python manage.py migrate

6. Buat superuser

python manage.py createsuperuser