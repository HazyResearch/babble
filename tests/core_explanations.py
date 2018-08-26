from babble import Explanation

def get_aliases():
    return {
        'colors':['red','green','blue'],
        'bluebird':['blue','bird','fly'],
        'greek':['alpha','beta','gamma'],
        'letters':['a','B','C'],
        'smalls':['a','b','c','d'],
        'luckies': [7, 8, 9],
        'unluckies': [0, 13, 66],
    }

# Test candidate (hash: 668761641257950361):
# "City land records show that GM President [Daniel Ammann] and his wife,
# [Pernilla Ammann], bought the 15-bedroom mansion on Balmoral Drive in
# the upscale historic neighborhood on July 31."

logic = [
    # Base
    Explanation(
        condition="True",
        label=1,
        candidate=('foo', 'bar'),
        semantics=('.root', ('.label', ('.int', 1), ('.bool', True)))),
    # And
    Explanation(
        condition="True and True",
        label=1,
        candidate=('foo', 'bar'),
        semantics=('.root', ('.label', ('.int', 1), ('.and', ('.bool', True), ('.bool', True))))),
    # Or
    Explanation(
        condition="False or True",
        label=1,
        candidate=('foo', 'bar'),
        semantics=('.root', ('.label', ('.int', 1), ('.or', ('.bool', False), ('.bool', True))))),
    # Not boolean
    Explanation(
        condition="not False",
        label=1,
        candidate=('foo', 'bar'),
        semantics=('.root', ('.label', ('.int', 1), ('.not', ('.bool', False))))),
    # Not function
    Explanation(
        condition="2 is not less than 1",
        label=1,
        candidate=('foo', 'bar'),
        semantics=('.root', ('.label', ('.int', 1), ('.not', ('.call', ('.lt', ('.int', 1)), ('.int', 2)))))),
    # All
    Explanation(
        condition='all of (2, 3, 4) are greater than 1',
        label=1,
        candidate=('foo', 'bar'),
        semantics=('.root', ('.label', ('.int', 1), ('.all', ('.map', ('.gt', ('.int', 1)), ('.list', ('.int', 2), ('.int', 3), ('.int', 4))))))),
    # Any
    Explanation(
        condition='any of (3, 1, 4) are less than 2',
        label=1,
        candidate=('foo', 'bar'),
        semantics=('.root', ('.label', ('.int', 1), ('.any', ('.map', ('.lt', ('.int', 2)), ('.list', ('.int', 3), ('.int', 1), ('.int', 4))))))),
    # None
    Explanation(
        condition='none of (1, 2, 3) are greater than 4',
        label=1,
        candidate=('foo', 'bar'),
        semantics=('.root', ('.label', ('.int', 1), ('.none', ('.map', ('.gt', ('.int', 4)), ('.list', ('.int', 1), ('.int', 2), ('.int', 3))))))),
]

grouping = [
    # Parentheses
    Explanation(
        condition="True or (True and False)",
        label=1,
        candidate=('foo', 'bar'),
        semantics=('.root', ('.label', ('.int', 1), ('.or', ('.bool', True), ('.and', ('.bool', True), ('.bool', False)))))),
]

integers = [
    # Equals (Int)
    Explanation(
        condition="1 is equal to 1",
        label=1,
        candidate=('foo', 'bar'),
        semantics=('.root', ('.label', ('.int', 1), ('.call', ('.eq', ('.int', 1)), ('.int', 1))))),
    # Integers (digit or text)
    Explanation(
        condition="1 is equal to one",
        label=1,
        candidate=('foo', 'bar'),
        semantics=('.root', ('.label', ('.int', 1), ('.call', ('.eq', ('.int', 1)), ('.int', 1))))),
    # Less than
    Explanation(
        condition="1 is less than 2",
        label=1,
        candidate=('foo', 'bar'),
        semantics=('.root', ('.label', ('.int', 1), ('.call', ('.lt', ('.int', 2)), ('.int', 1))))),
    # At most
    Explanation(
        condition="2 is less than or equal to 2",
        label=1,
        candidate=('foo', 'bar'),
        semantics=('.root', ('.label', ('.int', 1), ('.call', ('.leq', ('.int', 2)), ('.int', 2))))),
    # Greater than
    Explanation(
        condition="2 > 1",
        label=1,
        candidate=('foo', 'bar'),
        semantics=('.root', ('.label', ('.int', 1), ('.call', ('.gt', ('.int', 1)), ('.int', 2))))),
    # At least
    Explanation(
        condition="2 is at least 2",
        label=1,
        candidate=('foo', 'bar'),
        semantics=('.root', ('.label', ('.int', 1), ('.call', ('.geq', ('.int', 2)), ('.int', 2))))),
]

lists = [
    # OrList left
    Explanation(
        condition="7 or 5 is larger than 6",
        label=1,
        candidate=('foo', 'bar'),
        semantics=('.root',('.label',('.int', 1),('.any',('.map', ('.gt', ('.int', 6)), ('.list', ('.int', 7), ('.int', 5))))))),
    # OrList right
    Explanation(
        condition="2 is less than 3 or 1",
        label=1,
        candidate=('foo', 'bar'),
        semantics=('.root',('.label',('.int', 1),('.call',('.composite_or', ('.lt',), ('.list', ('.int', 3), ('.int', 1))),('.int', 2))))),
    # AndList left
    Explanation(
        condition="8 and 8 are equal to 8",
        label=1,
        candidate=('foo', 'bar'),
        semantics=('.root',('.label',('.int', 1),('.all',('.map', ('.eq', ('.int', 8)), ('.list', ('.int', 8), ('.int', 8))))))),
    # AndList right
    Explanation(
        condition="2 is less than 3 and 4",
        label=1,
        candidate=('foo', 'bar'),
        semantics=('.root',('.label',('.int', 1),('.call',('.composite_and', ('.lt',), ('.list', ('.int', 3), ('.int', 4))),('.int', 2))))),
    # Not AndList
    Explanation(
        condition="2 is not more than 1 and 3",
        label=1,
        candidate=('foo', 'bar'),
        semantics=('.root',('.label',('.int', 1),('.not',('.call',('.composite_and', ('.gt',), ('.list', ('.int', 1), ('.int', 3))),('.int', 2)))))),
    # Not OrList
    Explanation(
        condition="2 is not more than 3 or 4",
        label=1,
        candidate=('foo', 'bar'),
        semantics=('.root',('.label',('.int', 1),('.not',('.call',('.composite_or', ('.gt',), ('.list', ('.int', 3), ('.int', 4))),('.int', 2)))))),
]

membership = [
    # In
    Explanation(
        condition="1 is in (1, 2)",
        label=1,
        candidate=('foo', 'bar'),
        semantics=('.root', ('.label', ('.int', 1), ('.call', ('.in', ('.list', ('.int', 1), ('.int', 2))), ('.int', 1))))),
    # In AndList
    Explanation(
        condition="1 and 2 are in (1, 2, 3)",
        label=1,
        candidate=('foo', 'bar'),
        semantics=('.root', ('.label', ('.int', 1), ('.all', ('.map', ('.in', ('.list', ('.int', 1), ('.int', 2), ('.int', 3))), ('.list', ('.int', 1), ('.int', 2))))))),
    # In OrList
    Explanation(
        condition="1 or 2 is in (2, 3)",
        label=1,
        candidate=('foo', 'bar'),
        semantics=('.root', ('.label', ('.int', 1), ('.any', ('.map', ('.in', ('.list', ('.int', 2), ('.int', 3))), ('.list', ('.int', 1), ('.int', 2))))))),
    # Contains
    Explanation(
        condition="(1, 2) contains 2",
        label=1,
        candidate=('foo', 'bar'),
        semantics=('.root', ('.label', ('.int', 1), ('.call', ('.in', ('.list', ('.int', 1), ('.int', 2))), ('.int', 2))))),
    # Contains AndList
    Explanation(
        condition="(1, 2) contains 2 and 1",
        label=1,
        candidate=('foo', 'bar'),
        semantics=('.root', ('.label', ('.int', 1), ('.all', ('.map', ('.in', ('.list', ('.int', 1), ('.int', 2))), ('.list', ('.int', 2), ('.int', 1))))))),
    # Contains OrList
    Explanation(
        condition="(1, 2) contains 2 or 3",
        label=1,
        candidate=('foo', 'bar'),
        semantics=('.root', ('.label', ('.int', 1), ('.any', ('.map', ('.in', ('.list', ('.int', 1), ('.int', 2))), ('.list', ('.int', 2), ('.int', 3))))))),
]

absorption = [
    # Partially unparseable
    Explanation(
        condition="1 is less than 2 and the moon is full",
        label=1,
        candidate=('foo', 'bar'),
        semantics=('.root', ('.label', ('.int', 1), ('.call', ('.lt', ('.int', 2)), ('.int', 1)))))
]

explanations = (logic + grouping + integers + lists + membership + absorption)