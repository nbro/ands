#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author: Nelson Brochado

Creation: July, 2015

Last update: 13/02/16

Contains the class RBT for representing red-black trees.

## Red-black tree property

1. Every node is either red or black.

2. The root is black.

3. Every NIL or leaf node is black.

4. If a node is red, then both its children are black,
in other words, there cannot be two red nodes in a row.

5. For every node x, each path from x to its descendent leaves
has the same number of black nodes, i.e. bh(x).

## Lemma

The height `h(x)` of a red-black tree with `n = size(x)` internal nodes
is at most 2 * log<sub>2</sub>(n + 1), that is, h(x) <= 2 * log<sub>2</sub>(n + 1),
which is equivalent to h(x)/2 <= log<sub>2</sub>(n + 1), which is equivalent to
n >= 2<sup>h(x)/2</sup> - 1. If you don't understand exactly why this last statements
are equivalent, then do the reversed reasoning:

* n >= 2<sup>h(x)/2</sup> - 1

* n + 1 >= 2<sup>h(x)/2</sup>

Now we log both parts

* log<sub>2</sub>(n + 1) >= log<sub>2</sub>(2<sup>h(x)/2</sup>)

* log<sub>2</sub>(n + 1) >= h(x)/2 * log<sub>2</sub>(2)

* log<sub>2</sub>(n + 1) >= h(x)/2 * 1

* 2 * log<sub>2</sub>(n + 1) >= h(x)


### Proof

1. Prove that for all `x`, size(x) >= 2<sup>bh(x)</sup> - 1 by induction.

    1.1. **Base case**: `x` is a leaf, so `size(x) = 0` and `bh(x) = 0`.

    1.2. **Induction step**: consider y<sub>1</sub>, y<sub>2</sub>,
    and `x` such that y<sub>1</sub>.parent = y<sub>2</sub>.parent = x,
    and assume (induction) that size(y<sub>1</sub>) >= 2<sup>bh(y<sub>1</sub>)</sup> - 1
    and size(y<sub>2</sub>) >= 2<sup>bh(y<sub>2</sub>)</sup> - 1.
    Prove that size(x) >= 2<sup>bh(x)</sup> - 1.

    **Proof**:

    size(x) = size(y<sub>1</sub>) + size(y<sub>2</sub>) + 1 >= (2<sup>bh(y<sub>1</sub>)</sup> - 1)
    + (2<sup>bh(y<sub>2</sub>)</sup> - 1) + 1

    Since bh(x) = {

        bh(y), if color(y) = red
        
        bh(y) + 1, if color(y) = black
    }
    
    size(x) >= (2<sup>bh(x) - 1</sup> - 1) + (2<sup>bh(x) - 1</sup> - 1) + 1
    = (2<sup>bh(x)</sup> - 1).

    Since every red node has black children,
    in every path from `x` to a leaf node,
    at least half the nodes are black, thus bh(x) >= h(x)/2.
    So, n = size(x) >= 2<sup>h(x)/2</sup> - 1. Therefore
    h(x) <= 2 * log<sub>2</sub>(n + 1).

    A red-black tree works as a binary-search tree for search,
    insert, etc, so the complexity of those operations is T(n) = O(h),
    that is T(n) = O(log<sub>2</sub> n), which is also the worst case complexity.

## TODO
- Override needed methods inherited from BST.

## References

- [Red-black tree](https://en.wikipedia.org/wiki/Red%E2%80%93black_tree)

- Slides by prof. A. Carzaniga

- Chapter 13 of _Introduction to Algorithms_ (3rd ed.) by CLRS
"""

from ands.ds.BST import *
from ands.ds.RBTNode import RBTNode, RED, BLACK


__all__ = ["RBT"]


class RBT(BST):

    def __init__(self, root=None, name="RBT"):
        BST.__init__(self, root, name)

    def insert(self, u, value=None):
        """Inserts `u` into this `RBT`.

        This operation is similar to the `insert` operation of a classical `BST`,
        but, in this case, the red-black tree property must be maintained,
        so addional work is needed.    

        There are several cases of inserting into a RBT to handle:

        1. `u`  is the root node (first node).

        2. `u.parent` is `BLACK`.

        3. `u.parent` and the uncle of `u` are `RED`.

            The uncle of `u` will be the left child of `u.parent.parent`,
        if `u.parent` is the right child of `u.parent.parent`,
        otherwise (`u.parent` is the left child of `u.parent.parent`)
        the uncle will be the right child of `u.parent.parent`.

        4. u.parent is RED, but u.uncle is BLACK (or None). u.grandparent exists because u.parent is RED.

            4.1. `u` is added to the right of a left child of `u.parent.parent` (grandparent)

            4.2. or `u` is added to the left of a right child of `u.parent.parent`.

            4.3. `u` is added to the left of a left child of `u.parent.parent`.

            4.4. or `u` is added to the right of a right child of `u.parent.parent`.

        `_fix_insertion` handles these cases in the same order as just presented above.

        **Time Complexity:** O(log<sub>2</sub>(n))."""
        if u is None:
            raise ValueError("u cannot be None.")

        if not isinstance(u, RBTNode):
            u = RBTNode(u, value)

        if u.left or u.right or u.parent:
            raise ValueError("u cannot have left or right children, or parent.")

        c = self.root  # Current node
        p = None  # Current node's parent

        while c is not None:
            p = c
            if u.key < c.key:
                c = c.left
            else:  # u.key >= c.key
                c = c.right

        u.parent = p

        # The while loop was not executed even once.
        # Case 1: node is inserted as root.
        if p is None:
            self.root = u
        elif p.key > u.key:
            p.left = u
        else:  # p.key < u.key:
            p.right = u

        u.color = RED
        self.n += 1
        self._fix_insertion(u)

    def _fix_insertion(self, u: RBTNode):
        # u is the root and we color it BLACK.
        if u.parent is None:
            u.color = BLACK

        elif u.parent.color == BLACK:
            return
        
        elif u.parent.color == RED and (u.uncle is not None and u.uncle.color == RED):
            u.parent.color = BLACK
            u.uncle.color = BLACK
            u.grandparent.color = RED
            self._fix_insertion(u.grandparent)

        elif u.parent.color == RED and (u.uncle is None or u.uncle.color == BLACK):
            
            # u is added as a right child to a node that is the left child.
            if u.parent.is_left_child() and u.is_right_child():
                
                # left_rotation does not violate the property:
                # all paths from any given node to its leaf nodes
                # contain the same number of black nodes.
                self.left_rotate(u.parent)

                # With the previous left_rotate call,
                # u.parent has become the left child of u,
                # or, u bas become the parent of what before was u.parent
                # We can pass to case 5, where we have 2 red nodes in a row,
                # specifically, u.parent and u,
                # which are both left children of their parents.

                self._fix_insertion(u.left)

            # u is added as a left child to a node that is the right child.
            elif u.parent.is_right_child() and u.is_left_child():
                self.right_rotate(u.parent)
                self._fix_insertion(u.right)

            # u is added as a left child to a node that is the left child.
            elif u.parent.is_left_child() and u.is_left_child():
                # Note that grandparent is known to be black,
                # since its former child could not have been RED
                # without violating property 4.
                self.right_rotate(u.grandparent)
                u.parent.color = BLACK
                u.parent.right.color = RED

            # u is added as a right child to a node that is the right child.
            elif u.parent.is_right_child() and u.is_right_child():
                self.left_rotate(u.grandparent)
                u.parent.color = BLACK
                u.parent.left.color = RED

            else:
                assert False

    def delete(self, u):
        """Delete `u` from this `RBT` object.

        `u` can either be a `RBTNode` object or a key.
        
        If a key, then a search is performed first
        to find the corresponding `RBTNode` object.
        An exception is raised if a `RBTNode` object
        with a key=u is not found.
        
        If `u` is a `RBTNode` object, the only check
        that is performed is that if it hasn't a parent,
        then it must be the root. Similarly,
        a node that isn't the root must have a parent.
        If `u` has a parent, therefore it cannot be the root,
        but there's no way of knowing if this node
        really belongs to this `RBT` object,
        because no search is performed (for now).
        
        If it doesn't belong to this `RBT` object,
        then the behaviour of this method is undefined (for now).

        **Time Complexity:** O(log<sub>2</sub>(n))."""
        def delete_case1(v):
            #print("delete_case1")
            if v.parent is not None:
                delete_case2(v)

        def delete_case2(v):
            #print("delete_case2")
            if v.sibling.color == RED:

                assert v.parent.color == BLACK

                v.sibling.color = BLACK
                v.parent.color = RED

                if v.is_left_child():
                    self.left_rotate(v.parent)
                else:
                    self.right_rotate(v.parent)
                    
                assert v.sibling.color == BLACK

            delete_case3(v)

        def delete_case3(v):
            #print("delete_case3")            
            # not sure if the children of v.sibling can be None
            if (v.parent.color == BLACK and v.sibling.color == BLACK and
                ((v.sibling.left and v.sibling.left.color == BLACK) or not v.sibling.left) and
                ((v.sibling.right and v.sibling.right.color == BLACK) or not v.sibling.right)):

                v.sibling.color = RED
                delete_case1(v.parent)
            else:
                delete_case4(v)

        def delete_case4(v):
            #print("delete_case4")
            # not sure if the children of v.sibling can be None
            if (v.parent.color == RED and v.sibling.color == BLACK and
                ((v.sibling.left and v.sibling.left.color == BLACK) or not v.sibling.left) and
                ((v.sibling.right and v.sibling.right.color == BLACK) or not v.sibling.right)):

                v.sibling.color = RED
                v.parent.color = BLACK
            else:
                delete_case5(v)

        def delete_case5(v):
            #print("delete_case5")            
            assert v.sibling is not None

            if v.sibling.color == BLACK:

                if (v.is_left_child() and
                    (not v.sibling.right or v.sibling.right.color == BLACK) and
                    v.sibling.left.color == RED):

                    v.sibling.color = RED
                    v.sibling.left.color = BLACK

                    self.right_rotate(v.sibling)

                elif (v.is_right_child() and
                      (not v.sibling.left or v.sibling.left.color == BLACK) and
                      v.sibling.right.color == RED):

                    v.sibling.color = RED
                    v.sibling.right.color = BLACK

                    self.left_rotate(v.sibling)

            delete_case6(v)

        def delete_case6(v):
            #print("delete_case6")
            assert v.sibling is not None

            v.sibling.color, v.parent.color = v.parent.color, v.sibling.color
            
            if v.is_left_child():
                assert v.sibling.right
                v.sibling.right.color = BLACK
                self.left_rotate(v.parent)
            else:
                assert v.sibling.left
                v.sibling.left.color = BLACK
                self.right_rotate(v.parent)
                
        if u is None:
            raise ValueError("u cannot be None.")

        if not isinstance(u, RBTNode):
            u = self.search(u)
            if u is None:
                raise LookupError("No node was found with key=u.")

        if u.parent is None and u != self.root:
            raise ValueError("u is not a valid node.")

        # If u has two non-leaf children, then replace u with its successor.
        if u.left is not None and u.right is not None:
            s = self.successor(u)
            self._switch(u, s)
            u.color, s.color = s.color, u.color

        # At least one of the children must be None.
        assert u.left is None or u.right is None

        # Case 1
        # If `u` is a red node, we simply replace it with its child `c`,
        # which must be black by property 4, if any.
        # This can only occur when `u` has two leaf children,
        # because if the red node `u` had a black non-leaf child on one side,
        # but just a leaf child on the other side,
        # then the count of black nodes on both sides would be different,
        # thus the tree would violate property 5.
        # All paths through the deleted node
        # will simply pass through one fewer red node,
        # and both the deleted node's parent and child must be black,
        # so property 3 (all leaves are black) and property 4
        # (both children of every red node are black) still hold.
        if u.color == RED:
            assert u.left is None and u.right is None
            assert u != self.root

            if u.is_left_child():
                u.parent.left = None
            else:
                u.parent.right = None

        else:  # u.color == BLACK

            # One of the children of u is RED.
            # Simply removing a black node (u) could break properties 4,
            # i.e., both children of every red node are black,
            # because u.parent could be RED (e.g.), and 5,
            # i.e. all paths from any given node to its leaf nodes
            # contain the same number of black nodes),
            # but if we repaint `c` BLACK,
            # both of these properties are preserved.
            if u.left is not None and u.left.color == RED:
                if u != self.root:
                    if u.is_left_child():
                        u.parent.left = u.left
                    else:
                        u.parent.right = u.left

                u.left.parent = u.parent
                u.left.color = BLACK

                if u == self.root:
                    self.root = u.left

            elif u.right is not None and u.right.color == RED:
                if u != self.root:
                    if u.is_left_child():
                        u.parent.left = u.right
                    else:
                        u.parent.right = u.right

                u.right.parent = u.parent
                u.right.color = BLACK

                if u == self.root:
                    self.root = u.right

            # The complex case is when both `u` and `c` are BLACK.
            # This can only occur when deleting a black node
            # which has two leaf children, because if the black node `u`
            # had a black non-leaf child on one side
            # but just a leaf child on the other side,
            # then the count of black nodes on both sides would be different,
            # thus the tree would have been an invalid red–black tree
            # by violation of property 5.
            elif u.left is None and u.right is None:
                # 6 cases
                if u != self.root:
                    assert u.sibling is not None
                    
                    # Note that u.sibling cannot be None,
                    # because otherwise the substree containing it
                    # would have fewer black nodes
                    # than the subtree containing u.
                    # Specifically, the subree containing u
                    # would have a black height of 2,
                    # whereas the one containing the sibling
                    # would have a black height of 1.

                    delete_case1(u)

                    # We begin by replacing u with its child c.
                    # Note that both children of u are null-leaf children,
                    # as we observed
                    if u.is_left_child():
                        u.parent.left = None
                    else:
                        u.parent.right = None
                else:
                    self.root = None                
            else:
                assert False

        # Ensures that u has no reference to any node of this RBT.
        self.n -= 1
        u.parent = u.left = u.right = None
        return u

    def remove_max(self):
        """Removes and returns the element with the greatest value from `self`.

        **Time Complexity:** O(log<sub>2</sub>(n))."""
        if self.root:
            m = self.maximum()
            assert m
            return self.delete(m)

    def remove_min(self):
        """Removes and returns the element with the smallest value from `self`.

        **Time Complexity:** O(log<sub>2</sub>(n))."""        
        if self.root:
            m = self.minimum()
            assert m
            return self.delete(m)
