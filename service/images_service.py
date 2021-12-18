import sqlite3

DATABASE = 'database.db'


class ImagesService:

    def updateAnimalCategoryRating(self, animalName, isCorrect):
        con = sqlite3.connect(DATABASE)
        cur = con.cursor()
        attempts_rs = cur.execute(
            f"SELECT attempts FROM animals_recognition WHERE name='{animalName}'").fetchone()
        number_of_attempts = attempts_rs[0]
        positives_rs = cur.execute(
            f"SELECT positive FROM animals_recognition WHERE name='{animalName}'").fetchone()
        number_of_positives = positives_rs[0]
        number_of_attempts = number_of_attempts + 1
        if isCorrect:
            number_of_positives = number_of_positives + 1
        cur.execute(
            f"UPDATE animals_recognition SET attempts = {number_of_attempts}, positive = {number_of_positives} WHERE name ='{animalName}'")
        con.commit()
        con.close()
