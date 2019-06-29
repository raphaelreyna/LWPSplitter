CREATE OR REPLACE FUNCTION get_distinct_roots_of_degree_eq(d INTEGER) RETURNS SETOF complex_numbers AS
$$
BEGIN
RETURN QUERY (
SELECT
real_part,
imaginary_part
FROM
polynomial_roots
WHERE
polynomial.degree = d
);
END; $$
LANGUAGE PLPGSQL;
