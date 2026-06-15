create table `users` (
  `UUID` VARCHAR(255) not null,
  `Message` TEXT not null,
  primary key (`UUID`)
)
ENGINE=InnoDB;


CREATE TABLE entry(
ID INT PRIMARY KEY AUTO_INCREMENT,
UUID VARCHAR(255) NOT NULL,
Succesful TINYINT NOT NULL,
entry_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
)
ENGINE=InnoDB;