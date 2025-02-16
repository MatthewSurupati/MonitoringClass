create table detail_monitoring
(
    id_monitoring  varchar(255) not null,
    activity       varchar(255) null,
    activity_count int          null,
    constraint detail_monitoring___fk
        foreign key (id_monitoring) references monitoring (id_monitoring)
);


