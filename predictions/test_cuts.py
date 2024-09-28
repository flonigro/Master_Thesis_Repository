import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.append('/Users/markcostantini/codes/MG5_aMC_v3_4_1')
sys.path.append('/Users/markcostantini/codes/MG5_aMC_v3_4_1/madgraph/various')
sys.path.append('/Users/markcostantini/Projects/PhD/smeft_jets/develop')


import lhe_parser

lhe = lhe_parser.EventFile(f"/Users/markcostantini/Projects/PhD/smeft_jets/develop/test_runs/run_27/unweighted_events.lhe.gz")
rap_star = []

for event in lhe:
    rap_tmp = []
    for particle in event:

        if particle.status == 1: # 1: outgoing, -1: incoming
            rap_tmp.append(lhe_parser.FourMomentum(particle).rapidity)

    rap_star.append(np.abs(rap_tmp[0]-rap_tmp[1])*0.5)

hist, bin_edges = np.histogram(rap_star, bins = np.linspace(-5,5,40))

print(np.max(rap_star), np.min(rap_star))
fig, ax = plt.subplots()

ax.stairs(hist, bin_edges)
plt.show()
