CREATE OR REPLACE FUNCTION globalMultiplicityOf(cn_id BIGINT) RETURNS INTEGER AS $$
BEGIN
RETURN (SELECT SUM(multiplicity) FROM roots WHERE complex_number_id = cn_id);
End; $$
LANGUAGE PLPGSQL;
