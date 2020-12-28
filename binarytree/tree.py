from binarytree.node import Node
from binarytree.functions import _generate_random_node_values, _get_leaves
import numpy


class Tree(object):

  def __init__(self, height: int):
    self.root = self.generate(height)
    self.init_rewards()
  
  def init_rewards(self) -> object:
    """Initialize the rewards for the leaf nodes

    :return: object
    """
    leaves = self.get_leaves()
    rewards = numpy.random.uniform(0, 100, len(leaves))

    for i_leaves in range(len(leaves)):
      leaves[i_leaves].reward = rewards[i_leaves]

    return self

  def generate(self, height: int):
    """Generate a random binary tree and return its root node.
  
    :param height: depth of the tree (default: 3, range: 0 - 9 inclusive).
    :type height: int
    :return: Root node of the binary tree.
    """
    values = _generate_random_node_values(height)
    nodes = [None if v is None else Node(v) for v in values]
  
    for index in range(1, len(nodes)):
      node = nodes[index]
  
      if node is not None:
        parent_index = (index - 1) // 2
        parent = nodes[parent_index]
  
        if parent is None:
          raise ValueError('Parent node missing at index {}'.format(parent_index))
  
        # set the parent
        node.parent = parent
        if index % 2:
          parent.left = node
        else:
          parent.right = node

    return nodes[0] if nodes else None

  def get_parent(self, child):
    """Search the binary tree and return the parent of given child.

    :param child: Child node.
    :return: Parent node, or None if missing.
    """
    if child is None:
      return None

    stack = [self.root]
    while stack:
      node = stack.pop()
      if node:
        if node.left is child or node.right is child:
          return node
        else:
          stack.append(node.left)
          stack.append(node.right)
  
    return None
  
  def get_leaves(self):
    return _get_leaves(self.root)

  def __str__(self):
    """Return the pretty-print string for the binary tree.

    :return: Pretty-print string.
    :rtype: str | unicode
    """
    return str(self.root)

