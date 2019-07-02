CREATE OR REPLACE FUNCTION insert_root(poly_id BIGINT, cn_id BIGINT, mult INTEGER) RETURNS
BIGINT AS
$$
DECLARE
  ret_val BIGINT;
BEGIN
INSERT INTO
  roots (polynomial_id, complex_number_id, multiplicity)
VALUES
  (poly_id, cn_id, mult)
RETURNING
  id
INTO
  ret_val;
RETURN
  ret_val;
END; $$
LANGUAGE PLPGSQL;
