CREATE OR REPLACE FUNCTION get_degree_of_polynomial(poly_id BIGINT) RETURNS INTEGER AS $$
BEGIN
RETURN (SELECT degree FROM polynomials WHERE id = poly_id);
END; $$
LANGUAGE PLPGSQL;
