import psycopg2 as pg  
import pandas as pd
import numpy as np
import requests

def table_setup(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            """)
        tables = cursor.fetchall()
        tables = [table[0] for table in tables]
        if 'Moves' not in tables:
            query = """
                CREATE TABLE IF NOT EXISTS Moves (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(50),
                    type VARCHAR(50),
                    power SMALLINT CHECK(power BETWEEN 0 AND 100),
                    energy SMALLINT CHECK(energy BETWEEN 0 AND 100),
                    duration SMALLINT CHECK(duration BETWEEN 0 AND 100),
                    damage_window SMALLINT CHECK(damage_window BETWEEN 0 AND 100)
                );
            """
            cursor.execute(query)
            connection.commit()
        if 'typechart' not in tables:
            query = """
                CREATE TABLE IF NOT EXISTS TypeChart (
                    id SERIAL PRIMARY KEY,
                    type1 VARCHAR(50),
                    type2 VARCHAR(50),
                    Bug NUMERIC(3, 2) CHECK (Bug IN (0, 0.25, 0.5, 1, 2, 4)),
                    Dark NUMERIC(3, 2) CHECK (Dark IN (0, 0.25, 0.5, 1, 2, 4)),
                    Dragon NUMERIC(3, 2) CHECK (Dragon IN (0, 0.25, 0.5, 1, 2, 4)),
                    Electric NUMERIC(3, 2) CHECK (Electric IN (0, 0.25, 0.5, 1, 2, 4)),
                    Fairy NUMERIC(3, 2) CHECK (Fairy IN (0, 0.25, 0.5, 1, 2, 4)),
                    Fighting NUMERIC(3, 2) CHECK (Fighting IN (0, 0.25, 0.5, 1, 2, 4)),
                    Fire NUMERIC(3, 2) CHECK (Fire IN (0, 0.25, 0.5, 1, 2, 4)),
                    Flying NUMERIC(3, 2) CHECK (Flying IN (0, 0.25, 0.5, 1, 2, 4)),
                    Ghost NUMERIC(3, 2) CHECK (Ghost IN (0, 0.25, 0.5, 1, 2, 4)),
                    Grass NUMERIC(3, 2) CHECK (Grass IN (0, 0.25, 0.5, 1, 2 ,4)),
                    Ground NUMERIC(3 ,2) CHECK(Ground IN (0 ,0.25 ,0.5 ,1 ,2 ,4)), 
                    Ice NUMERIC(3 ,2) CHECK(Ice IN (0 ,0.25 ,0.5 ,1 ,2 ,4)),
                    Normal NUMERIC(3 ,2) CHECK(Normal IN (0 ,0.25 ,0.5 ,1 ,2 ,4)), 
                    Poison NUMERIC(3 ,2) CHECK(Poison IN (0 ,0 .25 ,0.5 ,1 ,2 ,4)),
                    Psychic NUMERIC(3 ,2) CHECK(Psychic IN (0 ,0.25 ,0.5 ,1 ,2 ,4)),
                    Rock NUMERIC(3 ,2) CHECK(Rock IN (0 ,0.25 ,0.5 ,1 ,2 ,4)),
                    Steel NUMERIC(3 ,2) CHECK(Steel IN (0 ,0.25 ,0.5 ,1 ,2 ,4)),
                    Water NUMERIC(3 ,2) CHECK(Water IN (0 ,0.25 ,0.5 ,1 ,2 ,4))
                );
            """
            cursor.execute(query)
            connection.commit() 
            try:
                types = ['Bug', 'Dark', 'Dragon', 'Electric', 'Fairy', 'Fighting', 'Fire', 'Flying', 'Ghost', 'Grass', 'Ground', 'Ice', 'Normal', 'Poison', 'Psychic', 'Rock', 'Steel', 'Water']
                print(f"{len(types)} types in the list")
                #this one creates a list of tuples with all the possible combinations of types by running a nested loop and skipping the ones that have already been added. but using a list comprehension
                dual_types = [(types[i], types[j]) for i in range(len(types)) for j in range(i, len(types))]
                print (f"{len(dual_types)} dual types in the total") #must be 171 dual types total
                type_chart = pd.DataFrame(
                    np.ones((len(dual_types), len(types))),
                    index=pd.MultiIndex.from_tuples(dual_types, names=['Type1', 'Type2']),
                    columns=types
                )
                # type effectiveness, attacker type is the index, defender type is the column
                super_effective = {
                    'Bug': ['Grass', 'Psychic', 'Dark'],
                    'Dark': ['Ghost', 'Psychic'],
                    'Dragon': ['Dragon'],
                    'Electric': ['Flying', 'Water'],
                    'Fairy': ['Dragon', 'Dark', 'Fighting'],
                    'Fighting': ['Normal', 'Ice', 'Rock', 'Dark', 'Steel'],
                    'Fire': ['Bug', 'Grass', 'Ice', 'Steel'],
                    'Flying': ['Bug', 'Fighting', 'Grass'],
                    'Ghost': ['Ghost', 'Psychic'],
                    'Grass': ['Ground', 'Rock', 'Water'],
                    'Ground': ['Electric', 'Fire', 'Poison', 'Rock', 'Steel'],
                    'Ice': ['Dragon', 'Flying', 'Grass', 'Ground'],
                    'Poison': ['Fairy', 'Grass'],
                    'Psychic': ['Fighting', 'Poison'],
                    'Rock': ['Bug', 'Fire', 'Flying', 'Ice'],
                    'Steel': ['Fairy', 'Ice', 'Rock'],
                    'Water': ['Fire', 'Ground', 'Rock']
                }
                not_very_effective = {
                    'Bug': ['Fighting', 'Fire', 'Flying', 'Ghost', 'Poison', 'Steel', 'Fairy'],
                    'Dark': ['Dark', 'Fairy', 'Fighting'],
                    'Dragon': ['Steel'],
                    'Electric': ['Dragon', 'Electric', 'Grass'],
                    'Fairy': ['Fire', 'Poison', 'Steel'],
                    'Fighting': ['Bug', 'Fairy', 'Flying', 'Poison', 'Psychic'],
                    'Fire': ['Dragon', 'Fire', 'Rock', 'Water'],
                    'Flying': ['Electric', 'Rock', 'Steel'],
                    'Ghost': ['Dark'],
                    'Grass': ['Bug', 'Dragon', 'Fire', 'Flying', 'Grass', 'Poison', 'Steel'],
                    'Ground': ['Bug', 'Grass'],
                    'Ice': ['Fire', 'Ice', 'Steel', 'Water'],
                    'Normal': ['Rock', 'Steel'],
                    'Poison': ['Ghost', 'Ground', 'Poison', 'Rock'],
                    'Psychic': ['Psychic', 'Steel'],
                    'Rock': ['Fighting', 'Ground', 'Steel'],
                    'Steel': ['Electric', 'Fire', 'Steel', 'Water'],
                    'Water': ['Dragon', 'Grass', 'Water']
                }
                no_effect = {
                    'Normal': ['Ghost'],
                    'Fighting': ['Ghost'],
                    'Flying': ['Ground'],
                    'Poison': ['Steel'],
                    'Ground': ['Flying'],
                    'Ghost': ['Normal', 'Psychic'],
                    'Electric': ['Ground'],
                    'Psychic': ['Dark'],
                    'Dragon': ['Fairy']
                }

                # Update the DataFrame
                def update_chart(effectiveness_dict, value):
                    for attacker, targets in effectiveness_dict.items():
                        for target in targets:
                            type_chart.loc[(target, slice(None)), attacker] = value
                            type_chart.loc[(slice(None), target), attacker] *= value
                            type_chart.at[(target, target), attacker] = value

                # Apply updates
                update_chart(super_effective, 2)
                update_chart(not_very_effective, 0.5)
                update_chart(no_effect, 0)
                #insert dataframe into the table
                for index, row in type_chart.iterrows():
                    # Combine index and row values into a single list
                    values = list(index) + list(row)
                    # Format the values with single quotes and join them with commas
                    formatted_values = ", ".join(["'{}'".format(i) for i in values])
                    cursor.execute(
                        """
                        INSERT INTO TypeChart (type1, type2,
                        Bug, Dark, Dragon, Electric, Fairy,
                        Fighting, Fire, Flying, Ghost, Grass,
                        Ground, Ice, Normal, Poison, Psychic, Rock, Steel, Water) 
                        VALUES ({});
                        """.format(formatted_values)
                    )
                connection.commit()
                
                cursor.close()
            except Exception as e:
                print(f"Error: {e}")
        if 'GoStorage' not in tables:
            query = """
                CREATE TABLE IF NOT EXISTS GoStorage (
                    id SERIAL PRIMARY KEY,
                    pokemon_name VARCHAR(50),
                    species_id SMALLINT,
                    FOREIGN key (species_id) REFERENCES Pokedex(id),
                    type SMALLINT,
                    FOREIGN key (type) REFERENCES TypeChart(id),
                    attack_iv SMALLINT CHECK(attack_iv BETWEEN 0 AND 15),
                    defence_iv SMALLINT CHECK(defence_iv BETWEEN 0 AND 15),
                    hp_iv SMALLINT CHECK(hp_iv BETWEEN 0 AND 15),
                    level SMALLINT CHECK(level BETWEEN 1 AND 100),
                    combat_power SMALLINT,
                    is_shiny BOOLEAN DEFAULT FALSE,
                    is_shadow BOOLEAN DEFAULT FALSE,
                    weight SMALLINT,
                    height SMALLINT,
                    exhibition_score SMALLINT,
                    is_xl BOOLEAN DEFAULT FALSE,
                    is_xs BOOLEAN DEFAULT FALSE,
                    is_favorite BOOLEAN DEFAULT FALSE,
                    is_best_buddy BOOLEAN DEFAULT FALSE,
                    has_costume INTEGER DEFAULT 0,
                    FastMove SMALLINT,
                    ChargeMove1 SMALLINT,
                    ChargeMove2 SMALLINT,
                    FOREIGN KEY (FastMove) REFERENCES Moves(id),
                    FOREIGN KEY (ChargeMove1) REFERENCES Moves(id),
                    FOREIGN KEY (ChargeMove2) REFERENCES Moves(id),
                    caugth_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """
        if 'Pokedex' not in tables:
            query = """"
                CREATE TABLE IF NOT EXISTS Pokedex (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(50),
                    Types smallINT,
                    FOREIGN key (Types) REFERENCES TypeChart(id),
                    height SMALLINT CHECK(height BETWEEN 0 AND 100),
                    weight SMALLINT CHECK(weight BETWEEN 0 AND 100),
                    stats JSONB,
                    types JSONB,
                    url VARCHAR(255),
                    evolution SMALLINT,
                    
                );
                """ 
            cursor.execute(query)
            connection.commit()
        if 'GoDex' not in tables:
            query = """
                CREATE TABLE IF NOT EXISTS GoDex (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(50),
                    species_id SMALLINT,
                    FOREIGN key (species_id) REFERENCES Pokedex(id),
                    type SMALLINT,
                    FOREIGN key (type) REFERENCES TypeChart(id),
                    attack_stat SMALLINT,
                    defence_stat SMALLINT,
                    stamina_stat SMALLINT,
                    average_weight SMALLINT,
                    max_weight SMALLINT,
                    average_height SMALLINT,
                    max_height SMALLINT,
                );
            """
            cursor.execute(query)
            connection.commit()
        cursor.close()
    except Exception as e:
        print(f"Error: {e}")

def data_fetching():
    url = "https://pokeapi.co/api/v2/pokemon?limit=100000&offset=0"
    response = requests.get(url)
    
    if response.status_code == 200:
        pokemon_list = response.json()['results']
        all_pokemon_data = []
        i = 1
        for entry in pokemon_list:
            endpoint = entry['url']
            response = requests.get(endpoint)
            print (f"{i/1302 * 100:.2f}% done")
            i += 1
            if response.status_code == 200:
                data = response.json()
                pokemon_stats = {
                    'name': data['name'],
                    'id': data['id'],
                    'height': data['height'],
                    'weight': data['weight'],
                    'stats': {stat['stat']['name']: stat['base_stat'] for stat in data['stats']},
                    'types': [type_info['type']['name'] for type_info in data['types']],
                    'url': endpoint
                }
                all_pokemon_data.append(pokemon_stats)
            else:
                print(f"Failed to fetch data for {entry['name']}")
        
        df = pd.DataFrame(all_pokemon_data)
        df.to_csv('pokemon_data.csv', index=True)
        print("Data fetched successfully")
        return df
    else:
        print(f"Failed to fetch data. error code: {response.status_code}\n {response.text}")
        return None

if __name__ == "__main__":
    data_fetching()