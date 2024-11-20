import random
from datetime import datetime


ANIMAL_FILE = "arrivingAnimals.txt"
NAME_FILE = "animalnames.txt"
OUTPUT_FILE = "zooPopulation.txt"


birthday_Months = {
    "spring": 4,
    "summer": 7,
    "fall": 10,
    "winter": 1
}

HyenaID = 0
LionID = 0
TigerID = 0
BearID = 0


def read_animal_data(file_path):
    animals = []
    with open(file_path, "r") as file:
        for line in file:
            parts = line.strip().split(", ")
            animals.append({
                "age": int(parts[0].split()[0]),
                "sex": parts[0].split()[2],
                "species": parts[0].split()[-1],
                "birth_season": parts[1].split()[-1],
                "color": parts[2],
                "weight": int(parts[3].split()[0]),
                "origin": parts[4]
            })
    return animals


def read_names(file_path):

    speciesNames = {}
    with open(file_path, "r") as file:
        species = ""
        for line in file:
            line = line.strip()
            if line.endswith("Names:"):
                species = line.split()[0]
                speciesNames[species.lower()] = []
            elif line and species:
                speciesNames[species.lower()].extend(line.split(", "))

    return speciesNames


def gen_birth_date(age, birth_season):

    if birth_season == "season": #also as unknown
        birth_season = "spring"


    current_year = datetime.now().year
    birth_year = current_year - age



    month = birthday_Months.get(birth_season.lower(), 1)
    return datetime(birth_year, month, 1).date().isoformat()





def gen_unique_id(species):
    global HyenaID, LionID, TigerID, BearID

    if species == "hyena":
        HyenaID += 1
        return HyenaID
    elif species == "lion":
        LionID += 1
        return LionID
    elif species == "tiger":
        TigerID += 1
        return TigerID
    elif species == "bear":
        BearID += 1
        return BearID




def assign_names_and_ids(animals, names):

    used_names = []
    for animal in animals:
        species = animal["species"]
        available_names = [name for name in names[species] if name not in used_names]
        name = random.choice(available_names)
        used_names.extend(name)
        animal["name"] = name
        animal["id"] = gen_unique_id(species)









def organize_habitats(animals):
    habitats = {}
    for animal in animals:
        species = animal["species"]
        if species not in habitats:
            habitats[species] = []
        habitats[species].append(animal)
    return habitats


def write_zoo_population(habitats, file_path):
    with open(file_path, "w") as file:
        for species, animals in habitats.items():
            file.write(f"{species.capitalize()} Habitat:\n")
            for animal in animals:
                file.write(
                    f"ID: {animal['id']}, Name: {animal['name']}, "
                    f"Age: {animal['age']}, Sex: {animal['sex']}, "
                    f"Color: {animal['color']}, Weight: {animal['weight']} lbs, "
                    f"Origin: {animal['origin']}, Birthday: {animal['birth_date']}\n"
                )
            file.write("\n")


animals = read_animal_data(ANIMAL_FILE)
names = read_names(NAME_FILE)

for animal in animals:
    animal["birth_date"] = gen_birth_date(animal["age"], animal["birth_season"])


assign_names_and_ids(animals, names)


habitats = organize_habitats(animals)

write_zoo_population(habitats, OUTPUT_FILE)
