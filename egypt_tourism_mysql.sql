-- Create database
CREATE DATABASE IF NOT EXISTS egypt_tourism;
USE egypt_tourism;

-- Create tables
CREATE TABLE user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(64) NOT NULL UNIQUE,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(256) NOT NULL,
    is_guide BOOLEAN,
    is_student BOOLEAN,
    is_tourist BOOLEAN,
    is_admin BOOLEAN,
    phone VARCHAR(20),
    country VARCHAR(100),
    governorate VARCHAR(100),
    city VARCHAR(100),
    profile_pic VARCHAR(200),
    education_level VARCHAR(100),
    university VARCHAR(200),
    languages VARCHAR(200),
    bio TEXT,
    date_joined TIMESTAMP,
    profile_completed BOOLEAN
);

CREATE TABLE region (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    name_ar VARCHAR(100),
    description TEXT,
    description_ar TEXT
);

CREATE TABLE attraction (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    name_ar VARCHAR(100),
    description TEXT NOT NULL,
    description_ar TEXT,
    image_url VARCHAR(200),
    address VARCHAR(200),
    latitude DOUBLE,
    longitude DOUBLE,
    ticket_price VARCHAR(100),
    opening_hours VARCHAR(100),
    website VARCHAR(200),
    featured BOOLEAN,
    region_id INT NOT NULL,
    FOREIGN KEY (region_id) REFERENCES region(id)
);

CREATE TABLE activity (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    name_ar VARCHAR(100),
    description TEXT,
    description_ar TEXT,
    image_url VARCHAR(200),
    price VARCHAR(100),
    duration VARCHAR(50),
    attraction_id INT NOT NULL,
    FOREIGN KEY (attraction_id) REFERENCES attraction(id)
);

CREATE TABLE restaurant (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    name_ar VARCHAR(100),
    description TEXT,
    description_ar TEXT,
    image_url VARCHAR(200),
    cuisine_type VARCHAR(100),
    price_range VARCHAR(50),
    contact VARCHAR(100),
    latitude DOUBLE,
    longitude DOUBLE,
    attraction_id INT NOT NULL,
    FOREIGN KEY (attraction_id) REFERENCES attraction(id)
);

CREATE TABLE review (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    content TEXT NOT NULL,
    rating INT NOT NULL,
    date_posted TIMESTAMP,
    user_id INT NOT NULL,
    attraction_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(id),
    FOREIGN KEY (attraction_id) REFERENCES attraction(id)
);

CREATE TABLE guide (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    years_experience INT,
    specialization VARCHAR(200),
    certification VARCHAR(200),
    available BOOLEAN,
    FOREIGN KEY (user_id) REFERENCES user(id)
);

CREATE TABLE tour_plan (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    title_ar VARCHAR(200),
    description TEXT NOT NULL,
    description_ar TEXT,
    duration INT NOT NULL,
    price DOUBLE NOT NULL,
    created_at TIMESTAMP,
    image_url VARCHAR(200)
);

CREATE TABLE tour_plan_destination (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tour_plan_id INT NOT NULL,
    attraction_id INT NOT NULL,
    day_number INT NOT NULL,
    description TEXT,
    description_ar TEXT,
    FOREIGN KEY (tour_plan_id) REFERENCES tour_plan(id),
    FOREIGN KEY (attraction_id) REFERENCES attraction(id),
    UNIQUE KEY unique_plan_attraction_day (tour_plan_id, attraction_id, day_number)
);

CREATE TABLE tour_booking (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tourist_id INT NOT NULL,
    tour_plan_id INT NOT NULL,
    guide_id INT,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    status VARCHAR(20),
    booking_date TIMESTAMP,
    FOREIGN KEY (tourist_id) REFERENCES user(id),
    FOREIGN KEY (tour_plan_id) REFERENCES tour_plan(id),
    FOREIGN KEY (guide_id) REFERENCES user(id)
);

CREATE TABLE tour_progress (
    id INT AUTO_INCREMENT PRIMARY KEY,
    booking_id INT NOT NULL,
    destination_id INT NOT NULL,
    completed BOOLEAN,
    completion_date TIMESTAMP,
    notes TEXT,
    FOREIGN KEY (booking_id) REFERENCES tour_booking(id),
    FOREIGN KEY (destination_id) REFERENCES tour_plan_destination(id),
    UNIQUE KEY unique_booking_destination (booking_id, destination_id)
);

CREATE TABLE tour_photo (
    id INT AUTO_INCREMENT PRIMARY KEY,
    progress_id INT NOT NULL,
    image_url VARCHAR(200) NOT NULL,
    caption VARCHAR(200),
    uploaded_at TIMESTAMP,
    FOREIGN KEY (progress_id) REFERENCES tour_progress(id)
);

CREATE TABLE chat_group (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP,
    guide_id INT NOT NULL,
    language VARCHAR(50) NOT NULL,
    FOREIGN KEY (guide_id) REFERENCES user(id)
);

CREATE TABLE chat_group_member (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    chat_group_id INT NOT NULL,
    joined_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(id),
    FOREIGN KEY (chat_group_id) REFERENCES chat_group(id),
    UNIQUE KEY unique_user_group (user_id, chat_group_id)
);

CREATE TABLE chat_message (
    id INT AUTO_INCREMENT PRIMARY KEY,
    content TEXT NOT NULL,
    timestamp TIMESTAMP,
    user_id INT NOT NULL,
    chat_group_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(id),
    FOREIGN KEY (chat_group_id) REFERENCES chat_group(id)
);

CREATE TABLE language_practice (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    guide_id INT,
    language VARCHAR(50) NOT NULL,
    proficiency_level VARCHAR(50) NOT NULL,
    availability VARCHAR(200),
    interests VARCHAR(200),
    FOREIGN KEY (student_id) REFERENCES user(id),
    FOREIGN KEY (guide_id) REFERENCES user(id)
);

-- Add indexes
CREATE INDEX idx_user_email ON user(email);
CREATE INDEX idx_attraction_region ON attraction(region_id);
CREATE INDEX idx_tour_booking_date ON tour_booking(start_date);
CREATE INDEX idx_chat_message_timestamp ON chat_message(timestamp);
CREATE INDEX idx_tour_progress_completed ON tour_progress(completed);

-- Set character set
ALTER DATABASE egypt_tourism CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE user CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE region CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE attraction CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE activity CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE restaurant CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE review CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE guide CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE tour_plan CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE tour_plan_destination CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE tour_booking CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE tour_progress CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE tour_photo CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE chat_group CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE chat_group_member CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE chat_message CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE language_practice CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
