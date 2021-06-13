CREATE USER 'admin_GrowPal'@'localhost' IDENTIFIED BY 'admin@password@GrowPal';
CREATE DATABASE GrowPal;
GRANT ALL PRIVILEGES ON GrowPal.* TO 'admin_GrowPal'@'localhost';
FLUSH PRIVILEGES;


USE GrowPal;
CREATE TABLE login_details(
username VARCHAR(50),
password VARCHAR(100),
email VARCHAR(100),
phone_number VARCHAR(10),
PRIMARY KEY(username));
