import yaml
import random


def main():
    stream = open("data.yaml", "r")
    app_data = yaml.load(stream)
    stream.close()

    stream = open("save.yaml", "r") 
    save_data = yaml.load(stream)
    stream.close()

    print(save_data)
    game = GameModel(app_data, save_data)
    #game.make_set_available(game.find_set_by_name("Monster Smash"))
    #game.make_set_unavailable(game.find_set_by_name("Monster Smash"))
    #print(game.make_teams(4))
    game.save_data("save.yaml")


class GameModel():
    def __init__(self, raw_app_data, raw_save_data):
        # 0) pre-process raw data
        set_data = raw_app_data["sets"]
        available_set_names = raw_save_data["available sets"]
        disabled_factions = raw_save_data["disabled factions"]
        # 1) Make list of all sets, where the sets contain information of their respective factions
        self.supported_sets = self._init_supported_set_data(set_data)
        # 2) Make list of all available sets with references to the list of all sets
        self.available_sets = self._init_available_sets(available_set_names)
        # #) Put all factions of the active sets in a list, as long as they are not in the list of names of disabled factions
        self.enabled_factions = self._init_enabled_factions(disabled_factions)

    def _init_supported_set_data(self, loaded_data):
        supported_sets = []
        for set_dict in loaded_data:
            supported_sets.append(Set(self, set_dict))           
        return supported_sets
    
    def _init_available_sets(self, available_names):
        available_sets = []
        for set in self.supported_sets:
            if set.name in available_names:
                available_sets.append(set)
        return available_sets
    
    def _init_enabled_factions(self, disabled_names):
        enabled_factions = []
        for set in self.available_sets:
            for faction in set.factions:
                if faction.name not in disabled_names:
                    enabled_factions.append(faction)
        return enabled_factions
    
    def enable_faction(self, faction):
        if faction not in self.enabled_factions:
            self.enabled_factions.append(faction)
    
    def disable_faction(self, faction):
        if faction in self.enabled_factions:
            self.enabled_factions.pop(self.enabled_factions.index(faction))
    
    def make_set_available(self, set):
        self.available_sets.append(set)
        for faction in set.factions:
            self.enable_faction(faction)
    
    def make_set_unavailable(self, set):
        self.available_sets.pop(self.available_sets.index(set))
        for faction in set.factions:
            self.disable_faction(faction)

    def find_faction_by_name(self, faction_name):
        for set in self.supported_sets:
            for faction in set.factions:
                if faction.name == faction_name:
                    return faction
        raise KeyError("Faction '" + faction_name + "' was not found!")

    def find_set_by_name(self, set_name):
        for set in self.supported_sets:
            if set.name == set_name:
                return set
        raise KeyError("Set '" + set_name + "' was not found!")

    def _get_rnd_faction(self):
        rnd = random.randrange(0, len(self.enabled_factions))
        return self.enabled_factions[rnd]

    def _make_team(self):
        f1 = self._get_rnd_faction()
        self.disable_faction(f1)
        f2 = self._get_rnd_faction()
        self.disable_faction(f2)
        return (f1, f2)
    
    def make_teams(self, num_of_teams):
        team = 1
        teams = []
        # Make teams
        while team <= num_of_teams:
            teams.append(self._make_team())
            team += 1
        # Reset factions
        for team in teams:
            self.enable_faction(team[0])
            self.enable_faction(team[1])
        return teams
    
    def save_data(self, file_path):
        # serialize
        serialized_data = self.serialize_save()
        print(serialized_data)
        # save
        with open(file_path, "w") as file:
            yaml.dump(serialized_data, file)

    def serialize_save(self):
        # Availalbe sets
        disabled_faction_names = []
        available_set_names = []
        for set in self.available_sets:
            available_set_names.append(set.name)
            for faction in set.factions:
                if faction not in self.enabled_factions:
                    disabled_faction_names.append(faction.name)
        return {"available sets": available_set_names, "disabled factions": disabled_faction_names}


class Readable():
    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.name


class Faction(Readable):
    def __init__(self, model, faction_dict):
        self.name = faction_dict["name"]
        self.model = model
    
    def disable(self):
        self.model.disable_faction(self)

    def enable(self):
        self.model.enable_faction(self)


class Set(Readable):
    def __init__(self, model, set_dict):
        self.name = set_dict["name"]
        self.available = set_dict["available"]
        self.model = model
        factions = []
        try:
            for faction in set_dict["factions"]:
                factions.append(Faction(model, faction))
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