DROP TABLE if exists urls CASCADE;
DROP TABLE if exists url_checks CASCADE;


CREATE TABLE urls (
    id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name varchar UNIQUE NOT NULL,
    created_at date
);


CREATE TABLE url_checks (
    id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    url_id bigint REFERENCES urls(id) ON DELETE CASCADE,
    status_code bigint,
    h1 varchar,
    title varchar,
    description varchar,
    created_at date
);
