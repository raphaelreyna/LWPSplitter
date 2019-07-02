CREATE TABLE roots (
       id BIGSERIAL PRIMARY KEY,
       polynomial_id BIGINT NOT NULL,
       complex_number_id BIGINT NOT NULL,
       multiplicity SMALLINT NOT NULL,
       UNIQUE(polynomial_id, complex_number_id)
);
