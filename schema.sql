CREATE DATABASE net_banking;
USE net_banking;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    bank_name VARCHAR(255),
    phone VARCHAR(20),
    account_number VARCHAR(50),
    role ENUM('admin', 'customer') NOT NULL
);

CREATE TABLE transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    account_type VARCHAR(50) NOT NULL,
    recipient_phone VARCHAR(20) NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    status ENUM('pending', 'success', 'failed') DEFAULT 'pending',
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE notifications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_read BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Insert a default admin user
INSERT INTO users (name, email, password, bank_name, role)
VALUES ('Admin User', 'admin@bank.com', '$2b$12$7Q5z5z5z5z5z5z5z5z5z5u', 'Central Bank', 'admin');
-- Note: The password hash above is a placeholder. In practice, this should be a bcrypt hash of 'admin123'.