CREATE TABLE random_complex_numbers (
             id BIGSERIAL PRIMARY KEY,
             real_part DOUBLE PRECISION NOT NULL,
             imaginary_part DOUBLE PRECISION NOT NULL,
             UNIQUE(real_part, imaginary_part)
);
