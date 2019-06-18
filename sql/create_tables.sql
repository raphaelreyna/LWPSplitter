CREATE TABLE polynomial (
       id BIGSERIAL PRIMARY KEY,
       degree SMALLINT NOT NULL,
       code BIGINT NOT NULL,
       UNIQUE(degree, code)
);

CREATE TABLE complex_number (
       id BIGSERIAL PRIMARY KEY,
       real_part DOUBLE PRECISION NOT NULL,
       imaginary_part DOUBLE PRECISION NOT NULL,
       UNIQUE(real_part, imaginary_part)
);

CREATE TABLE root (
       id BIGSERIAL PRIMARY KEY,
       polynomial_id BIGINT NOT NULL,
       complex_number_id BIGINT NOT NULL,
       multiplicity SMALLINT NOT NULL,
       UNIQUE(polynomial_id, complex_number_id)
);
