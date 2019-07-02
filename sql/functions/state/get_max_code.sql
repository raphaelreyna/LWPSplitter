CREATE OR REPLACE FUNCTION get_max_code() RETURNS BIGINT AS $$
BEGIN
RETURN (SELECT max(code) FROM polynomials WHERE degree=(SELECT get_max_degree()));
END; $$
LANGUAGE PLPGSQL;
