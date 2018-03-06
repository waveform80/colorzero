# vim: set et sw=4 sts=4 fileencoding=utf-8:
#
# The colorzero color library
# Copyright (c) 2016-2018 Dave Jones <dave@waveform.org.uk>
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the copyright holder nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

from __future__ import (
    unicode_literals,
    print_function,
    division,
    absolute_import,
    )

import sys
import re
import inspect
from textwrap import dedent

from .color import Color


_CONVERTERS = {}
def color_conversion(returns):

    def make_color_constructors():
        # Figure out all conversions capable of reaching "rgb" and create
        # Color.from_xxx class constructors for each
        graph = find_conversions(target='rgb')
        for source, target in graph.items():
            try:
                constructor = getattr(Color, 'from_%s' % source)
                if constructor._target != target:
                    raise AttributeError('path changed')
            except AttributeError:
                function = _CONVERTERS[(source, target)]
                if target == 'rgb':
                    code = dedent("""\
                        def from_{source}(cls, {all_args}):
                            return super(Color, cls).__new__(cls, *{function.__name__}({all_args}))
                        """)
                else:
                    code = dedent("""\
                        def from_{source}(cls, {all_args}):
                            return cls.from_{target}({unpack}{function.__name__}({all_args}))
                        """)
                spec = inspect.getargspec(function)
                all_args = ', '.join(spec.args)
                unpack = '*' if issubclass(function.returns, tuple) else ''
                namespace = {
                    '__name__':        'colorzero',
                    function.__name__: function,
                    Color.__name__:    Color,
                    }
                code = code.format(**locals())
                exec(code, namespace)
                constructor = namespace['from_%s' % source]
                constructor._code = code
                constructor._target = target
                setattr(Color, 'from_%s' % source, classmethod(constructor))

    def make_color_properties():
        graph = find_conversions(source='rgb')
        for target, source in graph.items():
            try:
                attribute = getattr(Color, target)
                if attribute.fget._source != source:
                    raise AttributeError('path changed')
            except AttributeError:
                function = _CONVERTERS[(source, target)]
                if source == 'rgb':
                    code = dedent("""\
                        def {target}(self):
                            return {function.__name__}(*self)
                        """)
                else:
                    code = dedent("""\
                        def {target}(self):
                            return {function.__name__}({unpack}self.{source})
                        """)
                spec = inspect.getargspec(function)
                unpack = '*' if len(spec.args) > 1 else ''
                namespace = {
                    '__name__':        'colorzero',
                    function.__name__: function,
                    }
                code = code.format(**locals())
                exec(code, namespace)
                attribute = namespace[target]
                attribute._code = code
                attribute._source = source
                setattr(Color, target, property(attribute))

    def decorator(function):
        m = re.match(r'_(?P<source>\w+)_to_(?P<target>\w+)', function.__name__)
        if not m:
            raise ValueError('color conversion functions must be named _something_to_something')
        function.returns = returns
        source = m.group('source')
        target = m.group('target')
        _CONVERTERS[(source, target)] = function
        make_color_constructors()
        make_color_properties()
        return function

    return decorator


def find_conversions(source=None, target=None):
    """
    Constructs a mapping representing the shortest path from *source* to all
    reachable conversions, or from all reachable conversions to *target*.
    Specifying both *source* and *target* will raise :exc:`ValueError`.
    """
    # Dijkstra's algorithm is used to compute the shortest paths, using the
    # assumption that all conversions "cost" the same (1). This is overly
    # simple, and Dijkstra's isn't the fastest algorithm, but the search space
    # is small so this is "good enough" while keeping the code relatively
    # simple.
    nodes = {
        node
        for s, t in _CONVERTERS
        for node in (s, t)
        }
    distances = {node: 1000 for node in nodes} # inf~=1000 ;)
    if source is not None:
        if target is not None:
            raise ValueError('only one of source or target must be specified')
        distances[source] = 0
        neighbours = {
            node: {t for s, t in _CONVERTERS if s == node}
            for node in nodes
            }
    elif target is not None:
        distances[target] = 0
        neighbours = {
            node: {s for s, t in _CONVERTERS if t == node}
            for node in nodes
            }
    else:
        raise ValueError('either source or target must be specified')
    unvisited = nodes.copy()
    graph = {}
    while unvisited:
        node = min(unvisited, key=distances.get)
        unvisited.remove(node)
        for neighbour in neighbours[node]:
            d = distances[node] + 1 # all converters cost "1"
            if d < distances[neighbour]:
                distances[neighbour] = d
                graph[neighbour] = node
    return graph


def get_converter(source, target):
    # Construct a conversion function which traverses the path and handles
    # unpacking of arguments (just saves doing unpacking in every bloody
    # definition below)
    graph = find_conversions(source=source)
    if target not in graph:
        raise ValueError(
            'Unable to find a conversion from %s to %s' % (source, target))
    name = '%s_to_%s' % (source, target)
    prefix = suffix = ''
    while target in graph:
        source = graph[target]
        function = _CONVERTERS[(source, target)]
        if issubclass(function.returns, tuple):
            prefix += '*'
        spec = inspect.getargspec(function)
        prefix += function.__name__ + '('
        suffix += ')'
        target = source
    prototype = inspect.formatargspec(
        spec.args, None, None, (None,) * (len(spec.args) - 1))
    first_arg = spec.args[0]
    all_args = ', '.join(spec.args)
    other_args = ', '.join(spec.args[1:])
    conversion = prefix.lstrip('*') + all_args + suffix
    if len(spec.args) > 1:
        unpack = dedent("""\
            try:
                iter({first_arg})
            except TypeError:
                pass
            else:
                {all_args} = {first_arg}
            """)
    else:
        unpack = ""
    code = dedent("""\
        def {name}{prototype}:
            {unpack}
            return {conversion}
        """)
    unpack = indent(unpack, ' ' * 4).lstrip().format(**locals())
    code = code.format(**locals())
    namespace = {
        f.__name__: f
        for f in _CONVERTERS.values()
        }
    namespace['__name__'] = 'colorzero'
    exec(code, namespace)
    result = namespace[name]
    result._source = code
    return result

