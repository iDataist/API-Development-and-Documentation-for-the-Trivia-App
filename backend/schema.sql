DROP TABLE IF EXISTS categories CASCADE;
CREATE TABLE categories (
    id serial primary key,
    type text
);

DROP TABLE IF EXISTS questions CASCADE;
CREATE TABLE questions (
    id serial primary key,
    question text,
    answer text,
    difficulty integer,
    category integer
);