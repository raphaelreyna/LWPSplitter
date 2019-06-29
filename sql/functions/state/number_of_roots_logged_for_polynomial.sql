CREATE OR REPLACE FUNCTION number_of_roots_logged_for_polynomial(poly_id BIGINT) RETURNS INTEGER AS $$
BEGIN
RETURN (SELECT SUM(multiplicity) FROM roots WHERE polynomial_id = poly_id);
END; $$
LANGUAGE PLPGSQL;
