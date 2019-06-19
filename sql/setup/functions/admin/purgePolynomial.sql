CREATE OR REPLACE FUNCTION purgePolynomial(poly_id BIGINT) RETURNS VOID AS $$
BEGIN
DELETE FROM roots WHERE polynomial_id = poly_id;
DELETE FROM polynomials WHERE id = poly_id;
END; $$
LANGUAGE PLPGSQL;
