import random


def _generate_random_node_values(depth):
  """Return random node values for building binary trees.

  :param depth: depth of the binary tree.
  :type depth: int
  :return: Randomly generated node values.
  :rtype: [int]
  """
  max_node_count = 2 ** (depth + 1) - 1
  node_values = list(range(max_node_count))
  random.shuffle(node_values)

  return node_values


def _build_tree_string(root, curr_index, index = False, delimiter = '-'):
  """Recursively walk down the binary tree and build a pretty-print string.

  In each recursive call, a "box" of characters visually representing the
  current (sub)tree is constructed line by line. Each line is padded with
  whitespaces to ensure all lines in the box have the same length. Then the
  box, its width, and start-end positions of its root node value repr string
  (required for drawing branches) are sent up to the parent call. The parent
  call then combines its left and right sub-boxes to build a larger box etc.

  :param root: Root node of the binary tree.
  :type root: binarytree.Node
  :param curr_index: Level-order_ index of the current node (root node is 0).
  :type curr_index: int
  :param index: If set to True, include the level-order_ node indexes using
      the following format: ``{index}{delimiter}{value}`` (default: False).
  :type index: bool
  :param delimiter: Delimiter character between the node index and the node
      value (default: '-').
  :type delimiter:
  :return: Box of characters visually representing the current subtree, width
      of the box, and start-end positions of the repr string of the new root
      node value.
  :rtype: ([str], int, int, int)
  """
  if root is None:
    return [], 0, 0, 0

  line1 = []
  line2 = []
  if index:
    node_repr = '{}{}{}'.format(curr_index, delimiter, f'{root.visits}')
  else:
    node_repr = f'visits={root.visits}, reward={root.reward}'

  new_root_width = gap_size = len(node_repr)

  # Get the left and right sub-boxes, their widths, and root repr positions
  l_box, l_box_width, l_root_start, l_root_end = _build_tree_string(root.left, 2 * curr_index + 1, index, delimiter)
  r_box, r_box_width, r_root_start, r_root_end = _build_tree_string(root.right, 2 * curr_index + 2, index, delimiter)

  # Draw the branch connecting the current root node to the left sub-box
  # Pad the line with whitespaces where necessary
  if l_box_width > 0:
    l_root = (l_root_start + l_root_end) // 2 + 1
    line1.append(' ' * (l_root + 1))
    line1.append('_' * (l_box_width - l_root))
    line2.append(' ' * l_root + '/')
    line2.append(' ' * (l_box_width - l_root))
    new_root_start = l_box_width + 1
    gap_size += 1
  else:
    new_root_start = 0

  # Draw the representation of the current root node
  line1.append(node_repr)
  line2.append(' ' * new_root_width)

  # Draw the branch connecting the current root node to the right sub-box
  # Pad the line with whitespaces where necessary
  if r_box_width > 0:
    r_root = (r_root_start + r_root_end) // 2
    line1.append('_' * r_root)
    line1.append(' ' * (r_box_width - r_root + 1))
    line2.append(' ' * r_root + '\\')
    line2.append(' ' * (r_box_width - r_root))
    gap_size += 1
  new_root_end = new_root_start + new_root_width - 1
  
  # Combine the left and right sub-boxes with the branches drawn above
  gap = ' ' * gap_size
  new_box = [''.join(line1), ''.join(line2)]
  for i in range(max(len(l_box), len(r_box))):
    l_line = l_box[i] if i < len(l_box) else ' ' * l_box_width
    r_line = r_box[i] if i < len(r_box) else ' ' * r_box_width
    new_box.append(l_line + gap + r_line)

  # Return the new box, its width and its root repr positions
  return new_box, len(new_box[0]), new_root_start, new_root_end


def _get_tree_properties(root):
  """Inspect the binary tree and return its properties (e.g. depth).

  :param root: Root node of the binary tree.
  :type root: binarytree.Node
  :return: Binary tree properties.
  :rtype: dict
  """
  is_descending = True
  is_ascending = True
  min_node_value = root.value
  max_node_value = root.value
  size = 0
  leaf_count = 0
  min_leaf_depth = 0
  max_leaf_depth = -1
  is_strict = True
  is_complete = True
  current_level = [root]
  non_full_node_seen = False
  
  while len(current_level) > 0:
    max_leaf_depth += 1
    next_level = []
    
    for node in current_level:
      size += 1
      val = node.value
      min_node_value = min(val, min_node_value)
      max_node_value = max(val, max_node_value)
      
      # Node is a leaf.
      if node.left is None and node.right is None:
        if min_leaf_depth == 0:
          min_leaf_depth = max_leaf_depth
        leaf_count += 1
      
      if node.left is not None:
        if node.left.value > val:
          is_descending = False
        elif node.left.value < val:
          is_ascending = False
        next_level.append(node.left)
        is_complete = not non_full_node_seen
      else:
        non_full_node_seen = True
      
      if node.right is not None:
        if node.right.value > val:
          is_descending = False
        elif node.right.value < val:
          is_ascending = False
        next_level.append(node.right)
        is_complete = not non_full_node_seen
      else:
        non_full_node_seen = True
      
      # If we see a node with only one child, it is not strict
      is_strict &= (node.left is None) == (node.right is None)

    current_level = next_level

  return {
    'depth': max_leaf_depth,
    'size': size,
    'is_max_heap': is_complete and is_descending,
    'is_min_heap': is_complete and is_ascending,
    'is_perfect': leaf_count == 2 ** max_leaf_depth,
    'is_strict': is_strict,
    'is_complete': is_complete,
    'leaf_count': leaf_count,
    'min_node_value': min_node_value,
    'max_node_value': max_node_value,
    'min_leaf_depth': min_leaf_depth,
    'max_leaf_depth': max_leaf_depth,
  }


def _get_leaves(root):
  current_level = [root]
  leaves = []

  while len(current_level) > 0:
    next_level = []

    for node in current_level:
      if node.left is None and node.right is None:
        leaves.append(node)
        continue

      if node.left is not None:
        next_level.append(node.left)
      if node.right is not None:
        next_level.append(node.right)

    current_level = next_level

  return leaves
