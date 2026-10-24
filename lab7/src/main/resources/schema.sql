CREATE TABLE IF NOT EXISTS STUDENTS (
                          id int NOT NULL AUTO_INCREMENT,
                          name varchar(15),
                          surname varchar(25),
                          faculty varchar(20),
                          age int,
                          PRIMARY KEY (id));

CREATE TABLE IF NOT EXISTS STUDY_GROUPS (
                          id int NOT NULL AUTO_INCREMENT,
                          name varchar(20),
                          faculty varchar(20),
                          course int,
                          curator varchar(50),
                          PRIMARY KEY (id));
