CREATE TABLE polynomials (
       id BIGSERIAL PRIMARY KEY,
       degree SMALLINT NOT NULL,
       code BIGINT NOT NULL,
       UNIQUE(degree, code)
);
