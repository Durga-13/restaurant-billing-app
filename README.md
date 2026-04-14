# Restaurant Billing System

## Overview
A desktop-based restaurant billing application built using Python Tkinter with MySQL integration. It allows users to reserve tables, select menu items, and generate bills.

## Features
- Table reservation system
- Menu display from database
- Add items to bill
- Automatic bill generation
- View reserved tables

## Tech Stack
- Python (Tkinter)
- MySQL

## Database Setup
Create a database:

```sql
CREATE DATABASE restaurant_db;

CREATE TABLE menu_items (
    item_name VARCHAR(100),
    category VARCHAR(50),
    price FLOAT
);

CREATE TABLE reserved_tables (
    table_id INT,
    customer_name VARCHAR(100),
    reservation_time DATETIME
);