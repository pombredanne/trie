#
# Copyright (c) David Hain and Spideroak, Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import trie


def test_root_no_value():
    t = trie.Trie()
    try:
        t[()]
    except KeyError:
        pass


def test_root_with_value():
    t = trie.Trie('hello')
    assert t[()] == 'hello'


def test_setitem():
    t = trie.Trie()
    t['foo'] = 'bar'
    assert t['foo'] == 'bar'


def test_needmore():
    t = trie.Trie()
    t['foo'] = 'bar'
    try:
        t['fo']
    except trie.NeedMore:
        pass


def test_keyerror():
    t = trie.Trie()
    try:
        t['foo']
    except  KeyError:
        pass


def test_delitem():
    t = trie.Trie()
    t['foo'] = 'bar'
    del t['foo']

    try:
        t['foo']
    except KeyError:
        pass
    assert not t.root.nodes


def test_delitem_keyerror():
    t = trie.Trie()
    try:
        del t['foo']
    except KeyError:
        pass
    t['foobar'] = 'bar'
    try:
        del t['foo']
    except KeyError:
        pass


def test_delitem_node():
    t = trie.Trie()
    t['foobar'] = 'bar'
    t['foobarbaz'] = 'baz'
    del t['foobarbaz']
    assert t['foobar'] == 'bar'


def test_children():
    t = trie.Trie()
    t['foo'] = 'bar'
    t['fox'] = 'baz'
    assert not t.children('f')
    assert t.children('fo') == {'o': 'bar', 'x': 'baz'}


def test_iter():
    t = trie.Trie()
    t['f'] = 'fval'
    t['foo'] = 'fooval'
    t['bar'] = 'barval'
    t['baz'] = 'bazval'
    itered = list(t)
    assert itered == map(list, 'bar baz f foo'.split())


def test_iteritems():
    t = trie.Trie()
    t['f'] = 'fval'
    t['foo'] = 'fooval'
    t['bar'] = 'barval'
    t['baz'] = 'bazval'
    itered = list(t.iteritems())
    assert itered == zip(map(list, 'bar baz f foo'.split()), 'barval bazval fval fooval'.split())


def test_itervalues():
    t = trie.Trie()
    t['f'] = 'fval'
    t['foo'] = 'fooval'
    t['bar'] = 'barval'
    t['baz'] = 'bazval'
    itered = list(t.itervalues())
    assert itered == 'barval bazval fval fooval'.split()


def test_serialise():
    try:
        import cPickle as pickle
    except ImportError:
        import pickle
    t = trie.Trie()
    t['f'] = 'fval'
    t['foo'] = 'fooval'
    t['bar'] = 'barval'
    t['baz'] = 'bazval'
    t2 = pickle.loads(pickle.dumps(t))
    itered = list(t2.itervalues())
    assert itered == 'barval bazval fval fooval'.split()

    t = trie.Trie()
    t['obj'] = object()
    t2 = pickle.loads(pickle.dumps(t))
    assert type(t2['obj']) == object, t2['obj']
