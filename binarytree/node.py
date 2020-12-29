from binarytree.functions import _build_tree_string
import numbers


class Node(object):

  def __init__(self, reward: int = None, left = None, right = None):
    if not isinstance(reward, numbers.Number):
      raise ValueError('node value must be a number')

    if left is not None and not isinstance(left, Node):
      raise TypeError('left child must be a Node instance')

    if right is not None and not isinstance(right, Node):
      raise TypeError('right child must be a Node instance')

    if reward is not None and (left is not None or right is not None):
      raise TypeError('non-leaf node cannot have a reward')

    self.reward = 0.0
    self.visits = 0

    self.parent = None
    self.left = left
    self.right = right

  def __str__(self):
    """Return the pretty-print string for the binary tree.

    :return: Pretty-print string.
    :rtype: str | unicode
    """
    lines = _build_tree_string(self, 0, False, '-')[0]

    return '\n' + '\n'.join((line.rstrip() for line in lines))

  def is_terminal(self) -> bool:
    """Returns true if the node is a terminal node

      :return: Whether the node is a terminal node
      :rtype: bool
      """
    return (self.left is None and self.right is None) or self.visits == 0
