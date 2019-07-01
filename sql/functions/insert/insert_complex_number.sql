CREATE OR REPLACE FUNCTION insert_complex_number(re_part DOUBLE PRECISION, im_part DOUBLE PRECISION) RETURNS BIGINT AS
$$
DECLARE ret_val BIGINT;
BEGIN
INSERT INTO
  complex_numbers (real_part, imaginary_part)
VALUES
  (re_part, im_part)
RETURNING
  id
INTO
  ret_val;
RETURN
  ret_val;
END; $$
LANGUAGE PLPGSQL;
