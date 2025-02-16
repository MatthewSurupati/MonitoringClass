create table monitoring
(
    date             date         not null,
    class_code       varchar(255) null,
    id_monitoring    varchar(255) not null
        primary key,
    count_engage     int          null,
    count_not_engage int          null,
    analysis         varchar(15)  null,
    constraint monitoring___fk
        foreign key (class_code) references class (class_code)
);


