CREATE OR REPLACE FUNCTION is_polynomial_completed(poly_id BIGINT) RETURNS BOOLEAN AS $$
BEGIN
RETURN get_degree_of_polynomial(poly_id) = number_of_roots_logged_for_polynomial(poly_id);
END; $$
LANGUAGE PLPGSQL;
