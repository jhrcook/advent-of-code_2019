#!/usr/bin/env python3

from pathlib import Path

orbit_map_input: list[str] = []
with open(Path("data", "06", "input.txt"), "r") as file:
    for line in file:
        orbit_map_input.append(line.strip())


OrbitGraph = dict[str, list[str]]
PlanetList = set[str]


def make_orbit_graph(orbit_map: list[str]) -> tuple[OrbitGraph, PlanetList]:
    orbit_graph: OrbitGraph = {}
    all_planets: PlanetList = set()
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
    planets: PlanetList, orbit_graph: OrbitGraph
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
