CREATE TABLE ILPI (
  id_institution integer PRIMARY KEY,
  intitution_username varchar(255) COMMENT 'Nome da ILPI',
  latitute float,
  longitude float
);

CREATE TABLE Residente (
  uuidv5 integer PRIMARY KEY,
  id_institution integer,
  full_name varchar(255),
  date_of_birth date,
  elder_age integer,
  sex integer,
  race integer,
  education integer
);

CREATE TABLE TempoInstituicao (
  uuidv5 integer PRIMARY KEY,
  id_institution integer,
  intitution_time_year integer COMMENT 'tempo institucionalizado'
);

CREATE TABLE SuporteFamiliar (
  uuidv5 integer PRIMARY KEY,
  id_institution integer,
  family_support integer COMMENT 'suporte da familia'
);

CREATE TABLE GrauDependencia (
  uuidv5 integer PRIMARY KEY,
  id_institution integer,
  dependence_degree integer COMMENT 'grau dependência'
);

CREATE TABLE QtdeMedicTot (
  uuidv5 integer PRIMARY KEY,
  id_institution integer,
  tot_medicin integer COMMENT 'numero de medicamentos'
);

CREATE TABLE Morbidades (
  uuidv5 integer PRIMARY KEY,
  id_institution integer,
  soma_morbidities integer
);

CREATE TABLE EstadoSaude (
  uuidv5 integer PRIMARY KEY,
  id_institution integer,
  health_condition integer COMMENT 'estado de saude'
);

-- CREATE TABLE emergencia (
--   uuidv5 integer PRIMARY KEY,
--   id_institution integer,
--   family_support integer COMMENT 'atendimentos em UPA'
-- );

CREATE TABLE Hospitalizacao (
  uuidv5 integer PRIMARY KEY,
  id_institution integer,
  elder_hospitalization integer COMMENT 'hospitalizacoes'
);

CREATE TABLE mpiScore (
  uuidv5 integer PRIMARY KEY,
  id_institution integer,
  full_name varchar(255),
  score_social float,
  score_abvd float,
  score_mobility float,
  score_falls float,
  score_inpatient float,
  score_nutrition float,
  score_comorb float,
  score_drugs float,
  score_nursing float,
  MPI float,
  risk varchar(25)
);


,





