import numpy as np
import matplotlib.pyplot as plt
from stats.plot_helpers import crop_zeroes

p_insert = 0.8
n = 100*1000
histogram_width = 100

# determine the distribution for (i) n~geom(p); n~uniform(0,n)

counts_1 = histogram_width*[0]

for _ in range(n):
	n_inserts = np.random.geometric(1 - p_insert)
	location = np.random.randint(0, n_inserts)
	n_inserts -= location
	counts_1[n_inserts] += 1


# determine the distribution for (i) n~geom(p)

counts_2 = histogram_width*[0]

for _ in range(n):
	n_inserts = np.random.geometric(1 - p_insert)
	counts_2[n_inserts] += 1


# cleanup data
counts_1, counts_2 = crop_zeroes(counts_1, counts_2)
indices = range(1, len(counts_1))
counts_1 = counts_1[1:]
counts_2 = counts_2[1:]

# plot both distributions

fig, ax = plt.subplots()
l1, = ax.plot(indices, counts_1)
l2, = ax.plot(indices, counts_2)
ax.legend((l1, l2), ('subtract', 'geometric'))

ax.grid()
plt.savefig('geometric_start.pdf')
plt.show()
