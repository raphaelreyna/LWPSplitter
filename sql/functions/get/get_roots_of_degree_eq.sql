CREATE OR REPLACE FUNCTION
get_roots_of_degree_eq(d INTEGER)
RETURNS TABLE (real_part DOUBLE PRECISION, imaginary_part DOUBLE PRECISION)
AS
$$
BEGIN
RETURN QUERY (
SELECT
polynomial_roots.real_part,
polynomial_roots.imaginary_part
FROM
polynomial_roots
WHERE
degree = d
);
END; $$
LANGUAGE PLPGSQL;
