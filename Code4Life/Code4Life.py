import sys
import math
from pprint import pformat
from dataclasses import dataclass, field


def pdebug(*args):
    for arg in args:
        print(arg, file=sys.stderr, flush=True, sep=" | ")


def handle_start(**kwawrgs):
    pdebug("start")
    print("GOTO SAMPLES")


def handle_samples(**kwawrgs):
    pdebug("samples")
    player = kwawrgs["player"]
    if player.sample_carried is None:
        print("CONNECT 2")
    else:
        print("GOTO DIAGNOSIS")


def handle_diagnosis(**kwawrgs):
    pdebug("diag")
    player = kwawrgs["player"]
    cloud_samples = kwawrgs["cloud_samples"]
    if player.proc_samp_last_turn:
        player.proc_samp_last_turn = False
        print("GOTO MOLECULES")
    elif player.sample_carried is None:
        good_samples = [x.sample_id for x in cloud_samples if x.health > 1]
        [pdebug(x) for x in good_samples]
        target_sample = good_samples[0] if len(good_samples) > 0 else cloud_samples[-1].sample_id
        print(f"CONNECT {target_sample}")
    elif player.sample_carried is not None:
        player.proc_samp_last_turn = True
        print(f"CONNECT {player.sample_carried.sample_id}")
    else:
        print("GOTO MOLECULES")


def handle_molecules(**kwawrgs):
    pdebug("mol")
    player = kwawrgs["player"]
    if not player.has_required_ingredients():
        ing: str = player.needed_ingredients()[0]
        pdebug("ing: " + ing)
        print(f"CONNECT {ing}")
    else:
        print(f"GOTO LABORATORY")


def handle_lab(**kwawrgs):
    pdebug("lab")
    player = kwawrgs["player"]
    if player.has_required_ingredients():
        print(f"CONNECT {player.sample_carried.sample_id}")
        player.sample_carried = None
    else:
        print("GOTO SAMPLES")


@dataclass
class Sample:
    sample_id: int
    carried_by: int
    rank: int
    gain: str
    health: int
    cost_a: int
    cost_b: int
    cost_c: int
    cost_d: int
    cost_e: int
    total_cost: int = field(init=False)
    molecule_cost: dict[str, int] = field(default_factory=dict)

    def __post_init__(self):
        self.total_cost = sum([self.cost_a, self.cost_b, self.cost_c, self.cost_d, self.cost_e])
        self.molecule_cost["A"] = self.cost_a
        self.molecule_cost["B"] = self.cost_b
        self.molecule_cost["C"] = self.cost_c
        self.molecule_cost["D"] = self.cost_d
        self.molecule_cost["E"] = self.cost_e


@dataclass
class Player:
    target: str = ""
    eta: int = 0
    score: int = 0
    storage_a: int = 0
    storage_b: int = 0
    storage_c: int = 0
    storage_d: int = 0
    storage_e: int = 0
    expertise_a: int = 0
    expertise_b: int = 0
    expertise_c: int = 0
    expertise_d: int = 0
    expertise_e: int = 0
    molecule_storage: dict[str, int] = field(default_factory=dict)
    total_molecules: int = 0
    sample_carried: Sample = None
    is_collecting: bool = False
    proc_samp_last_turn: bool = False

    def __post_init__(self):
        self.init()

    def init(self):
        molecules = [self.storage_a, self.storage_b, self.storage_c, self.storage_d, self.storage_e]
        for (reg, store) in zip(list("ABCDE"), molecules):
            self.molecule_storage[reg] = store
        self.total_molecules = sum(molecules)

    def has_required_ingredients(self) -> bool:
        if self.sample_carried is None:
            return False
        has_ingredients_bools = []
        sample = self.sample_carried
        ingredients = [sample.cost_a, sample.cost_b, sample.cost_c, sample.cost_d, sample.cost_e]
        for (a, b) in zip(list("ABCDE"), ingredients):
            has_ingredients_bools.append(self.molecule_storage[a] >= b)
        return False if False in has_ingredients_bools else True

    def needed_ingredients(self) -> list[str]:
        if self.sample_carried is None:
            return []
        missing_molecules: list[str] = []
        for reg in list("ABCDE"):
            num_missing = self.sample_carried.molecule_cost[reg] - self.molecule_storage[reg]
            for i in range(num_missing):
                missing_molecules.append(reg)
        return missing_molecules


# Bring data on patient samples from the diagnosis machine to the laboratory with enough molecules to produce medicine!
project_count = int(input())
for i in range(project_count):
    inputs = input().split()
    a, b, c, d, e = [int(j) for j in inputs]

player: Player = Player()
handle_station: dict = {
    "START_POS": handle_start,
    "SAMPLES": handle_samples,
    "DIAGNOSIS": handle_diagnosis,
    "MOLECULES": handle_molecules,
    "LABORATORY": handle_lab
}
# game loop
while True:
    cloud_samples: list[Sample] = []

    inputs = input().split()
    player.target = inputs[0]
    player.eta = int(inputs[1])
    player.score = int(inputs[2])
    player.storage_a = int(inputs[3])
    player.storage_b = int(inputs[4])
    player.storage_c = int(inputs[5])
    player.storage_d = int(inputs[6])
    player.storage_e = int(inputs[7])
    player.expertise_a = int(inputs[8])
    player.expertise_b = int(inputs[9])
    player.expertise_c = int(inputs[10])
    player.expertise_d = int(inputs[11])
    player.expertise_e = int(inputs[12])
    player.init()

    inputs = input().split()
    opponent: Player = Player(
        inputs[0],
        int(inputs[1]),
        int(inputs[2]),
        int(inputs[3]),
        int(inputs[4]),
        int(inputs[5]),
        int(inputs[6]),
        int(inputs[7]),
        int(inputs[8]),
        int(inputs[9]),
        int(inputs[10]),
        int(inputs[11]),
        int(inputs[12])
    )
    opponent.init()

    available_a, available_b, available_c, available_d, available_e = [int(i) for i in input().split()]

    sample_count = int(input())
    for i in range(sample_count):
        inputs = input().split()
        sample = Sample(
            int(inputs[0]),
            int(inputs[1]),
            int(inputs[2]),
            inputs[3],
            int(inputs[4]),
            int(inputs[5]),
            int(inputs[6]),
            int(inputs[7]),
            int(inputs[8]),
            int(inputs[9])
        )
        if sample.carried_by == 0:
            pdebug("scbp")
            player.sample_carried = sample
        elif sample.carried_by == 1:
            pdebug("scbo")
            opponent.sample_carried = sample
        else:
            pdebug("scbn")
            cloud_samples.append(sample)

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)
    pdebug(player.sample_carried)
    # pdebug(opponent)
    [pdebug(x) for x in cloud_samples]

    p_dict = player.__dict__
    p_dict["has_ing"] = player.has_required_ingredients()
    p_dict["needed_ing"] = player.needed_ingredients()
    print(pformat(p_dict), file=sys.stderr, flush=True)
    handle_station[player.target](cloud_samples=cloud_samples, player=player)
