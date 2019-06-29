CREATE VIEW polynomial_roots AS
SELECT
  r.id id,
  p.degree degree,
  p.code code,
  c.real_part real_part,
  c.imaginary_part imaginary_part,
  r.multiplicity multiplicity
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
