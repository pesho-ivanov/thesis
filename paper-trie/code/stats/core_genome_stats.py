import numpy as np
import matplotlib.pyplot as plt
from stats.plot_helpers import crop_zeroes
from mutate_full import mutate, p_ins
from cut_full import cut
from bio import Genome, Segment


n = 100*1000
genome_length = 10


def generate_segment(L=4):
	g = Genome(10 * 'A')
	g_mut = mutate(g)
	seg = cut(g_mut, L)
	return seg


def count_n_start_insertions(s: Segment):
	n = 0
	for _, a, _ in s.mutations:
		if a == 'ins':
			n += 1
		else:
			break
	return n


def count_n_insertions(s: Segment):
	insertions = [a for _, a, _ in s.mutations if a == 'ins']
	return len(insertions)


def get_stats():
	start_stats = np.zeros(genome_length + 1)
	n_start_inserts_stats = np.zeros(5 * genome_length)
	n_inserts_sum = np.zeros(genome_length + 1)
	n_errors = 0

	for i in range(n):
		try:
			# generate
			s = generate_segment(4)
			# determine start index
			start = s.mutations[0][0].index
			start_stats[start] += 1
			# determine number of insertions at start
			n_start_inserts = count_n_start_insertions(s)
			n_start_inserts_stats[n_start_inserts] += 1
			# determine number total number of inserts per start
			n_insertions = count_n_insertions(s)
			n_inserts_sum[start] += n_insertions
		except ValueError:
			n_errors += 1

	position_zeroes = np.zeros_like(n_inserts_sum)
	avg_insertions = np.divide(n_inserts_sum, start_stats, out=position_zeroes, where=start_stats != 0)
	return start_stats, n_start_inserts_stats, avg_insertions, n_errors


start_stats_1, n_start_inserts_stats_1, avg_insertions_1, n_errors_1 = get_stats()
start_stats_2, n_start_inserts_stats_2, avg_insertions_2, n_errors_2 = get_stats()

# print n errors
print('# errors:', n_errors_1, '/', n_errors_2)

# plot starts
position_indices = range(len(start_stats_1))
_, ax = plt.subplots()
ax.plot(position_indices, start_stats_1, 'x')
ax.plot(position_indices, start_stats_1, '*')
ax.set_title(f'starts (p_ins={p_ins})')
ax.grid()
plt.savefig(f'starts_{p_ins}.pdf')
plt.show()

# plot n insertions at start
n_start_inserts_stats_1, n_start_inserts_stats_2 = crop_zeroes(n_start_inserts_stats_1, n_start_inserts_stats_2)
indices = range(len(n_start_inserts_stats_1))
_, ax = plt.subplots()
plt.yscale('log')
ax.plot(indices, n_start_inserts_stats_1, 'x')
ax.plot(indices, n_start_inserts_stats_2, 'x')
geometric = n*np.power(p_ins, indices)*(1-p_ins)
ax.plot(indices, geometric, '*')
ax.legend(['empirical 1', 'empirical 2', 'geometric'])
ax.set_title(f'# insertions at start (p_ins={p_ins})')
ax.grid()
plt.savefig(f'start_insertions_{p_ins}.pdf')
plt.show()


# plot n insertions per start
_, ax = plt.subplots()
ax.plot(position_indices, avg_insertions_1, 'x')
ax.plot(position_indices, avg_insertions_2, 'x')
ax.set_title(f'total # insertions per start (p_ins={p_ins})')
ax.grid()
plt.savefig(f'total_insertions_{p_ins}.pdf')
plt.show()
