CREATE OR REPLACE FUNCTION insert_complex_number(re_part DOUBLE PRECISION, im_part DOUBLE PRECISION) RETURNS BIGINT AS
$$
BEGIN
INSERT INTO
  complex_numbers (real_part, imaginary_part)
VALUES
  (re_part, im_part)
RETURNING
  id;
END; $$
LANGUAGE PLPGSQL;