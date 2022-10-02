import numpy as np


def select_action(actions):
	"""
	:param actions: list of (probability, action)
	:return: action, sampled according to its probability
	"""
	probabilities = [action[0] for action in actions]
	indices = list(range(len(actions)))
	index = np.random.choice(indices, p=probabilities)
	return actions[index][1:]