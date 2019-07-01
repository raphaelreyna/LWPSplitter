CREATE OR REPLACE FUNCTION
get_distinct_roots_of_degree_geq(d INTEGER)
RETURNS TABLE (real_part DOUBLE PRECISION, imaginary_part DOUBLE PRECISION)
AS
$$
BEGIN
RETURN QUERY (
SELECT DISTINCT
polynomial_roots.real_part,
polynomial_roots.imaginary_part
FROM
polynomial_roots
WHERE
degree >= d
);
END; $$
LANGUAGE PLPGSQL;
