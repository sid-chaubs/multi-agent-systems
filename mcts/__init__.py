from binarytree.tree import Tree
from binarytree.node import Node
import math
import random


class MCTS:

  def __init__(self, tree_height: int = 3, exploration_weight: int = 50):
    self.tree = Tree(height = tree_height)
    self.plays = 0
    self.exploration_weight = exploration_weight

  def run(self, epochs: int) -> None:
    for i_epochs in range(epochs):
      # start from the root
      selected = self.tree.root
      self.plays += 1

      while not selected.is_terminal():
        selected = self.choose(selected)

      self.back_propagate(selected)

  def choose(self, node: Node) -> Node:
    children = [node.left, node.right]
    random.shuffle(children)

    return max(children, key = self.score)

  def back_propagate(self, node: Node):
    reward = node.reward
    node.visits += 1

    while node.parent is not None:
      node.parent.reward += reward
      node.parent.visits += 1
      node = node.parent

  def score(self, node: Node) -> float:
    if node.visits == 0:
      return math.inf

    mean = node.reward / node.visits

    score = mean + self.exploration_weight * math.sqrt(math.log(node.parent.visits) / node.visits)

    return score

