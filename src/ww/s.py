
# TODO : make a s object for strings with split(regex|iterable), replace(regex|iterable)
# TODO : flags can be passed as strings. Ex: s.search('regex', flags='ig')
# TODO : make s.search(regex) return a wrapper with __bool__ evaluating to
# false if no match instead of None and allow default value for group(x)
# also allow match[1] to return group(1) and match['foo'] to return groupdict['foo']
# TODO .groups would be a g() object


# TODO : add encoding detection, fuzzy_decode() to make the best of shitty decoding,
# unidecode, slug, etc,


# f() for format, if no args are passed, it uses local. Also allow f >> ""

# t() or t >> for a jinja2 template (opeional dependancy ?)

# TODO: join() autocast to str, with a callable you can customize

# TODO: match.__repr__ should show match, groups, groupsdict in summary
# TODO : if g() is called on a callable, iter() calls the callable everytime

import re
import operator

from textwrap import dedent

from .g import g


def ensure_tuple(val):
    if not isinstance(val, str):
        try:
            return tuple(val)
        except TypeError:
            return (val,)
    return (val,)


class MetaS(type):
    """ Allow s >> 'text' as a shortcut to dedent strings """
    def __rshift__(self, other):
        return s(dedent(other))

REGEX_FLAGS = {
    'm': re.MULTILINE,
    'x': re.VERBOSE,
    'v': re.VERBOSE,
    's': re.DOTALL,
    '.': re.DOTALL,
    'd': re.DEBUG,
    'i': re.IGNORECASE,
    'a': re.ASCII,
    'u': re.UNICODE,
    'l': re.LOCALE,
}

class s(str, metaclass=MetaS):

    def _parse_flags(self, flags):
        bflags = 0
        if isinstance(flags, str):
            for flag in flags:
                bflags |= REGEX_FLAGS[flag]

            return bflags

        return flags

    def split(self, *separators, maxsplit=0, flags=0):
        return g(self._split(separators, maxsplit, self._parse_flags(flags)))

    def _split(self, separators, maxsplit=0, flags=0):
        try:
            sep = separators[0]
            for chunk in re.split(sep, self, maxsplit, flags):
                yield from s(chunk)._split(separators[1:], maxsplit=0, flags=0)
        except IndexError:
            yield self

    def replace(self, patterns, substitutions, maxreplace=0, flags=0):

        patterns = ensure_tuple(patterns)
        substitutions = ensure_tuple(substitutions)

        num_of_subs = len(substitutions)
        num_of_patterns = len(patterns)
        if num_of_subs == 1:
            substitutions *= num_of_patterns
        else:
            if len(patterns) != num_of_subs:
                raise ValueError("You must have exactly one substitution "
                                 "for each pattern or only one substitution")

        flags = self._parse_flags(flags)

        res = self
        for pattern, sub in zip(patterns, substitutions):
            res = re.sub(pattern, sub, res, count=maxreplace, flags=flags)

        return s(res)