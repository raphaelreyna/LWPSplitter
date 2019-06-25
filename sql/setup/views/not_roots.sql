CREATE VIEW not_roots AS
SELECT
  r.real_part,
  r.imaginary_part
FROM
  random_complex_numbers r
LEFT JOIN
  complex_numbers c
ON
  r.real_part = c.real_part
AND
  r.imaginary_part = c.imaginary_part
WHERE
  c.id
IS NULL;
