from leuvenmapmatching.matcher.distance import DistanceMatcher
from leuvenmapmatching.map.inmem import InMemMap
from leuvenmapmatching import visualization as mmviz

path = [(1, 0), (7.5, 0.65), (10.1, 1.9)]
mapdb = InMemMap("mymap", graph={
    "A": ((1, 0.00), ["B"]),
    "B": ((3, 0.00), ["A", "C"]),
    "C": ((4, 0.70), ["B", "D"]),
    "D": ((5, 1.00), ["C", "E"]),
    "E": ((6, 1.00), ["D", "F"]),
    "F": ((7, 0.70), ["E", "G"]),
    "G": ((8, 0.00), ["F", "H"]),
    "H": ((10, 0.0), ["G", "I"]),
    "I": ((10, 2.0), ["H"])
}, use_latlon=False)
matcher = DistanceMatcher(mapdb, max_dist_init=0.2, obs_noise=1, obs_noise_ne=10,
                          non_emitting_states=True, only_edges=True)
states, _ = matcher.match(path)
nodes = matcher.path_pred_onlynodes

print("States\n------")
print(states)
print("Nodes\n------")
print(nodes)
print("")
matcher.print_lattice_stats()

mmviz.plot_map(mapdb, matcher=matcher,
              show_labels=True, show_matching=True
              filename="output.png")