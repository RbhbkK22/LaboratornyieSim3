CREATE TABLE IF NOT EXISTS STUDENTS (
                          id int NOT NULL AUTO_INCREMENT,
                          name varchar(15),
                          surname varchar(25),
                          faculty varchar(20),
                          age int,
                          PRIMARY KEY (id));

CREATE TABLE IF NOT EXISTS DISCIPLINES (
                          id int NOT NULL AUTO_INCREMENT,
                          name varchar(50),
                          teacher varchar(50),
                          hours int,
                          semester int,
                          PRIMARY KEY (id));
