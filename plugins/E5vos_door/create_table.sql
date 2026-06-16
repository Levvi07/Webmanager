create table `users` (
  `UUID` VARCHAR(255) not null,
  `Name` TEXT not null,
  `Email` TEXT not null,
  `E5kod` TEXT not null,
  `Comment` TEXT not null,
  `created_at` timestamp not null default CURRENT_TIMESTAMP(),
  `last_used_at` timestamp not null default CURRENT_TIMESTAMP(),
  primary key (`UUID`)
)
ENGINE=InnoDB
;

CREATE TABLE `entry`(
  `ID` INT AUTO_INCREMENT,
  `UUID` VARCHAR(255) NOT NULL,
  `Succesful` TINYINT(1) NOT NULL,
  `entry_time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
  primary key (`ID`)
)
ENGINE=InnoDB
;
