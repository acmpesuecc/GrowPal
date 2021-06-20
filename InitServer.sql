CREATE USER 'admin_GrowPal'@'localhost' IDENTIFIED BY 'admin@password@GrowPal';
DROP DATABASE IF EXISTS GrowPal;
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

CREATE TABLE credit_card_transactions(
username VARCHAR(50),
item VARCHAR(50),
price VARCHAR(50),
card_number VARCHAR(50),
cvv VARCHAR(50),
flat_number VARCHAR(400));

CREATE TABLE debit_card_transactions(
username VARCHAR(50),
item VARCHAR(50),
price VARCHAR(50),
card_number VARCHAR(50),
cvv VARCHAR(50),
flat_number VARCHAR(400));

CREATE TABLE upi_transactions(
username VARCHAR(50),
item VARCHAR(50),
price VARCHAR(50),
UPI_ID VARCHAR(50),
flat_number VARCHAR(400));

CREATE TABLE net_bank_transactions(
username VARCHAR(50),
item VARCHAR(50),
price VARCHAR(50),
account_number VARCHAR(50),
CIF_num VARCHAR(50),
branch_code VARCHAR(50),
flat_number VARCHAR(400));


CREATE TABLE listed_items(
product_name VARCHAR(50),
product_price VARCHAR(50),
product_description VARCHAR(1000),
seller_name VARCHAR(50),
seller_phone_number VARCHAR(10),
seller_email VARCHAR(50),
selleer_upi_ID VARCHAR(50));


