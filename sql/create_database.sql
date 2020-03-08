-- Database: final_project

-- DROP DATABASE final_project;

CREATE DATABASE final_project
    WITH 
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'English_United States.1252'
    LC_CTYPE = 'English_United States.1252'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;
	
-- Create Tables
create table example(
	example_id serial PRIMARY KEY,
	description VARCHAR(100)
);

-- Populate Tables
INSERT INTO example (description) 
VALUES ('foo');

INSERT INTO example (description) 
VALUES ('bar');

-- Test Query
SELECT * FROM example;
