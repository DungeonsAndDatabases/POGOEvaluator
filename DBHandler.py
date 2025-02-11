import psycopg2 as pg  

def TableSetup (connection):
    try:
        cursor = connection.cursor()
        create_table_query = """
            CREATE TABLE IF NOT EXISTS GoStorage (
                id SERIAL PRIMARY KEY,
                pokemon_name VARCHAR(50),
                attack_iv SMALLINT CHECK(attack_iv BETWEEN 0 AND 15),
                defence_iv SMALLINT CHECK(defence_iv BETWEEN 0 AND 15),
                hp_iv SMALLINT CHECK(hp_iv BETWEEN 0 AND 15),
            );
            CREATE TABLE IF NOT EXISTS TypeChart (
                id SERIAL PRIMARY KEY,
                type1 VARCHAR(8),
                type2 VARCHAR(8),
                Bug NUMERIC(3, 2) CHECK (Bug IN (0, 0.25, 0.5, 1, 2, 4)),
                Dark NUMERIC(3, 2) CHECK (Dark IN (0, 0.25, 0.5, 1, 2, 4)),
                Dragon NUMERIC(3, 2) CHECK (Dragon IN (0, 0.25, 0.5, 1, 2, 4)),
                Electric NUMERIC(3, 2) CHECK (Electric IN (0, 0.25, 0.5, 1, 2, 4)),
                Fairy NUMERIC(3, 2) CHECK (Fairy IN (0, 0.25, 0.5, 1, 2, 4)),
                Fighting NUMERIC(3, 2) CHECK (Fighting IN (0, 0.25, 0.5, 1, 2, 4)),
                Fire NUMERIC(3, 2) CHECK (Fire IN (0, 0.25, 0.5, 1, 2, 4)),
                Flying NUMERIC(3, 2) CHECK (Flying IN (0, 0.25, 0.5, 1, 2, 4)),
                Ghost NUMERIC(3, 2) CHECK (Ghost IN (0, 0.25, 0.5, 1, 2, 4)),
                Grass NUMERIC(3, 2) CHECK (Grass IN (0, 0.25, 0.5, 1, 2, 4)),
                Ground NUMERIC(3, 2) CHECK (Ground IN (0, 0.25, 0.5, 1, 2, 4)), 
                Ice NUMERIC(3, 2) CHECK (Ice IN (0, 0.25, 0.5, 1, 2, 4)),
                Normal NUMERIC(3, 2) CHECK (Normal IN (0, 0.25, 0.5, 1, 2, 4)), 
                Poison NUMERIC(3, 2) CHECK (Poison IN (0, 0.25, 0.5, 1, 2, 4)),
                Psychic NUMERIC(3, 2) CHECK (Psychic IN (0, 0.25, 0.5, 1, 2, 4)),
                Rock NUMERIC(3, 2) CHECK (Rock IN (0, 0.25, 0.5, 1, 2, 4)),
                Steel NUMERIC(3, 2) CHECK (Steel IN (0, 0.25, 0.5, 1, 2, 4)),
                Water NUMERIC(3, 2) CHECK (Water IN (0, 0.25, 0.5, 1, 2, 4)),
            );
            """
        cursor.execute(create_table_query)
        connection.commit()
        types = ['None', 'Bug', 'Dark', 'Dragon', 'Electric', 'Fairy', 'Fighting', 'Fire', 'Flying', 'Ghost', 'Grass', 'Ground', 'Ice', 'Normal', 'Poison', 'Psychic', 'Rock', 'Steel', 'Water']

        interactions = {
            'Bug':      {'Bug': 1, 'Dark': 1, 'Dragon': 1, 'Electric': 1, 'Fairy': 1, 'Fighting': 0.5, 'Fire': 2, 'Flying': 2, 'Ghost': 1, 'Grass': 0.5, 'Ground': 0.5, 'Ice': 1, 'Normal': 1, 'Poison': 1, 'Psychic': 1, 'Rock': 2, 'Steel': 1, 'Water': 1},
            'Dark':     {'Bug': 2, 'Dark': 0.5, 'Dragon': 1, 'Electric': 1, 'Fairy': 2, 'Fighting': 2, 'Fire': 1, 'Flying': 1, 'Ghost': 0.5, 'Grass': 1, 'Ground': 1, 'Ice': 1, 'Normal': 1, 'Poison': 1, 'Psychic': 0, 'Rock': 1, 'Steel': 1, 'Water': 1},
            'Dragon':   {'Bug': 1, 'Dark': 1, 'Dragon': 2, 'Electric': 0.5, 'Fairy': 2, 'Fighting': 1, 'Fire': 0.5, 'Flying': 1, 'Ghost': 1, 'Grass': 0.5, 'Ground': 1, 'Ice': 2, 'Normal': 1, 'Poison': 1, 'Psychic': 1, 'Rock': 1, 'Steel': 1, 'Water': 0.5},
            'Electric': {'Bug': 1, 'Dark': 1, 'Dragon': 1, 'Electric': 0.5, 'Fairy': 1, 'Fighting': 1, 'Fire': 1, 'Flying': 0.5, 'Ghost': 1, 'Grass': 1, 'Ground': 2, 'Ice': 1, 'Normal': 1, 'Poison': 1, 'Psychic': 1, 'Rock': 1, 'Steel': 0.5, 'Water': 1},
            'Fairy':    {'Bug': 0.5, 'Dark': 0.5, 'Dragon': 0, 'Electric': 1, 'Fairy': 1, 'Fighting': 0.5, 'Fire': 1, 'Flying': 1, 'Ghost': 1, 'Grass': 1, 'Ground': 1, 'Ice': 1, 'Normal': 1, 'Poison': 2, 'Psychic': 1, 'Rock': 1, 'Steel': 2, 'Water': 1},
            'Fighting': {'Bug': 0.5, 'Dark': 0.5, 'Dragon': 1, 'Electric': 1, 'Fairy': 2, 'Fighting': 1, 'Fire': 1, 'Flying': 2, 'Ghost': 1, 'Grass': 1, 'Ground': 1, 'Ice': 1, 'Normal': 1, 'Poison': 1, 'Psychic': 2, 'Rock': 0.5, 'Steel': 1, 'Water': 1},
            'Fire':     {'Bug': 0.5, 'Dark': 1, 'Dragon': 1, 'Electric': 1, 'Fairy': 0.5, 'Fighting': 1, 'Fire': 0.5, 'Flying': 1, 'Ghost': 1, 'Grass': 0.5, 'Ground': 2, 'Ice': 0.5, 'Normal': 1, 'Poison': 1, 'Psychic': 1, 'Rock': 2, 'Steel': 0.5, 'Water': 2},
            'Flying':   {'Bug': 0.5, 'Dark': 1, 'Dragon': 1, 'Electric': 2, 'Fairy': 1, 'Fighting': 0.5, 'Fire': 1, 'Flying': 1, 'Ghost': 1, 'Grass': 0.5, 'Ground': 0, 'Ice': 2, 'Normal': 1, 'Poison': 1, 'Psychic': 1, 'Rock': 2, 'Steel': 1, 'Water': 1},
            'Ghost':    {'Bug': 0.5, 'Dark': 2, 'Dragon': 1, 'Electric': 1, 'Fairy': 1, 'Fighting': 0, 'Fire': 1, 'Flying': 1, 'Ghost': 2, 'Grass': 1, 'Ground': 1, 'Ice': 1, 'Normal': 0, 'Poison': 0.5, 'Psychic': 1, 'Rock': 1, 'Steel': 1, 'Water': 1},
            'Grass':    {'Bug': 1, 'Dark': 1, 'Dragon': 1, 'Electric': 1, 'Fairy': 1, 'Fighting': 1, 'Fire': 1, 'Flying': 1, 'Ghost': 1, 'Grass': 1, 'Ground': 1, 'Ice': 1, 'Normal': 1, 'Poison': 1, 'Psychic': 1, 'Rock': 1, 'Steel': 1, 'Water': 1},
            'Ground':   {'Bug': 1, 'Dark': 1, 'Dragon': 1, 'Electric': 1, 'Fairy': 1, 'Fighting': 1, 'Fire': 1, 'Flying': 1, 'Ghost': 1, 'Grass': 1, 'Ground': 1, 'Ice': 1, 'Normal': 1, 'Poison': 1, 'Psychic': 1, 'Rock': 1, 'Steel': 1, 'Water': 1},
            'Ice':      {'Bug': 1, 'Dark': 1, 'Dragon': 1, 'Electric': 1, 'Fairy': 1, 'Fighting': 1, 'Fire': 1, 'Flying': 1, 'Ghost': 1, 'Grass': 1, 'Ground': 1, 'Ice': 1, 'Normal': 1, 'Poison': 1, 'Psychic': 1, 'Rock': 1, 'Steel': 1, 'Water': 1},
            'Normal':   {'Bug': 1, 'Dark': 1, 'Dragon': 1, 'Electric': 1, 'Fairy': 1, 'Fighting': 1, 'Fire': 1, 'Flying': 1, 'Ghost': 1, 'Grass': 1, 'Ground': 1, 'Ice': 1, 'Normal': 1, 'Poison': 1, 'Psychic': 1, 'Rock': 1, 'Steel': 1, 'Water': 1},
            'Poison':   {'Bug': 1, 'Dark': 1, 'Dragon': 1, 'Electric': 1, 'Fairy': 1, 'Fighting': 1, 'Fire': 1, 'Flying': 1, 'Ghost': 1, 'Grass': 1, 'Ground': 1, 'Ice': 1, 'Normal': 1, 'Poison': 1, 'Psychic': 1, 'Rock': 1, 'Steel': 1, 'Water': 1},
            'Psychic':  {'Bug': 1, 'Dark': 1, 'Dragon': 1, 'Electric': 1, 'Fairy': 1, 'Fighting': 1, 'Fire': 1, 'Flying': 1, 'Ghost': 1, 'Grass': 1, 'Ground': 1, 'Ice': 1, 'Normal': 1, 'Poison': 1, 'Psychic': 1, 'Rock': 1, 'Steel': 1, 'Water': 1},
            'Rock':     {'Bug': 1, 'Dark': 1, 'Dragon': 1, 'Electric': 1, 'Fairy': 1, 'Fighting': 1, 'Fire': 1, 'Flying': 1, 'Ghost': 1, 'Grass': 1, 'Ground': 1, 'Ice': 1, 'Normal': 1, 'Poison': 1, 'Psychic': 1, 'Rock': 1, 'Steel': 1, 'Water': 1},
            'Steel':    {'Bug': 1, 'Dark': 1, 'Dragon': 1, 'Electric': 1, 'Fairy': 1, 'Fighting': 1, 'Fire': 1, 'Flying': 1, 'Ghost': 1, 'Grass': 1, 'Ground': 1, 'Ice': 1, 'Normal': 1, 'Poison': 1, 'Psychic': 1, 'Rock': 1, 'Steel': 1, 'Water': 1},
            'Water':    {'Bug': 1, 'Dark': 1, 'Dragon': 1, 'Electric': 1, 'Fairy': 1, 'Fighting': 1, 'Fire': 1, 'Flying': 1, 'Ghost': 1, 'Grass': 1, 'Ground': 1, 'Ice': 1, 'Normal': 1, 'Poison': 1, 'Psychic': 1, 'Rock': 1, 'Steel': 1, 'Water': 1},
        }
        cursor.execute(create_table_query)
        connection.commit()
        cursor.close()
    except Exception as e:
        print(f"Error: {e}")
if __name__ == "__main__":
    TableSetup()