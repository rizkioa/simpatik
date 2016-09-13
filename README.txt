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