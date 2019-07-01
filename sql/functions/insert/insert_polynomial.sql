CREATE OR REPLACE FUNCTION insert_polynomial(d INTEGER, c BIGINT) RETURNS
BIGINT AS
$$
DECLARE ret_value BIGINT;
BEGIN
INSERT INTO
  polynomials (degree, code)
VALUES
  (d, c)
RETURNING
  id
INTO
  ret_value;
RETURN
  ret_value;
END; $$
LANGUAGE PLPGSQL;
