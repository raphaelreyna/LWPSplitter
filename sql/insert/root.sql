INSERT INTO roots (polynomial_id, complex_number_id, multiplicity)
VALUES (
       {polynomial},
       {complexNumber},
       {multiplicity}
       )
RETURNING id;
