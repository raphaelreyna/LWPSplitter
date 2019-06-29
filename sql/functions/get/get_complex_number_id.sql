CREATE OR REPLACE FUNCTION get_complex_number_id(re_part DOUBLE PRECISION, im_part DOUBLE PRECISION) RETURNS BIGINT AS
$$
BEGIN 
RETURN (
SELECT id FROM complex_numbers WHERE real_part=re_part AND imaginary_part=im_part
);
END; $$
LANGUAGE PLPGSQL;
