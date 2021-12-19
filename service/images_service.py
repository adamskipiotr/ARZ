import sqlite3

from domain.dto.animal_rating import AnimalRating

DATABASE = 'database.db'


class ImagesService:

    def update_animal_category_rating(self, animal_name, is_correct):
        con = sqlite3.connect(DATABASE)
        cur = con.cursor()
        attempts_rs = cur.execute(
            f"SELECT attempts FROM animals_recognition WHERE name='{animal_name}'").fetchone()
        number_of_attempts = attempts_rs[0]
        positives_rs = cur.execute(
            f"SELECT positive FROM animals_recognition WHERE name='{animal_name}'").fetchone()
        number_of_positives = positives_rs[0]
        number_of_attempts = number_of_attempts + 1
        if is_correct:
            number_of_positives = number_of_positives + 1
        cur.execute(
            f"UPDATE animals_recognition SET attempts = {number_of_attempts}, positive = {number_of_positives} WHERE name ='{animal_name}'")
        con.commit()
        con.close()

    def get_animals_category_rating(self):
        con = sqlite3.connect(DATABASE)
        cur = con.cursor()
        animals_rating = cur.execute(
            f"SELECT * FROM animals_recognition ").fetchall()
        animals_rating_list = []
        for animal_rating in animals_rating:
            animal_rating = AnimalRating(animal_rating[1], animal_rating[2], animal_rating[3])
            animals_rating_list.append(animal_rating)
        return animals_rating_list
