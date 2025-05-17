CREATE DATABASE IF DOES NOT EXISTS ALX_prodev;

USE ALX_prodev;

CREATE TABLE
    IF NOT EXISTS user_data (
        user_id CHAR(36) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        age DECIMAL(3, 0) NOT NULL,
        INDEX (user_id)
    );

INSERT INTO
    user_data (user_id, name, email, age)
VALUES
    (
        UUID (),
        "Johnnie Mayer",
        "Ross.Reynolds21@hotmail.com",
        35.0
    ),
    (
        UUID (),
        "Myrtle Waters",
        "Edmund_Funk@gmail.com",
        99.0
    ),
    (
        UUID (),
        "Flora Rodriguez I",
        "Willie.Bogisich@gmail.com",
        84.0
    ),
    (
        UUID (),
        "Dr. Cecilia Konopelski-Lakin",
        "Felicia75@gmail.com",
        87.0
    ),
    (
        UUID (),
        "Chelsea Boyle-Stoltenberg",
        "Regina.Emard97@yahoo.com",
        83.0
    );