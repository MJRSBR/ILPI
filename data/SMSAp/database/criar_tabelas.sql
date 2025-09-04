CREATE TABLE `instituicao` (
  `id_ilpi` integer PRIMARY KEY,
  `intitution_username` varchar(255) COMMENT 'Nome da ILPI',
  `latitute` float,
  `longitude` float
);

CREATE TABLE `residentes_ILPI` (
  `id_uuid` integer PRIMARY KEY,
  `id_ilpi` integer,
  `full_name` varchar(255),
  `date_of_birth` date,
  `elder_age` integer,
  `sex` integer,
  `race` integer
);

CREATE TABLE `tempo_instituicao` (
  `id_uuid` integer PRIMARY KEY,
  `id_ilpi` integer,
  `tempo` integer COMMENT 'tempo institucionalizado'
);

CREATE TABLE `suporte_familiar` (
  `id_uuid` integer PRIMARY KEY,
  `id_ilpi` integer,
  `family_support` integer COMMENT 'suporte da familia'
);

CREATE TABLE `grau_dependencia` (
  `id_uuid` integer PRIMARY KEY,
  `id_ilpi` integer,
  `dependence_degree` integer COMMENT 'grau dependência'
);

CREATE TABLE `contagem_medicamentos` (
  `id_uuid` integer PRIMARY KEY,
  `id_ilpi` integer,
  `tot_medic` integer COMMENT 'numero de medicamentos'
);

CREATE TABLE `morbidades` (
  `id_uuid` integer PRIMARY KEY,
  `id_ilpi` integer,
  `Morbidades` integer COMMENT 'morbidades',
  `other_morbidities` varchar(255),
  `soma_morbidities` integer
);

CREATE TABLE `estado_saude` (
  `id_uuid` integer PRIMARY KEY,
  `id_ilpi` integer,
  `health_condition` integer COMMENT 'estado de saude'
);

CREATE TABLE `emergencia` (
  `id_uuid` integer PRIMARY KEY,
  `id_ilpi` integer,
  `family_support` integer COMMENT 'atendimentos em UPA'
);

CREATE TABLE `hospitalizacao` (
  `id_uuid` integer PRIMARY KEY,
  `id_ilpi` integer,
  `family_support` integer COMMENT 'hospitalizacoes'
);

ALTER TABLE `residentes_ILPI` ADD FOREIGN KEY (`id_ilpi`) REFERENCES `instituicao` (`id_ilpi`);

CREATE TABLE `tempo_instituicao_residentes_ILPI` (
  `tempo_instituicao_id_ilpi` integer,
  `residentes_ILPI_id_ilpi` integer,
  PRIMARY KEY (`tempo_instituicao_id_ilpi`, `residentes_ILPI_id_ilpi`)
);

ALTER TABLE `tempo_instituicao_residentes_ILPI` ADD FOREIGN KEY (`tempo_instituicao_id_ilpi`) REFERENCES `tempo_instituicao` (`id_ilpi`);

ALTER TABLE `tempo_instituicao_residentes_ILPI` ADD FOREIGN KEY (`residentes_ILPI_id_ilpi`) REFERENCES `residentes_ILPI` (`id_ilpi`);


CREATE TABLE `residentes_ILPI_suporte_familiar` (
  `residentes_ILPI_id_ilpi` integer,
  `suporte_familiar_id_ilpi` integer,
  PRIMARY KEY (`residentes_ILPI_id_ilpi`, `suporte_familiar_id_ilpi`)
);

ALTER TABLE `residentes_ILPI_suporte_familiar` ADD FOREIGN KEY (`residentes_ILPI_id_ilpi`) REFERENCES `residentes_ILPI` (`id_ilpi`);

ALTER TABLE `residentes_ILPI_suporte_familiar` ADD FOREIGN KEY (`suporte_familiar_id_ilpi`) REFERENCES `suporte_familiar` (`id_ilpi`);


CREATE TABLE `residentes_ILPI_grau_dependencia` (
  `residentes_ILPI_id_ilpi` integer,
  `grau_dependencia_id_ilpi` integer,
  PRIMARY KEY (`residentes_ILPI_id_ilpi`, `grau_dependencia_id_ilpi`)
);

ALTER TABLE `residentes_ILPI_grau_dependencia` ADD FOREIGN KEY (`residentes_ILPI_id_ilpi`) REFERENCES `residentes_ILPI` (`id_ilpi`);

ALTER TABLE `residentes_ILPI_grau_dependencia` ADD FOREIGN KEY (`grau_dependencia_id_ilpi`) REFERENCES `grau_dependencia` (`id_ilpi`);


CREATE TABLE `residentes_ILPI_contagem_medicamentos` (
  `residentes_ILPI_id_ilpi` integer,
  `contagem_medicamentos_id_ilpi` integer,
  PRIMARY KEY (`residentes_ILPI_id_ilpi`, `contagem_medicamentos_id_ilpi`)
);

ALTER TABLE `residentes_ILPI_contagem_medicamentos` ADD FOREIGN KEY (`residentes_ILPI_id_ilpi`) REFERENCES `residentes_ILPI` (`id_ilpi`);

ALTER TABLE `residentes_ILPI_contagem_medicamentos` ADD FOREIGN KEY (`contagem_medicamentos_id_ilpi`) REFERENCES `contagem_medicamentos` (`id_ilpi`);


CREATE TABLE `residentes_ILPI_morbidades` (
  `residentes_ILPI_id_ilpi` integer,
  `morbidades_id_ilpi` integer,
  PRIMARY KEY (`residentes_ILPI_id_ilpi`, `morbidades_id_ilpi`)
);

ALTER TABLE `residentes_ILPI_morbidades` ADD FOREIGN KEY (`residentes_ILPI_id_ilpi`) REFERENCES `residentes_ILPI` (`id_ilpi`);

ALTER TABLE `residentes_ILPI_morbidades` ADD FOREIGN KEY (`morbidades_id_ilpi`) REFERENCES `morbidades` (`id_ilpi`);


CREATE TABLE `residentes_ILPI_estado_saude` (
  `residentes_ILPI_id_ilpi` integer,
  `estado_saude_id_ilpi` integer,
  PRIMARY KEY (`residentes_ILPI_id_ilpi`, `estado_saude_id_ilpi`)
);

ALTER TABLE `residentes_ILPI_estado_saude` ADD FOREIGN KEY (`residentes_ILPI_id_ilpi`) REFERENCES `residentes_ILPI` (`id_ilpi`);

ALTER TABLE `residentes_ILPI_estado_saude` ADD FOREIGN KEY (`estado_saude_id_ilpi`) REFERENCES `estado_saude` (`id_ilpi`);


CREATE TABLE `residentes_ILPI_emergencia` (
  `residentes_ILPI_id_ilpi` integer,
  `emergencia_id_ilpi` integer,
  PRIMARY KEY (`residentes_ILPI_id_ilpi`, `emergencia_id_ilpi`)
);

ALTER TABLE `residentes_ILPI_emergencia` ADD FOREIGN KEY (`residentes_ILPI_id_ilpi`) REFERENCES `residentes_ILPI` (`id_ilpi`);

ALTER TABLE `residentes_ILPI_emergencia` ADD FOREIGN KEY (`emergencia_id_ilpi`) REFERENCES `emergencia` (`id_ilpi`);


CREATE TABLE `residentes_ILPI_hospitalizacao` (
  `residentes_ILPI_id_ilpi` integer,
  `hospitalizacao_id_ilpi` integer,
  PRIMARY KEY (`residentes_ILPI_id_ilpi`, `hospitalizacao_id_ilpi`)
);

ALTER TABLE `residentes_ILPI_hospitalizacao` ADD FOREIGN KEY (`residentes_ILPI_id_ilpi`) REFERENCES `residentes_ILPI` (`id_ilpi`);

ALTER TABLE `residentes_ILPI_hospitalizacao` ADD FOREIGN KEY (`hospitalizacao_id_ilpi`) REFERENCES `hospitalizacao` (`id_ilpi`);






