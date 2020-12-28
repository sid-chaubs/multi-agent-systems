from binarytree.tree import Tree
from binarytree.node import Node
import math
import random


class MCTS:

  def __init__(self, tree_height: int, exploration_weight: int):
    self.tree = Tree(height = tree_height)
    self.plays = 0
    self.exploration_weight = exploration_weight

  def run(self, epochs: int) -> None:
    for i_epochs in range(epochs):
      # start from the root
      selected = self.tree.root
      self.plays += 1

      while not selected.is_terminal():
        selected = self.select(selected)
      
      final = self.rollout(selected)

      self.backup(selected, final)
  
  def rollout(self, node: Node):
    while node.left and node.right:
      node = self.select(node)
    
    return node

  def select(self, node: Node) -> Node:
    children = [node.left, node.right]
    random.shuffle(children)

    return max(children, key = self.score)

  def backup(self, node: Node, final: Node):
    reward = final.reward
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

