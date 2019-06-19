CREATE OR REPLACE FUNCTION numberOfRootsLogged(poly_id BIGINT) RETURNS INTEGER AS $$
BEGIN
RETURN (SELECT SUM(multiplicity) FROM roots WHERE polynomial_id = poly_id);
END; $$
LANGUAGE PLPGSQL;
