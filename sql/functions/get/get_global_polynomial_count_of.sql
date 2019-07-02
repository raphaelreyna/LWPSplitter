CREATE OR REPLACE FUNCTION get_global_polynomial_count_of(cn_id BIGINT) RETURNS INTEGER AS $$
BEGIN
RETURN (SELECT COUNT(multiplicity) FROM roots WHERE complex_number_id = cn_id);
End; $$
LANGUAGE PLPGSQL;
