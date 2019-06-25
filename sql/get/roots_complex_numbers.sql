SELECT {distinct}
  c.real_part,
  c.imaginary_part
FROM
  roots
INNER JOIN
  complex_number c
ON
  root.complex_number_id=c.id
INNER JOIN
  polynomial
ON
  root.polynomial_id=polynomial.id
WHERE
  polynomial.degree {relation} {degree};
