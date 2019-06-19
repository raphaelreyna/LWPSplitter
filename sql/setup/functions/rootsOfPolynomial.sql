CREATE OR REPLACE FUNCTION rootsOfPolynomial(poly_id BIGINT) RETURNS TABLE(complex_number_id BIGINT) AS $$
BEGIN
RETURN QUERY SELECT root.complex_number_id FROM roots WHERE polynomial_id = poly_id;
END; $$
LANGUAGE PLPGSQL;
