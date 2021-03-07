
CREATE TABLE test_table (
    id serial PRIMARY KEY,
    answer integer,
    question varchar,
    reviewed_answer varchar);

INSERT INTO test_table VALUES
    (1, 11, 'how high does it go?', null),
    (2, 42, 'what is the meaning of life?', null)
    ;


CREATE TABLE nlp_classification_output (
    id serial PRIMARY KEY,
    item_description varchar,
    predicted_item_label varchar,
    reviewed_answer varchar);

INSERT INTO nlp_classification_output VALUES
    (1, 'pizza', 'food', null),
    (2, 'prosciutto di parma', 'food', null),
    (3, 'prosecco', 'alcohol', null),
    (4, 'Lamborghini', 'unknown', null),
    (5, 'Ferrari', 'unknown', null)
    ;

CREATE TABLE nlp_classification_output_update (
    id serial PRIMARY KEY,
    item_description varchar,
    predicted_item_label varchar,
    reviewed_answer varchar);

INSERT INTO nlp_classification_output_update VALUES
    (1, 'pizza', 'food', null),
    (2, 'prosciutto di parma', 'food', null),
    (3, 'prosecco', 'alcohol', null),
    (4, 'Lamborghini', 'unknown', null),
    (5, 'Ferrari', 'unknown', null)
    ;
