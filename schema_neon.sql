CREATE TABLE IF NOT EXISTS voyages (
    id SERIAL PRIMARY KEY,
    code_agent VARCHAR(10),
    annee INTEGER,
    trimestre VARCHAR(2),
    corridor VARCHAR(3),
    sens VARCHAR(10),
    societe_transport VARCHAR(50),
    poids_total_autorise NUMERIC(6,2),
    charge VARCHAR(3),
    type_marchandise TEXT,
    poids_chargement NUMERIC(6,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
