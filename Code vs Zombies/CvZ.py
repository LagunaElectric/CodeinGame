import sys
import math
from dataclasses import dataclass, field

# Save humans, destroy zombies!


@dataclass
class Coordinate:
    x: int
    y: int

    def __repr__(self):
        return f"{x} {y}"


@dataclass
class Entity:
    pos: Coordinate

    def distance_to(self, coord: Coordinate) -> int:
        return round(math.sqrt(((coord.x - self.pos.x) ** 2) + ((self.pos.y - coord.y) ** 2)))

    def find_closest_entity(self, entities: list['Entity']) -> 'Entity':
        closest_entity: Entity = None
        for entity in entities:
            if closest_entity is None:
                closest_entity = entity
                continue
            closest_dist = self.distance_to(closest_entity.pos)
            current_dist = self.distance_to(entity.pos)
            if current_dist < closest_dist:
                closest_entity = entity
        return closest_entity


@dataclass
class Human(Entity):
    ID: int


@dataclass
class Player(Entity):
    def get_next_target(self) -> Coordinate:
        pass


@dataclass
class Zombie(Human):
    next_pos: Coordinate


# game loop
while True:
    x, y = [int(i) for i in input().split()]
    print(x, y, file=sys.stderr, flush=True)
    player: Player = Player(Coordinate(x, y))
    humans: list[Human] = []
    zombies: list[Zombie] = []

    human_count = int(input())
    for i in range(human_count):
        human_id, human_x, human_y = [int(j) for j in input().split()]
        human_coord = Coordinate(human_x, human_y)
        humans.append(Human(human_coord, human_id))

    zombie_count = int(input())
    for i in range(zombie_count):
        zombie_id, zombie_x, zombie_y, zombie_xnext, zombie_ynext = [int(j) for j in input().split()]
        zombie_coord = Coordinate(zombie_x, zombie_y)
        zombie_next_coord = Coordinate(zombie_xnext, zombie_ynext)
        zombies.append(Zombie(zombie_coord, zombie_id, zombie_next_coord))

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)
    print(player, file=sys.stderr, flush=True)
    print(player.find_closest_entity(zombies), file=sys.stderr, flush=True)
    print(humans, file=sys.stderr, flush=True)
    print(zombies, file=sys.stderr, flush=True)

    # Your destination coordinates
    print(f"{player.find_closest_entity(zombies).pos}")
