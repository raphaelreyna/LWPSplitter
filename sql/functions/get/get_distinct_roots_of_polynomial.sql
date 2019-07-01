CREATE OR REPLACE FUNCTION
get_distinct_roots_of_polynomial(d INTEGER, c BIGINT)
RETURNS TABLE (real_part DOUBLE PRECISION, imaginary_part DOUBLE PRECISION, multiplicity SMALLINT)
AS
$$
BEGIN 
RETURN QUERY (
SELECT DISTINCT
polynomial_roots.real_part,
polynomial_roots.imaginary_part,
polynomial_roots.multiplicity
FROM
polynomial_roots
WHERE
degree = d AND code = c
);
END; $$
LANGUAGE PLPGSQL;
