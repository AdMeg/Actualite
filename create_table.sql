CREATE TABLE IF NOT EXISTS thematique
(
    id SMALLSERIAL PRIMARY KEY NOT NULL,
    valeur VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS actu
(
    id BIGSERIAL PRIMARY KEY NOT NULL,
    contenu VARCHAR(1024),
    Thematique_ID INT,
    date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (Thematique_ID) REFERENCES thematique(id)
);

CREATE TABLE IF NOT EXISTS groupe
(
    id SMALLSERIAL PRIMARY KEY NOT NULL,
    nom VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS groupe_actu
(
    id SMALLSERIAL PRIMARY KEY NOT NULL,
    groupe_ID INT,
    actu_ID INT,
    FOREIGN KEY (groupe_ID) REFERENCES groupe(id),
    FOREIGN KEY (actu_ID) REFERENCES actu(id)
);

