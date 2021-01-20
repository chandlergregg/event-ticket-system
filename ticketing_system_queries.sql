drop database if exists ticketing_system;
create database ticketing_system;

use ticketing_system;
drop table if exists ticket_sales;
create table ticket_sales (
	ticket_id int
	, trans_date date
	, event_id int
	, event_name varchar(50)
	, event_date date
	, event_type varchar(10)
	, event_city varchar(20)
	, event_addr varchar(100)
	, customer_id int
	, price decimal
	, num_tickets int
	, primary key (ticket_id)
);

select * from ticket_sales;

select 
	  event_name
from ticket_sales
group by event_name
order by sum(num_tickets)
limit 3;
