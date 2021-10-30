#!/usr/bin/env python3

from pathlib import Path
from typing import Optional

orbit_map_input: list[str] = []
with open(Path("data", "06", "input.txt"), "r") as file:
    for line in file:
        orbit_map_input.append(line.strip())


OrbitGraph = dict[str, list[str]]
PlanetCollection = set[str]


def make_orbit_graph(orbit_map: list[str]) -> tuple[OrbitGraph, PlanetCollection]:
    orbit_graph: OrbitGraph = {}
    all_planets: PlanetCollection = set()
    for orbit in orbit_map:
        # Parse the orbit.
        orbit_split = orbit.split(")")
        a, b = orbit_split[0], orbit_split[1]
        # Add to collection of all planets.
        all_planets.add(a)
        all_planets.add(b)
        # Add to list of children.
        orbitors = orbit_graph.get(a, [])
        orbitors.append(b)
        orbit_graph[a] = orbitors
    return orbit_graph, all_planets


def count_direct_and_indirect_orbits(planet: str, orbit_graph: OrbitGraph) -> int:
    orbiting_planets = orbit_graph.get(planet)
    if orbiting_planets is None:
        return 0
    n_orbits = len(orbiting_planets)
    for orbiting_planet in orbiting_planets:
        n_orbits += count_direct_and_indirect_orbits(orbiting_planet, orbit_graph)
    return n_orbits


def count_all_direct_and_indirect_orbits(
    planets: PlanetCollection, orbit_graph: OrbitGraph
) -> int:
    return sum([count_direct_and_indirect_orbits(p, orbit_graph) for p in planets])


test_orbit_map_input = [
    "COM)B",
    "B)C",
    "C)D",
    "D)E",
    "E)F",
    "B)G",
    "G)H",
    "D)I",
    "E)J",
    "J)K",
    "K)L",
]

test_orbit_graph, test_planets = make_orbit_graph(test_orbit_map_input)
total_orbits = count_all_direct_and_indirect_orbits(test_planets, test_orbit_graph)
assert total_orbits == 42

orbit_graph, planets = make_orbit_graph(orbit_map_input)
total_orbits = count_all_direct_and_indirect_orbits(planets, orbit_graph)
print(f"(part 1) total number of orbits: {total_orbits}")

# ---- Part 2 ----

OrbitPath = list[str]
ReverseOrbitGraph = dict[str, str]


def reverse_shortest_path(
    orbit_graph: OrbitGraph, all_planets: PlanetCollection
) -> ReverseOrbitGraph:
    rev_graph: ReverseOrbitGraph = {}
    for planet in all_planets:
        for center_planet, orbiting_planets in orbit_graph.items():
            if planet in orbiting_planets:
                assert planet not in rev_graph
                rev_graph[planet] = center_planet
                break
    return rev_graph


def find_path_through_reverse_graph(
    from_planet: str,
    to_planet: str,
    rev_orbit_path: ReverseOrbitGraph,
    path: Optional[OrbitPath] = None,
) -> OrbitPath:
    if path is None:
        path = [from_planet]
    parent_planet = rev_orbit_path.get(from_planet)
    if parent_planet is None:
        return path
    elif parent_planet == to_planet:
        path.append(to_planet)
        return path
    else:
        path.append(parent_planet)
        find_path_through_reverse_graph(
            from_planet=parent_planet,
            to_planet=to_planet,
            rev_orbit_path=rev_orbit_path,
            path=path,
        )
    return path


def find_earliest_shared_node(path1: OrbitPath, path2: OrbitPath) -> tuple[str, int]:
    shortest_total_dist = len(path1) + len(path2)
    earliest_node = ""
    for shared_planet in set(path1.copy()).intersection(path2.copy()):
        idx1 = path1.index(shared_planet) - 1
        idx2 = path2.index(shared_planet) - 1
        total_dist = idx1 + idx2
        if total_dist < shortest_total_dist:
            shortest_total_dist = total_dist
            earliest_node = shared_planet
    return earliest_node, shortest_total_dist


def find_shortest_number_of_orbit_jumps(
    orbit_graph: OrbitGraph,
    planets: PlanetCollection,
    planet_a: str,
    planet_b: str,
    center_of_mass: str = "COM",
) -> tuple[str, int]:
    # Make a reverse orbit graph.
    rev_orbit_graph = reverse_shortest_path(orbit_graph, planets)
    # Get paths from each planet to COM.
    path1 = find_path_through_reverse_graph(planet_a, center_of_mass, rev_orbit_graph)
    path2 = find_path_through_reverse_graph(planet_b, center_of_mass, rev_orbit_graph)
    # Find the earliest shared node along the paths and count the number of jumps.
    return find_earliest_shared_node(path1, path2)


# Test input.
test_orbit_map_input = [
    "COM)B",
    "B)C",
    "C)D",
    "D)E",
    "E)F",
    "B)G",
    "G)H",
    "D)I",
    "E)J",
    "J)K",
    "K)L",
    "K)YOU",
    "I)SAN",
]
test_orbit_graph, test_planets = make_orbit_graph(test_orbit_map_input)
test_node, test_jumps = find_shortest_number_of_orbit_jumps(
    test_orbit_graph, test_planets, planet_a="YOU", planet_b="SAN"
)
assert test_jumps == 4 and test_node == "D"

# Puzzle input.
test_node, test_jumps = find_shortest_number_of_orbit_jumps(
    orbit_graph, planets, planet_a="YOU", planet_b="SAN"
)
print(f"(part 2) total number of orbital jumps between YOU and SAN: {test_jumps}")
