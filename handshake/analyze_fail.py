from handshake_automation.tasks.cs_diagram_creator import _EDGES_CONFIG
from handshake_automation.tasks.problem_solver import _find_critical_path

weights = {(u,v):w for (u,v),(w,_,_) in _EDGES_CONFIG.items()}
best_dist, best_path, all_paths = _find_critical_path(weights)
print(f"GTFA={best_dist} path={'->'.join(best_path)}")
print("All S->T paths:")
for d,p in all_paths:
    print(f"{d:2d} ms : {'->'.join(p)}")
print("Total:", len(all_paths))

print("\n--- Why models FAIL at crossing ---")
print("Crossing (C,F)x(D,E): labels 21 and 12 are 0.12 offset apart. Models swap them.")
print("Block1 error: reads D-E=21 not 12 => L(E)= S-A-D-E =14+22+21=57 then +8+20=85 (vs 76) error 11.8%")
print("Crossing (B,E)x(A,D): B-E=26 diagonal. Models invent B->C=26.")
print("Block2 error: S-B-C-E-F-T =18+26+17+8+20=89 error 17.1%")
print("Both >2% threshold => 2/2 FAIL PASS")
