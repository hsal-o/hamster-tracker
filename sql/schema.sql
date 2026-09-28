CREATE TABLE hamster (
   id INT AUTO_INCREMENT PRIMARY KEY,
   name VARCHAR(100) NOT NULL,
   acquired_date DATE DEFAULT NULL,
   active BOOLEAN NOT NULL DEFAULT TRUE,
   created_at TIMESTAMP DEFAULT current_timestamp()
);

CREATE TABLE wheel (
   id INT AUTO_INCREMENT PRIMARY KEY,
   name VARCHAR(100) NOT NULL,
   circumference_inches DECIMAL(10,4) NOT NULL,
   active BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE run_session (
   id BIGINT AUTO_INCREMENT PRIMARY KEY,
   hamster_id INT NOT NULL,
   wheel_id INT NOT NULL,
   started_at DATETIME NOT NULL,
   ended_at DATETIME NOT NULL,
   revolutions INT NOT NULL,
   distance_miles DECIMAL(10,4) NOT NULL,
   elapsed_seconds DECIMAL(10,3) NOT NULL,
   created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
   FOREIGN KEY (hamster_id) REFERENCES hamster(id),
   FOREIGN KEY (wheel_id) REFERENCES wheel(id)
);