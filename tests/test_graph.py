"""
Tests for the graph module.
"""
from nose.tools import assert_equals, assert_true, assert_false, assert_raises


def test_add_node():
    """
    add a node to a DirectedGraph
    """
    from arbiter.graph import DirectedGraph

    graph = DirectedGraph()

    assert_equals(graph.nodes, frozenset())
    assert_equals(graph.roots, frozenset())
    assert_false('foo' in graph)

    graph.add_node('foo')

    assert_equals(graph.nodes, frozenset(('foo',)))
    assert_equals(graph.roots, frozenset(('foo',)))
    assert_true('foo' in graph)
    assert_equals(graph.get_children('foo'), frozenset())
    assert_equals(graph.get_parents('foo'), frozenset())
    assert_false(graph.is_ancestor('foo', 'foo'))

    graph.add_node('bar', ('foo', 'baz'))

    assert_equals(graph.nodes, frozenset(('foo', 'bar', 'baz')))
    assert_equals(graph.roots, frozenset(('foo',)))

    assert_true('foo' in graph)
    assert_true('bar' in graph)
    assert_true('baz' in graph)

    assert_equals(graph.get_children('foo'), frozenset(('bar',)))
    assert_equals(graph.get_children('bar'), frozenset())
    assert_equals(graph.get_children('baz'), frozenset(('bar',)))

    assert_equals(graph.get_parents('foo'), frozenset())
    assert_equals(graph.get_parents('bar'), frozenset(('foo', 'baz')))
    assert_equals(graph.get_parents('baz'), frozenset())

    assert_false(graph.is_ancestor('foo', 'foo'))
    assert_false(graph.is_ancestor('foo', 'bar'))
    assert_false(graph.is_ancestor('foo', 'baz'))

    assert_true(graph.is_ancestor('bar', 'foo'))
    assert_false(graph.is_ancestor('bar', 'bar'))
    assert_true(graph.is_ancestor('bar', 'baz'))

    assert_false(graph.is_ancestor('baz', 'foo'))
    assert_false(graph.is_ancestor('baz', 'bar'))
    assert_false(graph.is_ancestor('baz', 'baz'))

    graph.add_node('baz', ('bar',))

    assert_equals(graph.nodes, frozenset(('foo', 'bar', 'baz')))
    assert_equals(graph.roots, frozenset(('foo',)))

    assert_true('foo' in graph)
    assert_true('bar' in graph)
    assert_true('baz' in graph)

    assert_equals(graph.get_children('foo'), frozenset(('bar',)))
    assert_equals(graph.get_children('bar'), frozenset(('baz',)))
    assert_equals(graph.get_children('baz'), frozenset(('bar',)))

    assert_equals(graph.get_parents('foo'), frozenset())
    assert_equals(graph.get_parents('bar'), frozenset(('foo', 'baz')))
    assert_equals(graph.get_parents('baz'), frozenset(('bar',)))

    assert_false(graph.is_ancestor('foo', 'foo'))
    assert_false(graph.is_ancestor('foo', 'bar'))
    assert_false(graph.is_ancestor('foo', 'baz'))

    assert_true(graph.is_ancestor('bar', 'foo'))
    assert_true(graph.is_ancestor('bar', 'bar'))
    assert_true(graph.is_ancestor('bar', 'baz'))

    assert_true(graph.is_ancestor('baz', 'foo'))
    assert_true(graph.is_ancestor('baz', 'bar'))
    assert_true(graph.is_ancestor('baz', 'baz'))

    graph.add_node('ouroboros', ('ouroboros',))

    assert_equals(graph.nodes, frozenset(('foo', 'bar', 'baz', 'ouroboros')))
    assert_equals(graph.roots, frozenset(('foo',)))

    assert_true('ouroboros' in graph)
    assert_equals(graph.get_children('ouroboros'), frozenset(('ouroboros',)))
    assert_equals(graph.get_parents('ouroboros'), frozenset(('ouroboros',)))
    assert_true(graph.is_ancestor('ouroboros', 'ouroboros'))

    assert_raises(ValueError, graph.add_node, 'foo')


def test_add_node_acyclic():
    """
    add a node to an acyclic DirectedGraph
    """
    from arbiter.graph import DirectedGraph

    graph = DirectedGraph(acyclic=True)

    assert_equals(graph.nodes, frozenset())
    assert_equals(graph.roots, frozenset())
    assert_false('foo' in graph)

    graph.add_node('foo')

    assert_equals(graph.nodes, frozenset(('foo',)))
    assert_equals(graph.roots, frozenset(('foo',)))
    assert_true('foo' in graph)
    assert_equals(graph.get_children('foo'), frozenset())
    assert_equals(graph.get_parents('foo'), frozenset())
    assert_false(graph.is_ancestor('foo', 'foo'))

    graph.add_node('bar', ('foo', 'baz'))

    assert_equals(graph.nodes, frozenset(('foo', 'bar', 'baz')))
    assert_equals(graph.roots, frozenset(('foo',)))

    assert_true('foo' in graph)
    assert_true('bar' in graph)
    assert_true('baz' in graph)

    assert_equals(graph.get_children('foo'), frozenset(('bar',)))
    assert_equals(graph.get_children('bar'), frozenset())
    assert_equals(graph.get_children('baz'), frozenset(('bar',)))

    assert_equals(graph.get_parents('foo'), frozenset())
    assert_equals(graph.get_parents('bar'), frozenset(('foo', 'baz')))
    assert_equals(graph.get_parents('baz'), frozenset())

    assert_false(graph.is_ancestor('foo', 'foo'))
    assert_false(graph.is_ancestor('foo', 'bar'))
    assert_false(graph.is_ancestor('foo', 'baz'))

    assert_true(graph.is_ancestor('bar', 'foo'))
    assert_false(graph.is_ancestor('bar', 'bar'))
    assert_true(graph.is_ancestor('bar', 'baz'))

    assert_false(graph.is_ancestor('baz', 'foo'))
    assert_false(graph.is_ancestor('baz', 'bar'))
    assert_false(graph.is_ancestor('baz', 'baz'))

    assert_raises(ValueError, graph.add_node, 'baz', ('bar',))
    assert_raises(ValueError, graph.add_node, 'ouroboros', ('ouroboros',))
    assert_raises(ValueError, graph.add_node, 'foo')

    assert_equals(graph.nodes, frozenset(('foo', 'bar', 'baz')))
    assert_equals(graph.roots, frozenset(('foo',)))


def test_remove_node():
    """
    Remove a node from a DirectedGraph
    """
    from arbiter.graph import DirectedGraph

    graph = DirectedGraph()

    graph.add_node('node')
    graph.add_node('bar', ('foo',))
    graph.add_node('baz', ('bar',))
    graph.add_node('beta', ('alpha',))
    graph.add_node('bravo', ('alpha',))
    graph.add_node('tick', ('tock',))
    graph.add_node('tock', ('tick',))

    assert_equals(
        graph.nodes,
        frozenset(
            ('node', 'foo', 'bar', 'baz', 'alpha', 'beta',
             'bravo', 'tick', 'tock')
        )
    )
    assert_equals(graph.roots, frozenset(('node',)))

    # node with no children/parents
    assert_equals(graph.remove_node('node'), frozenset(('node',)))

    assert_equals(
        graph.nodes,
        frozenset(
            ('foo', 'bar', 'baz', 'alpha', 'beta', 'bravo', 'tick', 'tock')
        )
    )
    assert_equals(graph.roots, frozenset())

    # node with child, unique stub parent
    assert_equals(
        graph.remove_node('bar', transitive_parents=False),
        frozenset(('bar', 'foo'))
    )

    assert_equals(
        graph.nodes,
        frozenset(
            ('baz', 'alpha', 'beta', 'bravo', 'tick', 'tock')
        )
    )
    assert_equals(graph.roots, frozenset(('baz',)))

    # node with non-unique stub parent
    assert_equals(graph.remove_node('bravo'), frozenset(('bravo',)))

    assert_equals(
        graph.nodes,
        frozenset(
            ('baz', 'alpha', 'beta', 'tick', 'tock')
        )
    )
    assert_equals(graph.roots, frozenset(('baz',)))

    # stub
    assert_equals(graph.remove_node('alpha'), frozenset(('alpha',)))

    assert_equals(
        graph.nodes,
        frozenset(
            ('baz', 'beta', 'tick', 'tock')
        )
    )
    assert_equals(graph.roots, frozenset(('baz', 'beta')))

    # cycle
    assert_equals(
        graph.remove_node('tock', transitive_parents=False),
        frozenset(('tock',))
    )

    assert_equals(
        graph.nodes,
        frozenset(
            ('baz', 'beta', 'tick')
        )
    )
    assert_equals(graph.roots, frozenset(('baz', 'beta', 'tick')))

    assert_equals(graph.get_parents('tick'), frozenset())
    assert_equals(graph.get_children('tick'), frozenset())

    assert_raises(KeyError, graph.remove_node, 'fake')


def test_remove_node_transitively():
    """
    Remove a node (transitively making its parents its children's
    parents) from a DirectedGraph.
    """
    from arbiter.graph import DirectedGraph

    graph = DirectedGraph()

    graph.add_node('ouroboros', ('ouroboros',))
    graph.add_node('son of ouroboros', ('ouroboros',))
    graph.add_node('tick', ('tock',))
    graph.add_node('tock', ('tick',))
    graph.add_node('aye')
    graph.add_node('insect')
    graph.add_node('bee', ('aye', 'insect'))
    graph.add_node('cee', ('bee',))
    graph.add_node('child', ('stub',))
    graph.add_node('grandchild', ('child',))

    assert_equals(
        graph.nodes,
        frozenset(
            (
                'ouroboros', 'son of ouroboros', 'tick', 'tock', 'aye',
                'insect', 'bee', 'cee', 'child', 'stub', 'grandchild',
            )
        )
    )

    assert_equals(graph.roots, frozenset(('aye', 'insect')))

    # don't pass yourself to children
    assert_equals(graph.remove_node('ouroboros'), frozenset(('ouroboros',)))
    assert_equals(
        graph.nodes,
        frozenset(
            (
                'son of ouroboros', 'tick', 'tock', 'aye',
                'insect', 'bee', 'cee', 'child', 'stub', 'grandchild',
            )
        )
    )

    assert_equals(
        graph.roots,
        frozenset(('son of ouroboros', 'aye', 'insect'))
    )

    # pass a child to themselves
    assert_equals(graph.remove_node('tock'), frozenset(('tock',)))
    assert_equals(
        graph.nodes,
        frozenset(
            (
                'son of ouroboros', 'tick', 'aye',
                'insect', 'bee', 'cee', 'child', 'stub', 'grandchild',
            )
        )
    )

    assert_equals(
        graph.roots,
        frozenset(('son of ouroboros', 'aye', 'insect'))
    )

    assert_equals(graph.get_children('tick'), frozenset(('tick',)))
    assert_equals(graph.get_parents('tick'), frozenset(('tick',)))

    # two new parents
    assert_equals(graph.remove_node('bee'), frozenset(('bee',)))
    assert_equals(
        graph.nodes,
        frozenset(
            (
                'son of ouroboros', 'tick', 'aye',
                'insect', 'cee', 'child', 'stub', 'grandchild',
            )
        )
    )

    assert_equals(
        graph.roots,
        frozenset(('son of ouroboros', 'aye', 'insect'))
    )

    assert_equals(graph.get_children('aye'), frozenset(('cee',)))
    assert_equals(graph.get_children('insect'), frozenset(('cee',)))
    assert_equals(graph.get_parents('cee'), frozenset(('aye', 'insect')))

    # now with stubs
    assert_equals(graph.remove_node('child'), frozenset(('child',)))
    assert_equals(
        graph.nodes,
        frozenset(
            (
                'son of ouroboros', 'tick', 'aye',
                'insect', 'cee', 'stub', 'grandchild',
            )
        )
    )

    assert_equals(
        graph.roots,
        frozenset(('son of ouroboros', 'aye', 'insect'))
    )

    assert_equals(graph.get_children('stub'), frozenset(('grandchild',)))
    assert_equals(graph.get_parents('grandchild'), frozenset(('stub',)))


def test_remove_node_and_children():
    """
    Remove a node (and its children) from a DirectedGraph
    """
    from arbiter.graph import DirectedGraph

    graph = DirectedGraph()

    graph.add_node('node')
    graph.add_node('bar', ('foo',))
    graph.add_node('baz', ('bar',))
    graph.add_node('beta', ('alpha',))
    graph.add_node('bravo', ('alpha',))
    graph.add_node('tick', ('tock',))
    graph.add_node('tock', ('tick',))

    assert_equals(
        graph.nodes,
        frozenset(
            ('node', 'foo', 'bar', 'baz', 'alpha', 'beta',
             'bravo', 'tick', 'tock')
        )
    )
    assert_equals(graph.roots, frozenset(('node',)))

    # node with no children/parents
    assert_equals(graph.remove_node('node', True), frozenset(('node',)))

    assert_equals(
        graph.nodes,
        frozenset(
            ('foo', 'bar', 'baz', 'alpha', 'beta', 'bravo', 'tick', 'tock')
        )
    )
    assert_equals(graph.roots, frozenset())

    # node with child, unique stub parent
    assert_equals(
        graph.remove_node('bar', True),
        frozenset(('bar', 'foo', 'baz'))
    )

    assert_equals(
        graph.nodes,
        frozenset(
            ('alpha', 'beta', 'bravo', 'tick', 'tock')
        )
    )
    assert_equals(graph.roots, frozenset())

    # node with non-unique stub parent
    assert_equals(graph.remove_node('bravo'), frozenset(('bravo',)))

    assert_equals(
        graph.nodes,
        frozenset(
            ('alpha', 'beta', 'tick', 'tock')
        )
    )
    assert_equals(graph.roots, frozenset())

    # stub
    assert_equals(
        graph.remove_node('alpha', True), frozenset(('alpha', 'beta'))
    )

    assert_equals(
        graph.nodes,
        frozenset(
            ('tick', 'tock')
        )
    )

    # cycle
    assert_equals(graph.remove_node('tock', True), frozenset(('tock', 'tick')))

    assert_equals(graph.nodes, frozenset())
    assert_equals(graph.roots, frozenset())

    assert_raises(KeyError, graph.remove_node, 'fake', True)


def test_prune():
    """
    Prune a DirectedGraph
    """
    from arbiter.graph import DirectedGraph

    graph = DirectedGraph()

    graph.add_node('node')
    graph.add_node('bar', ('foo',))
    graph.add_node('baz', ('bar',))
    graph.add_node('beta', ('alpha',))
    graph.add_node('bravo', ('alpha',))
    graph.add_node('tick', ('tock',))
    graph.add_node('tock', ('tick',))

    assert_equals(
        graph.nodes,
        frozenset(
            ('node', 'foo', 'bar', 'baz', 'alpha', 'beta',
             'bravo', 'tick', 'tock')
        )
    )
    assert_equals(graph.roots, frozenset(('node',)))

    assert_equals(
        graph.prune(),
        frozenset(('bar', 'baz', 'beta', 'bravo'))
    )

    assert_equals(
        graph.nodes,
        frozenset(
            ('node', 'tick', 'tock')
        )
    )
    assert_equals(graph.roots, frozenset(('node',)))

    assert_equals(graph.prune(), frozenset())

    assert_equals(
        graph.nodes,
        frozenset(
            ('node', 'tick', 'tock')
        )
    )
    assert_equals(graph.roots, frozenset(('node',)))


def test_equality():
    """
    DirectedGraph equality
    """
    from arbiter.graph import DirectedGraph

    graph = DirectedGraph()

    assert_false(graph == 1)
    assert_true(graph != 0)

    other = DirectedGraph()

    assert_true(graph == other)
    assert_false(graph != other)

    graph.add_node('foo')

    assert_false(graph == other)
    assert_true(graph != other)

    graph.add_node('bar', ('foo',))

    other.add_node('bar', ('foo',))

    # still shouldn't match graph['foo'] is a stub
    assert_false(graph == other)
    assert_true(graph != other)

    other.add_node('foo')

    assert_true(graph == other)
    assert_false(graph != other)


def test_naming():
    """
    Names just need to be hashable.
    """
    from arbiter.graph import DirectedGraph

    graph = DirectedGraph()

    for name in (1, float('NaN'), 0, None, '', frozenset(), (), False, sum):
        graph.add_node('child1', frozenset((name,)))

        graph.add_node(name)

        assert_true(name in graph)
        assert_equals(graph.nodes, frozenset((name, 'child1')))
        assert_equals(graph.roots, frozenset((name,)))
        assert_equals(graph.get_children(name), frozenset(('child1',)))
        assert_equals(graph.get_parents(name), frozenset())
        assert_false(graph.is_ancestor(name, name))

        graph.add_node('child2', frozenset((name,)))
        assert_equals(
            graph.get_children(name),
            frozenset(('child1', 'child2'))
        )

        graph.remove_node(name)
        graph.remove_node('child1')
        graph.remove_node('child2')

        assert_equals(graph.nodes, frozenset())

    graph.add_node(None)
    graph.add_node('', parents=((),))
    graph.add_node((), parents=(frozenset(),))
    graph.add_node(frozenset())

    assert_equals(graph.nodes, frozenset((None, '', (), frozenset())))
    assert_equals(graph.roots, frozenset((None, frozenset())))

    graph.remove_node((), remove_children=True)

    assert_equals(graph.nodes, frozenset((None, frozenset())))
    assert_equals(graph.roots, frozenset((None, frozenset())))

    assert_raises(TypeError, graph.add_node, [])
    assert_raises(TypeError, graph.add_node, 'valid', parents=([],))
