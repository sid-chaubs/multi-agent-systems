from mcts import MCTS

from binarytree.functions import _get_leaves

for i in range(100):
  mcts = MCTS()
  mcts.run(10000)

  leaves = _get_leaves(mcts.tree.root)
  max_reward = max(leaves, key = lambda x: x.reward)
  print(f'\nMax Reward: {max_reward}')

  max_visits = max(leaves, key = lambda x: x.visits)
  print(f'\nMax Visits: {max_visits}')

  print('__________________________________________________\n')

