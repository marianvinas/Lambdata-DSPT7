from pdb import set_trace as breakpoint


class Dog():
    def __init__(self, name, age, housebroke=True):
        self.name = name
        self.age = age
        self.housebroke = housebroke

    def bark(self):
        print(f'{self.name} likes to bark!')


class Beagle(Dog):
    def __init__(self, name, age, housebroke=True, barks_alot=True):
        super().__init__(name, age, housebroke)
        self.barks_alot = barks_alot

    def bark(self):
        if self.barks_alot == True:
            print(f'{self.name} likes to bark!')
        else: 
            print(f'{self.name} hates to bark!')


if __name__ == "__main__":
    
    lucky = Dog("Lucky", 3)
    spike = Beagle("Spike", 7, barks_alot=False)
    breakpoint()