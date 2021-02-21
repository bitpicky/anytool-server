
CREATE TABLE test_table (
    id serial PRIMARY KEY,
    answer integer,
    question varchar,
    reviewed_answer varchar);

INSERT INTO test_table VALUES
    (1, 11, 'how high does it go?', null),
    (2, 42, 'what is the meaning of life?', null)
    ;
