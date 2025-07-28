-- db_init/init.sql

CREATE DATABASE IF NOT EXISTS inventory;
USE inventory;

CREATE TABLE IF NOT EXISTS items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    quantity INT NOT NULL DEFAULT 0,
    price DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- You can also add some initial data for testing if you want
-- INSERT INTO items (name, description, quantity, price) VALUES
-- ('Laptop', 'Powerful laptop for everyday use', 10, 1200.00),
-- ('Mouse', 'Wireless ergonomic mouse', 50, 25.00),
-- ('Keyboard', 'Mechanical gaming keyboard', 30, 75.00);
