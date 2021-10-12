import sys
import math
from dataclasses import dataclass, field

# Save the Planet.
# Use less Fossil Fuel.


@dataclass
class Coordinate:
    x: int
    y: int

    def get_x_dist(self, coord: 'Coordinate') -> int:
        return coord.x - self.x

    def get_y_dist(self, coord):
        return coord.y - self.y

    def get_distance_to(self, coord: 'Coordinate') -> int:
        return round(math.sqrt(((self.get_x_dist(coord)) ** 2) + ((self.get_y_dist(coord)) ** 2)))


@dataclass
class Surface:
    left: Coordinate
    right: Coordinate
    height: int = field(init=False)
    center: Coordinate = field(init=False)

    def __post_init__(self):
        self.height = self.left.y
        center_x = round((self.left.x + self.right.x) / 2)
        self.center = Coordinate(center_x, self.height)


class LandMap:
    def __init__(self, points: list[Coordinate]):
        self.map: list[Coordinate] = points
        self.surface = self.get_flat_surface()

    def get_flat_surface(self) -> Surface:
        prev_point: Coordinate = None
        for point in self.map:
            if prev_point is None:
                prev_point = point
                continue
            if point.y == prev_point.y:
                return Surface(prev_point, point)
            prev_point = point

    def __repr__(self):
        out = ""
        for point in self.map:
            out += f"[{point.x}, {point.y}]"
            out += "" if point == self.map[len(self.map) - 1] else ", "
        return out


class Lander:
    def __init__(
        self,
        x: int,
        y: int,
        h_speed: int,
        v_speed: int,
        fuel: int,
        init_fuel: int,
        rotate: int,
        power: int,
        surface: Surface
    ):
        self.pos = Coordinate(x, y)
        self.h_speed = h_speed
        self.v_speed = v_speed
        self.fuel = fuel
        self.init_fuel = init_fuel
        self.rotate = rotate
        self.power = power
        self.target_surface = surface
        self.x_dist_to_center = self.get_x_dist(self.target_surface.center)
        self.y_dist_to_center = self.get_y_dist(self.target_surface.center)
        self.total_dist_to_center = self.get_distance_to(self.target_surface.center)

    def get_x_dist(self, coord: Coordinate) -> int:
        return self.pos.get_x_dist(coord)

    def get_y_dist(self, coord: Coordinate) -> int:
        return self.pos.get_y_dist(coord)

    def get_distance_to(self, coord: Coordinate) -> int:
        return self.pos.get_distance_to(coord)

    def __repr__(self):
        horizontal_direction_indicator = "-->" if self.h_speed > 0 else "<--" if self.h_speed < 0 else "---"
        vertical_direction_indicator = "^" if self.v_speed > 0 else "v" if self.v_speed < 0 else "-"
        fuel_percentage = round((self.fuel / self.init_fuel) * 100)
        fuel_guage_bars_full = round(fuel_percentage / 5)
        return f"""Lander:
    Position> X:{self.pos.x} | Y: {self.pos.y}
    Dist. to Surface Center>
        X: {self.x_dist_to_center}
        Y: {self.y_dist_to_center}
        Bee-Line: {self.total_dist_to_center}
    Horizontal Speed> {self.h_speed}m/s {horizontal_direction_indicator}
    Vertical Speed> {self.v_speed}m/s {vertical_direction_indicator}
    Fuel> {self.fuel}/{self.init_fuel} {fuel_percentage}% [{"#" * fuel_guage_bars_full}{"-" * (round(20 - fuel_guage_bars_full))}]
    Rotation> {self.rotate}deg
    Power> {self.power}"""


n = int(input())  # the number of points used to draw the surface of Mars.
points = []

for i in range(n):
    # land_x: X coordinate of a surface point. (0 to 6999)
    # land_y: Y coordinate of a surface point.
    # By linking all the points together in a sequential fashion, you form the surface of Mars.
    land_x, land_y = [int(j) for j in input().split()]
    points.append(Coordinate(land_x, land_y))

land_map = LandMap(points)
initial_turn = True
init_lander_fuel = None
# game loop
while True:
    # hs: the horizontal speed (in m/s), can be negative.
    # vs: the vertical speed (in m/s), can be negative.
    # f: the quantity of remaining fuel in liters.
    # r: the rotation angle in degrees (-90 to 90).
    # p: the thrust power (0 to 4).
    x, y, hs, vs, f, r, p = [int(i) for i in input().split()]
    if initial_turn:
        init_lander_fuel = f
        initial_turn = False
    lander = Lander(x, y, hs, vs, f, init_lander_fuel, r, p, land_map.surface)

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)
    print(lander, file=sys.stderr, flush=True)
    print(land_map, file=sys.stderr, flush=True)
    print(land_map.surface, file=sys.stderr, flush=True)
    print("""""", file=sys.stderr, flush=True)

    new_rotation: int = 0
    new_thrust: int = 3

    if lander.x_dist_to_center > 2000:
        new_rotation = -30
    elif lander.x_dist_to_center > 1500:
        new_rotation = -20
    elif lander.x_dist_to_center > 1000:
        new_rotation = -10
    elif lander.x_dist_to_center > 500:
        new_rotation = -5
        new_thrust = 4
    elif lander.x_dist_to_center > 100:
        new_rotation = -2
        new_thrust = 4
    elif lander.x_dist_to_center <= 100 and lander.x_dist_to_center >= -100:
        new_rotation = 0
        new_thrust = 4

    if abs(lander.v_speed) >= 40:
        new_rotation = 0
        new_thrust = 4

    if abs(lander.h_speed) >= 50:
        is_moving_right = lander.h_speed >= 50
        if is_moving_right:
            new_rotation = 45
            new_thrust = 2 if lander.rotate < 0 else 4
        else:
            new_rotation = -45
            new_thrust = 2 if lander.rotate > 0 else 4
    elif abs(lander.h_speed) >= 20 and lander.x_dist_to_center < 1000:
        is_moving_right = lander.h_speed >= 20
        if is_moving_right:
            new_rotation = 30
            new_thrust = 2 if lander.rotate < 0 else 4
        else:
            new_rotation = -30
            new_thrust = 2 if lander.rotate > 0 else 4

    if abs(lander.y_dist_to_center) < 200:
        new_rotation = 0
        new_thrust = 4

    # R P. R is the desired rotation angle. P is the desired thrust power.
    print(f"{new_rotation} {new_thrust}")
