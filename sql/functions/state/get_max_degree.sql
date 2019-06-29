CREATE OR REPLACE FUNCTION get_max_degree() RETURNS BIGINT AS $$
BEGIN
RETURN (SELECT max(degree) FROM polynomials);
END; $$
LANGUAGE PLPGSQL;