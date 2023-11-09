USE flask_chatbot;

CREATE TABLE `emotions3` (
  `year` SMALLINT NOT NULL,
  `month` TINYINT NOT NULL,
  `emotion` VARCHAR(45) NOT NULL,
  `count` INT NULL,
  PRIMARY KEY (`year`, `month`, `emotion`));
INSERT INTO emotions3 (`year`, `month`, `emotion`, `count`)
VALUES
    (2023, 1, 'joy', 0),
    (2023, 1, 'anger', 0),
    (2023, 1, 'sad', 0),
    (2023, 1, 'anxiety', 0),
    (2023, 1, 'embarrassment', 0),
    (2023, 2, 'joy', 0),
    (2023, 2, 'anger', 0),
    (2023, 2, 'sad', 0),
    (2023, 2, 'anxiety', 0),
    (2023, 2, 'embarrassment', 0),
    (2023, 3, 'joy', 0),
    (2023, 3, 'anger', 0),
    (2023, 3, 'sad', 0),
    (2023, 3, 'anxiety', 0),
    (2023, 3, 'embarrassment', 0),
    (2023, 4, 'joy', 0),
    (2023, 4, 'anger', 0),
    (2023, 4, 'sad', 0),
    (2023, 4, 'anxiety', 0),
    (2023, 4, 'embarrassment', 0),
    (2023, 5, 'joy', 0),
    (2023, 5, 'anger', 0),
    (2023, 5, 'sad', 0),
    (2023, 5, 'anxiety', 0),
    (2023, 5, 'embarrassment', 0),
    (2023, 6, 'joy', 0),
    (2023, 6, 'anger', 0),
    (2023, 6, 'sad', 0),
    (2023, 6, 'anxiety', 0),
    (2023, 6, 'embarrassment', 0),
    (2023, 7, 'joy', 0),
    (2023, 7, 'anger', 0),
    (2023, 7, 'sad', 0),
    (2023, 7, 'anxiety', 0),
    (2023, 7, 'embarrassment', 0),
    (2023, 8, 'joy', 0),
    (2023, 8, 'anger', 0),
    (2023, 8, 'sad', 0),
    (2023, 8, 'anxiety', 0),
    (2023, 8, 'embarrassment', 0),
    (2023, 9, 'joy', 0),
    (2023, 9, 'anger', 0),
    (2023, 9, 'sad', 0),
    (2023, 9, 'anxiety', 0),
    (2023, 9, 'embarrassment', 0),
    (2023, 10, 'joy', 0),
    (2023, 10, 'anger', 0),
    (2023, 10, 'sad', 0),
    (2023, 10, 'anxiety', 0),
    (2023, 10, 'embarrassment', 0),
    (2023, 11, 'joy', 0),
    (2023, 11, 'anger', 0),
    (2023, 11, 'sad', 0),
    (2023, 11, 'anxiety', 0),
    (2023, 11, 'embarrassment', 0),
    (2023, 12, 'joy', 0),
    (2023, 12, 'anger', 0),
    (2023, 12, 'sad', 0),
    (2023, 12, 'anxiety', 0),
    (2023, 12, 'embarrassment', 0);
    