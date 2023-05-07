import sys 
import sqlite3
from pymongo import MongoClient 

mongoClient = MongoClient("mongodb://localhost/pokemon")
pokemonDB = mongoClient['pokemondb']
pokemonColl = pokemonDB['pokemon_data']

conn = sqlite3.connect("pokemon.sqlite")



try:
        pokemonColl.drop()
        cursor = conn.cursor()
        gen_poke_q = """
                    SELECT
                        p.id,
                        p.name,
                        p.pokedex_number,
                        p.hp,
                        p.attack,
                        p.defense,
                        p.sp_attack,
                        p.sp_defense,
                        p.speed
                    FROM pokemon p
                    """
        gen_poke_data = cursor.execute(gen_poke_q).fetchall()

        for pokemon in gen_poke_data: 
                result_abilities = []
                abilities_q = """
                            SELECT a.name 
                            FROM ability a
                            JOIN pokemon_abilities p 
                            ON a.id = p.ability_id
                            WHERE p.pokemon_id=""" + "\"" + str(pokemon[0]) + "\""
                raw_abilities = cursor.execute(abilities_q).fetchall()
                for ability in raw_abilities:
                        curr = ability[0].strip("',")
                        result_abilities.append(curr)

                types_q = """
                        SELECT name, type1, type2
                        FROM pokemon_types_view p
                        WHERE p.name=""" + "\"" + str(pokemon[1]) + "\""
                raw_types = cursor.execute(types_q).fetchall()

                pokemon_record = {
                        "id": pokemon[0],
                        "name": pokemon[1],
                        "pokedex_number": pokemon[2],
                        "typeset": [raw_types[0][1], raw_types[0][2]],
                        "hp": pokemon[3],
                        "attack": pokemon[4],
                        "defense": pokemon[5],
                        "sp_attack": pokemon[6],
                        "sp_defense": pokemon[7],
                        "speed": pokemon[8],
                        "abilities": result_abilities                
                }

                pokemonColl.insert_one(pokemon_record)



        cursor2 = pokemonColl.find({})
        for doc in cursor2:
               print(doc)

finally:
    print(pokemonColl.count_documents({}))
    cursor.close()
    conn.close()
    mongoClient.close()
                
        


