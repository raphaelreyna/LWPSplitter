CREATE OR REPLACE FUNCTION polynomialIsComplete(poly_id BIGINT) RETURNS BOOLEAN AS $$
BEGIN
RETURN degreeOfPolynomial(poly_id) = numberOfRootsLogged(poly_id);
END; $$
LANGUAGE PLPGSQL;
