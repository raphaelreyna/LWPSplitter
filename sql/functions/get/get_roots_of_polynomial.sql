CREATE OR REPLACE FUNCTION get_roots_of_polynomial_distinct(d INTEGER, c BIGINT) RETURNS BIGINT AS
$$
BEGIN
RETURN (
       SELECT
        real_part,
        imaginary_part,
        multiplicity
       FROM
        polynomial_roots
       WHERE
        degree = d AND code = c
       );
END; $$
LANGUAGE PLPGSQL;
