create table users
(
    id            int auto_increment
        primary key,
    username      varchar(255) not null,
    password_hash varchar(255) not null,
    constraint username
        unique (username)
);


