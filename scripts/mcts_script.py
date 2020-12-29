from mcts import MCTS

from binarytree.functions import _get_leaves

correct_guess = 0
incorrect_guess = 0
total_guesses = 1000

for i in range(total_guesses):
  mcts = MCTS(12, 250)
  mcts.run(100000)

  leaves = _get_leaves(mcts.tree.root)

  max_reward_node = max(leaves, key = lambda x: x.reward)
  max_visits_node = max(leaves, key = lambda x: x.visits)

  if max_visits_node.visits == max_reward_node.visits and max_reward_node.reward == max_visits_node.reward:
    print('Correct guess')
    correct_guess += 1
  else:
    print('Incorrect guess')
    print(max_reward_node)
    print(max_visits_node)
    incorrect_guess += 1

print(f'Accuracy = {correct_guess / total_guesses}')
