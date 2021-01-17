import yaml
import random


def main():
    stream = open("data.yaml", "r")
    d = yaml.load(stream)
    sets = d["sets"]
    game = GameObj(sets)
    teams = game.find_teams(4)
    print(teams)


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class GameObj(metaclass=Singleton):
    def __init__(self, set_list) -> None:
        super().__init__()
        self.sets = []
        for set_dict in set_list:
            self.sets.append(Set(self, set_dict))
        self.factions = []
        for set in self.sets:
            for faction in set.factions:
                self.factions.append(faction)
        #Set availability:
        self.available_factions = []
        self.unavailable_factions = []
        for faction in self.factions:
            if faction.enabled == True:
                self.available_factions.append(faction)
            else:
                self.unavailable_factions.append(faction)        

    def disable_faction(self, faction):
        self.available_factions.pop(self.available_factions.index(faction))
        self.unavailable_factions.append(faction)
        faction._disable()

    def enable_faction(self, faction):
        self.available_factions.append(faction)
        self.unavailable_factions.pop(self.unavailable_factions.index(faction))
        faction._enable()

    def find_faction_by_name(self, faction_name):
        for faction in self.faction:
            if faction.name == faction_name:
                return faction
        return None
    
    def find_set_by_name(self, set_name):
        for set in self.sets:
            if set.name == set_name:
                return set
        return None
    
    def rnd_faction(self):
        rnd = random.randrange(0, len(self.available_factions))
        return self.available_factions[rnd]

    def find_team(self):
        f1 = self.rnd_faction()
        self.disable_faction(f1)
        f2 = self.rnd_faction()
        self.disable_faction(f2)
        return (f1, f2)

    
    def find_teams(self, num_of_players):
        generator = self.__teams_gen(num_of_players)
        teams = []
        try:
            while True:
                team = next(generator)
                teams.append(team)
        except StopIteration:
            pass
        finally:
            del generator
        return teams
        
    
    def __teams_gen(self, number_of_players):
        player = 1
        while player <= number_of_players:
            yield self.find_team()
            player += 1


class Readable():
    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.name


class Faction(Readable):
    def __init__(self, gameobj, faction_dict, available):
        self.name = faction_dict["name"]
        self.gameobj = gameobj
        if available:
            self.enabled = faction_dict["enabled"]
        else:
            self.enabled = False
    
    def disable(self):
        self.gameobj.disable_faction(self)
    
    def _disable(self):
        self.enabled = False

    def enable(self):
        self.gameobj.enable_faction(self)

    def _enable(self):
        self.enabled = True


class Set(Readable):
    def __init__(self, gameobj, set_dict):
        self.name = set_dict["name"]
        self.available = set_dict["available"]
        self.gameobj = gameobj
        factions = []
        try:
            for faction in set_dict["factions"]:
                factions.append(Faction(gameobj, faction, self.available))
        except KeyError:
            pass
        self.factions = factions

    def make_available(self):
        for faction in self.factions:
            faction.enable()
        self.available = True

    def make_unavailable(self):
        for faction in self.factions:
            faction.disable()
        self.available = False
        


if __name__ == "__main__":
    main()