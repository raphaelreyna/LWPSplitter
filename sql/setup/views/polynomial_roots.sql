CREATE VIEW polynomial_roots AS
SELECT
  r.id,
  p.degree,
  p.code,
  c.real_part,
  c.imaginary_part,
  r.multiplicity
FROM
  roots r
JOIN
  polynomials p
ON
  r.polynomial_id = p.id
JOIN
  complex_numbers c
ON
  r.complex_number_id = c.id;
