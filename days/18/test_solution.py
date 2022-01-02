from solution import Node
from typing import Union

op_t = Union[list, int]


def test_send_left():
    node = Node.from_list([0, 0])
    node.right._send_left(1)
    assert node.as_list() == [1, 0]

    node = Node.from_list([[0, 0], 0])
    node.right._send_left(1)
    assert node.as_list() == [[0, 1], 0]

    node = Node.from_list([0, [0, 0]])
    node.right.left._send_left(1)
    assert node.as_list() == [1, [0, 0]]

    node = Node.from_list([[0, 0], [0, 0]])
    node.right.left._send_left(1)
    assert node.as_list() == [[0, 1], [0, 0]]

    node = Node.from_list([[0, [0, 0]], [0, 0]])
    node.right.left._send_left(1)
    assert node.as_list() == [[0, [0, 1]], [0, 0]]

    # Nothing at left
    node = Node.from_list([0, [0, 0]])
    node.left._send_left(1)
    assert node.as_list() == [0, [0, 0]]

    node = Node.from_list([[0, 0], [0, 0]])
    node.left.left._send_left(1)
    assert node.as_list() == [[0, 0], [0, 0]]


def test_send_right():
    node = Node.from_list([0, 0])
    node.left._send_right(1)
    assert node.as_list() == [0, 1]

    node = Node.from_list([0, [0, 0]])
    node.left._send_right(1)
    assert node.as_list() == [0, [1, 0]]

    node = Node.from_list([[0, 0], 0])
    node.left.right._send_right(1)
    assert node.as_list() == [[0, 0], 1]

    node = Node.from_list([[0, 0], [0, 0]])
    node.left.right._send_right(1)
    assert node.as_list() == [[0, 0], [1, 0]]

    node = Node.from_list([[0, 0], [[0, 0], 0]])
    node.left.right._send_right(1)
    assert node.as_list() == [[0, 0], [[1, 0], 0]]

    # Nothing at right
    node = Node.from_list([0, [0, 0]])
    node.right._send_right(1)
    assert node.as_list() == [0, [0, 0]]

    node = Node.from_list([[0, 0], [0, 0]])
    node.right.right._send_right(1)
    assert node.as_list() == [[0, 0], [0, 0]]


def test_needs():
    assert Node.from_list([[[[[4, 3], 4], 4], [7, [[8, 4], 9]]], [1, 1]]).needs_explode()
    assert Node.from_list([[[[0, 7], 4], [7, [[8, 4], 9]]], [1, 1]]).needs_explode()
    assert Node.from_list([[[[0, 7], 4], [15, [0, 13]]], [1, 1]]).needs_split()
    assert Node.from_list([[[[0, 7], 4], [[7, 8], [0, 13]]], [1, 1]]).needs_split()
    assert Node.from_list([[[[0, 7], 4], [[7, 8], [0, [6, 7]]]], [1, 1]]).needs_explode()


def test_magnitude():
    assert Node.from_list([[1, 2], [[3, 4], 5]]).calc_magnitude() == 143
    assert Node.from_list([[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]]).calc_magnitude() == 1384
    assert Node.from_list([[[[1, 1], [2, 2]], [3, 3]], [4, 4]]).calc_magnitude() == 445
    assert Node.from_list([[[[3, 0], [5, 3]], [4, 4]], [5, 5]]).calc_magnitude() == 791
    assert Node.from_list([[[[5, 0], [7, 4]], [5, 5]], [6, 6]]).calc_magnitude() == 1137
    assert Node.from_list([[[[8, 7], [7, 7]], [[8, 6], [7, 7]]], [[[0, 7], [6, 6]], [8, 7]]]).calc_magnitude() == 3488


def split(l: op_t) -> list:
    node, splitted = Node.from_list(l).split()
    return node.as_list()


def test_split():
    assert split(10) == [5, 5]
    assert split(11) == [5, 6]
    assert split(12) == [6, 6]
    assert split([12, 12]) == [[6, 6], 12]


def test_explode():
    assert Node.from_list([[[[[9, 8], 1], 2], 3], 4]).explode().as_list() == \
           [[[[0, 9], 2], 3], 4]
    assert Node.from_list([7, [6, [5, [4, [3, 2]]]]]).as_list() == \
           [7, [6, [5, [7, 0]]]]
    assert Node.from_list([[6, [5, [4, [3, 2]]]], 1]).as_list() == \
           [[6, [5, [7, 0]]], 3]
    assert Node.from_list([[3, [2, [1, [7, 3]]]], [6, [5, [4, [3, 2]]]]]).as_list() == \
           [[3, [2, [8, 0]]], [9, [5, [4, [3, 2]]]]]
    assert Node.from_list([[3, [2, [8, 0]]], [9, [5, [4, [3, 2]]]]]).as_list() == \
           [[3, [2, [8, 0]]], [9, [5, [7, 0]]]]


def test_add():
    assert Node.from_list([[[0, [4, 5]], [0, 0]], [[[4, 5], [2, 6]], [9, 5]]]).add(
           Node.from_list([7, [[[3, 7], [4, 3]], [[6, 3], [8, 8]]]])).as_list() == \
           [[[[4, 0], [5, 4]], [[7, 7], [6, 0]]], [[8, [7, 7]], [[7, 9], [5, 0]]]]
    assert Node.from_list([[[[4, 0], [5, 4]], [[7, 7], [6, 0]]], [[8, [7, 7]], [[7, 9], [5, 0]]]]).add(
            Node.from_list([[2, [[0, 8], [3, 4]]], [[[6, 7], 1], [7, [1, 6]]]])).as_list() == \
           [[[[6, 7], [6, 7]], [[7, 7], [0, 7]]], [[[8, 7], [7, 7]], [[8, 8], [8, 0]]]]
    assert Node.from_list([[[[6, 7], [6, 7]], [[7, 7], [0, 7]]], [[[8, 7], [7, 7]], [[8, 8], [8, 0]]]]).add(
            Node.from_list([[[[2, 4], 7], [6, [0, 5]]], [[[6, 8], [2, 8]], [[2, 1], [4, 5]]]])).as_list() == \
           [[[[7, 0], [7, 7]], [[7, 7], [7, 8]]], [[[7, 7], [8, 8]], [[7, 7], [8, 7]]]]
    assert Node.from_list([[[[7, 0], [7, 7]], [[7, 7], [7, 8]]], [[[7, 7], [8, 8]], [[7, 7], [8, 7]]]]).add(
            Node.from_list([7, [5, [[3, 8], [1, 4]]]])).as_list() == \
           [[[[7, 7], [7, 8]], [[9, 5], [8, 7]]], [[[6, 8], [0, 8]], [[9, 9], [9, 0]]]]
    assert Node.from_list([[[[7, 7], [7, 8]], [[9, 5], [8, 7]]], [[[6, 8], [0, 8]], [[9, 9], [9, 0]]]]).add(
            Node.from_list([[2, [2, 2]], [8, [8, 1]]])).as_list() == \
           [[[[6, 6], [6, 6]], [[6, 0], [6, 7]]], [[[7, 7], [8, 9]], [8, [8, 1]]]]
    assert Node.from_list([[[[6, 6], [6, 6]], [[6, 0], [6, 7]]], [[[7, 7], [8, 9]], [8, [8, 1]]]]).add(
            Node.from_list([2, 9])).as_list() == \
           [[[[6, 6], [7, 7]], [[0, 7], [7, 7]]], [[[5, 5], [5, 6]], 9]]
    assert Node.from_list([[[[6, 6], [7, 7]], [[0, 7], [7, 7]]], [[[5, 5], [5, 6]], 9]]).add(
            Node.from_list([1, [[[9, 3], 9], [[9, 0], [0, 7]]]])).as_list() == \
           [[[[7, 8], [6, 7]], [[6, 8], [0, 8]]], [[[7, 7], [5, 0]], [[5, 5], [5, 6]]]]
    assert Node.from_list([[[[7, 8], [6, 7]], [[6, 8], [0, 8]]], [[[7, 7], [5, 0]], [[5, 5], [5, 6]]]]).add(
            Node.from_list([[[5, [7, 4]], 7], 1])).as_list() == \
           [[[[7, 7], [7, 7]], [[8, 7], [8, 7]]], [[[7, 0], [7, 7]], 9]]
    assert Node.from_list([[[[7, 7], [7, 7]], [[8, 7], [8, 7]]], [[[7, 0], [7, 7]], 9]]).add(
            Node.from_list([[[[4, 2], 2], 6], [8, 7]])).as_list() == \
           [[[[8, 7], [7, 7]], [[8, 6], [7, 7]]], [[[0, 7], [6, 6]], [8, 7]]]


def test_data():
    test_data_ = [
        [[[0, [5, 8]], [[1, 7], [9, 6]]], [[4, [1, 2]], [[1, 4], 2]]],
        [[[5, [2, 8]], 4], [5, [[9, 9], 0]]],
        [6, [[[6, 2], [5, 6]], [[7, 6], [4, 7]]]],
        [[[6, [0, 7]], [0, 9]], [4, [9, [9, 0]]]],
        [[[7, [6, 4]], [3, [1, 3]]], [[[5, 5], 1], 9]],
        [[6, [[7, 3], [3, 2]]], [[[3, 8], [5, 7]], 4]],
        [[[[5, 4], [7, 7]], 8], [[8, 3], 8]],
        [[9, 3], [[9, 9], [6, [4, 9]]]],
        [[2, [[7, 7], 7]], [[5, 8], [[9, 3], [0, 2]]]],
        [[[[5, 2], 5], [8, [3, 7]]], [[5, [7, 5]], [4, 4]]],
    ]
    node = Node.from_list(test_data_[0])
    for op in test_data_[1:]:
        op = Node.from_list(op)
        node = node.add(op)
    assert node.as_list() == [[[[6, 6], [7, 6]], [[7, 7], [7, 0]]], [[[7, 7], [7, 7]], [[7, 8], [9, 9]]]]
    assert node.calc_magnitude() == 4140


def test_node():
    list_ = [[[0, [5, 8]], [[1, 7], [9, 6]]], [[4, [1, 2]], [[1, 4], 2]]]
    node = Node.from_list(list_)
    assert list_ == node.as_list()
