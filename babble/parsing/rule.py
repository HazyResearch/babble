from types import FunctionType

class Rule(object):
    """Represents a CFG rule with a semantic attachment."""

    def __init__(self, lhs, rhs, sem=None):
        self.lhs = lhs
        self.rhs = tuple(rhs.split()) if isinstance(rhs, str) else rhs
        self.sem = sem
        self.validate_rule()

    def __str__(self):
        """Returns a string representation of this Rule."""
        return 'Rule' + str((self.lhs, ' '.join(self.rhs), self.sem))

    def __eq__(self, other):
        return (self.lhs == other.lhs and self.rhs == other.rhs)

    def __ne__(self, other):
        return (self.lhs != other.lhs or self.rhs != other.rhs)

    def __hash__(self):
        return hash((self.lhs, self.rhs))

    def apply_semantics(self, sems):
        if isinstance(self.sem, FunctionType):
            return self.sem(sems)
        else:
            return self.sem

    def is_lexical(self):
        """
        Returns true iff the given Rule is a lexical rule, i.e., contains only
        words (terminals) on the RHS.
        """
        return all([not is_cat(rhsi) for rhsi in self.rhs])

    def is_unary(self):
        """
        Returns true iff the given Rule is a unary compositional rule, i.e.,
        contains only a single category (non-terminal) on the RHS.
        """
        return len(self.rhs) == 1 and is_cat(self.rhs[0])

    def is_binary(self):
        """
        Returns true iff the given Rule is a binary compositional rule, i.e.,
        contains exactly two categories (non-terminals) on the RHS.
        """
        return len(self.rhs) == 2 and is_cat(self.rhs[0]) and is_cat(self.rhs[1])

    def validate_rule(self):
        """Returns true iff the given Rule is well-formed."""
        assert is_cat(self.lhs), 'Not a category: %s' % self.lhs
        assert isinstance(self.rhs, tuple), 'Not a tuple: %s' % self.rhs
        for rhs_i in self.rhs:
            assert isinstance(rhs_i, str), 'Not a string: %s' % rhs_i

    def contains_optionals(self):
        """Returns true iff the given Rule contains any optional items on the RHS."""
        return any([is_optional(rhsi) for rhsi in self.rhs])


def is_cat(label):
    """
    Returns true iff the given label is a category (non-terminal), i.e., is
    marked with an initial '$'.
    """
    return label.startswith('$')

def is_optional(label):
    """
    Returns true iff the given RHS item is optional, i.e., is marked with an
    initial '?'.
    """
    return label.startswith('?') and len(label) > 1

def sems0(sems):
    return sems[0]

def sems1(sems):
    return sems[1]

def sems_in_order(sems):
    return tuple(sems)

def sems_reversed(sems):
    return tuple(reversed(sems))

def flip_dir(dir_):
    if dir_ == '.right':
        return '.left'
    elif dir_ == '.left':
        return '.right'
    else:
        raise ValueError

def star(f):
  return lambda args: f(*args)