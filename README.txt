create database sbidb;
use sbidb;

create table accmaster(
accno integer primary key auto_increment,
name varchar(30),
balance integer
)auto_increment=1000;

create table trans(
tid integer primary key auto_increment,
tdate timestamp default now(),
accno integer,
amt integer,
ttype enum('D','W')
);
