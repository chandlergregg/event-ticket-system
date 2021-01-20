# event-ticket-system

This repo contains code and data to demonstrate using Python to programatically load and query data into a MySQL database. This project is part of the Springboard Data Engineering career track curriculum.

### Files

The project consists of 3 files:
- `ticketing_system.py`: This file contains all the code needed to load the CSV data into a local MySQL database and query the data for the most popular event tickets sold
- `third_party_sales.csv`: This file is a header-less CSV file with the data needed to load into MySQL
- `ticketing_system_queries.sql`: This file contains the queries used in the Python file and and can be executed manually to test

### How to reproduce

In order to reproduce the project locally:
- Clone / download all files in the repo
- Set up or use an existing MySQL database
- Edit `ticketing_system.py` with the proper MySQL database settings
    - [User and password](https://github.com/chandlergregg/event-ticket-system/blob/main/ticketing_system.py#L181-L182) are required at the bare minimum, if using a MySQL database on localhost
    - The CSV filename and other details are already set
