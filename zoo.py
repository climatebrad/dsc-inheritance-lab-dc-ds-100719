"""Zoo classes for Flatiron DataScience OOP inheritance lab."""

import re

class Animal:
    """Superclass Animal.
Mandatory properties:
    name, which is a string set at instantation time
    weight, which is an integer set at instantiation time.
    size, which can be 'small', 'medium', 'large', or 'enormous'.

Optional properties:
    species, a string that tells us the species of the animal
    food_type, which can be 'herbivore', 'carnivore', or 'omnivore' (default 'omnivore')
    nocturnal, a boolean value that is True if the animal sleeps during the day,
            otherwise False (default False)
    """

    def __init__(self, name: str, weight: int, size: str, nocturnal=False, **kwargs):
        self.name = name

        # settable property
        if self._validate_weight(weight):
            self._weight = weight

        # unsettable properties
        if self._validate_size(size):
            self._size = size

        self._nocturnal = nocturnal

        # set species from class (or subclass) name
        self._species = kwargs.get('species', type(self).__name__)

        food_type = kwargs.get('food_type', 'omnivore')
        if self._validate_food_type(food_type):
            self._food_type = food_type

        # utility attribute that converts from food_type to food name
        self._eats = {'plants' : ['herbivore', 'omnivore'],
                      'meat' : ['carnivore', 'omnivore']}

    def __repr__(self):
        return f"<{type(self).__name__}: {str(self.__dict__)}>"

    @staticmethod
    def of_species(species_name: str):
        """Returns an animal of class species_name."""
        return list(filter(lambda species:
                           species.__name__ == species_name,
                           Animal.__subclasses__()))[0]

    @property
    def species(self):
        """species"""
        return self._species

    @property
    def size(self):
        """size"""
        return self._size

    @property
    def nocturnal(self):
        """nocturnal"""
        return self._nocturnal

    @property
    def diurnal(self):
        """diurnal"""
        return not self.nocturnal

    @property
    def food_type(self):
        """food_type"""
        return self._food_type

    @property
    def weight(self):
        """weight"""
        return self._weight

    @weight.setter
    def weight(self, weight):
        if self._validate_weight(weight):
            self._weight = weight

    @staticmethod
    def _validate_size(size):
        valid_size = ['small', 'medium', 'large', 'enormous']
        if size not in valid_size:
            raise ValueError(f"results: size must be one of {valid_size}")
        return True

    @staticmethod
    def _validate_weight(weight):
        if weight < 0:
            raise ValueError(f"results: weight must be greater than or equal to 0")
        return True

    @staticmethod
    def _validate_food_type(food_type):
        valid_food_type = ['herbivore', 'carnivore', 'omnivore']
        if food_type not in valid_food_type:
            raise ValueError(f"results: food_type must be one of {valid_food_type}")
        return True

    def sleep(self):
        """Prints time of sleep based on whether the animal is nocturnal."""
        if self.nocturnal:
            sleep_time = 'day'
        else:
            sleep_time = 'night'
        print(f"I sleep during the {sleep_time}.")

    def eat(self, food: str):
        """Prints whether the animal likes to eat plants, meat, or both."""
        valid_food = ['plants', 'meat']
        if food not in valid_food:
            raise ValueError(f"results: food must be one of {valid_food}")

        if self.food_type in self._eats[food]:
            verb = "are" if food.endswith('s') else "is"
            print(f"{self.name} the {self.species} thinks {food} {verb} yummy!")
        else:
            print("I don't eat this!")

class Elephant(Animal):
    """An enormous animal."""

    def __init__(self, name, weight):
        super().__init__(name,
                         weight,
                         size='enormous',
                         food_type='herbivore',
                         nocturnal=False)

class Tiger(Animal):
    """The ferocious carnivore."""
    def __init__(self, name, weight):
        super().__init__(name,
                         weight,
                         size='large',
                         food_type='carnivore',
                         nocturnal=True)

class Raccoon(Animal):
    """A rascally bandit."""
    def __init__(self, name, weight):
        super().__init__(name,
                         weight,
                         size='small',
                         food_type='omnivore',
                         nocturnal=True)

class Gorilla(Animal):
    """Lives in the mist."""
    def __init__(self, name, weight):
        super().__init__(name,
                         weight,
                         size='large',
                         food_type='herbivore',
                         nocturnal=False)

class Zoo:
    """Smart list of animals."""
    def __init__(self, animals: list = None):
        if animals:
            self.animals = animals
        else:
            self.animals = []

    def __repr__(self):
        return f"<Zoo: {self.animals}>"

    def add_animal(self, animal):
        """Add an animal to the zoo."""
        self.animals.append(animal)

    def add_animals(self, animals: list):
        """Add a list of animals to the zoo."""
        self.animals.extend(animals)

    def add_animal_by_attributes(self, animal_type: str, name: str, weight: int):
        """Add animal of type animal_type to zoo."""
        only_letters = re.compile("[a-zA-Z]")
        animal_type = "".join(only_letters.findall(animal_type)).capitalize()
        animal = Animal.of_species(animal_type)(name, weight)
        self.add_animal(animal)

    def feed_animals(self, time: str = 'day'):
        """Feed the animals that are awake."""
        time = time.lower()
        if time not in ['day', 'night']:
            raise ValueError(f"results: time must be one of 'Day' or 'Night'")

        for animal in self.animals:
            if ((time == 'day') and animal.nocturnal) \
                or ((time == 'night') and animal.diurnal):
                continue
            if animal.food_type == 'carnivore':
                animal.eat('meat')
            else:
                animal.eat('plants')
