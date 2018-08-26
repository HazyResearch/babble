from babble import Explanation

def get_aliases():
    return {
        'colors':['red','green','blue'],
        'bluebird':['blue','bird','fly'],
        'greek':['alpha','beta','gamma'],
        'letters':['a','B','C'],
        'smalls':['a','b','c','d'],
        'spouse':['wife','husband','spouse']
    }

# Test candidate:
# "City land records show that GM President [Daniel Ammann] and his wife,
# [Pernilla Ammann], bought the 15-bedroom mansion on Balmoral Drive in
# the upscale historic neighborhood on July 31."
# hash = 668761641257950361
# stable_id = 52a56fa5-91bf-4df1-8443-632f4c1ce88d::span:604:616~~52a56fa5-91bf-4df1-8443-632f4c1ce88d::span:632:646
default_candidate = '52a56fa5-91bf-4df1-8443-632f4c1ce88d::span:604:616~~52a56fa5-91bf-4df1-8443-632f4c1ce88d::span:632:646'

strings = [
    # Equals (String)
    Explanation(
        condition="'yes' equals 'yes'",
        label=1,
        candidate=('foo', 'bar'),
        semantics=None),
    # Lowercase
    Explanation(
        condition="X is lowercase",
        label=1,
        candidate=('foo', 'bar'),
        semantics=None),
    # Uppercase
    Explanation(
        condition="X is upper case",
        label=1,
        candidate=('FOO', 'bar'),
        semantics=None),
    # Capitalized
    Explanation(
        condition="X is capitalized",
        label=1,
        candidate=('Foo', 'bar'),
        semantics=None),
    # Starts with
    Explanation(
        condition="the word 'blueberry' starts with 'blue'",
        label=1,
        candidate=('foo', 'bar'),
        semantics=None),
    # Ends with
    Explanation(
        condition="the word 'blueberry' ends with 'berry'",
        label=1,
        candidate=('foo', 'bar'),
        semantics=None),
]

string_lists = [
    # In
    Explanation(
        condition="'bar' is in 'foobarbaz'",
        label=1,
        candidate=('foo', 'bar'),
        semantics=None),
    # Contains
    Explanation(
        condition="the word 'foobarbaz' contains 'oobarba'",
        label=1,
        candidate=('foo', 'bar'),
        semantics=None),
    # List
    Explanation(
        condition="'bar' equals 'foo', 'bar', or 'baz'",
        label=1,
        candidate=('foo', 'bar'),
        semantics=None),
    # UserList
    Explanation(
        condition="'blue' in colors",
        label=1,
        candidate=('foo', 'bar'),
        semantics=None),
    # OrList left
    Explanation(
        condition="'blue' or 'shmoo' is in colors",
        label=1,
        candidate=('foo', 'bar'),
        semantics=None),
    # OrList right
    Explanation(
        condition="'blue' ends with 'moe' or 'lue'",
        label=1,
        candidate=('foo', 'bar'),
        semantics=None),
    # AndList left
    Explanation(
        condition="'blue' and 'red' are in colors",
        label=1,
        candidate=('foo', 'bar'),
        semantics=None),
    # AndList right
    Explanation(
        condition="'blue' contains 'l' and 'u'",
        label=1,
        candidate=('foo', 'bar'),
        semantics=None),
]

candidate_helpers = [
    # Candidate as string
    Explanation(
        condition="X is 'foo'",
        label=1,
        candidate=('foo', 'bar'),
        semantics=None),
    # Left words (list)
    Explanation(
        condition="'wife' is in the words left of Y",
        label=1,
        candidate=default_candidate,
        semantics=None),
    # Right words (list)
    Explanation(
        condition="'wife' is in the words to the right of X",
        label=1,
        candidate=default_candidate,
        semantics=None),
    # Between words (list)
    Explanation(
        condition="'wife' is in the words between X and Y",
        label=1,
        candidate=default_candidate,
        semantics=None),
    # Sentence (list)
    Explanation(
        condition='"wife" is in the sentence',
        label=1,
        candidate=default_candidate,
        semantics=None),
]

index_words = [
    # Index left
    Explanation(
        condition="X is left of Y",
        label=1,
        candidate=default_candidate,
        semantics=None),
    # Index right
    Explanation(
        condition="Y is right of X",
        label=1,
        candidate=default_candidate,
        semantics=None),
    # Between
    Explanation(
        condition="'wife' is between X and Y",
        label=1,
        candidate=default_candidate,
        semantics=None),
    # Index left equality
    Explanation(
        condition="'wife' is two words to the left of Y",
        label=1,
        candidate=default_candidate,
        semantics=None),
    # Index left inequality 0
    Explanation(
        condition="X is more than three words to the left of Y",
        label=1,
        candidate=default_candidate,
        semantics=None),
    # Index left inequality 1
    Explanation(
        condition="not X is more than fifty words to the left of Y",
        label=1,
        candidate=default_candidate,
        semantics=None),
    # Index left inequality 2
    Explanation(
        condition="',' is immediately to the left of Y",
        label=1,
        candidate=default_candidate,
        semantics=None),
    # Index left inequality 3
    Explanation(
        condition="',' is right before Y",
        label=1,
        candidate=default_candidate,
        semantics=None),
    # Index within (<=)
    Explanation(
        condition="'wife' is within three words to the left of Y",
        label=1,
        candidate=default_candidate,
        semantics=None),
    # Index within (<= or >= left)
    Explanation(
        condition="'wife' is within three words of Y",
        label=1,
        candidate=default_candidate,
        semantics=None),
    # Index within (<= or >= right)
    Explanation(
        condition="'bought' is within three words of Y",
        label=1,
        candidate=default_candidate,
        semantics=None),
    # Index OrList left
    Explanation(
        condition="'husband' or 'wife' is within three words to the left of Y",
        label=1,
        candidate=default_candidate,
        semantics=None),
    # Index AndList left
    Explanation(
        condition="the words 'his' and 'wife' are no more than three words to the left of Y",
        label=1,
        candidate=default_candidate,
        semantics=None),
    # Index AndArgList
    Explanation(
        condition="'wife' is within three words to the left of X or Y",
        label=1,
        candidate=default_candidate,
        semantics=None),
]

index_chars = [
    # Characters0
    Explanation(
        condition="'wife' is less than 10 characters to the left of Y",
        label=1,
        candidate=default_candidate,
        semantics=None),
    # Characters1
    Explanation(
        condition="'wife' is more than 5 characters to the right of X",
        label=1,
        candidate=default_candidate,
        semantics=None),
    # Characters2
    Explanation(
        condition="there are at least 10 characters between X and Y",
        label=1,
        candidate=default_candidate,
        semantics=None),
]

ner = [
    # Tokens
    Explanation(
        condition="at least one word to the left of X is lower case",
        label=1,
        candidate=default_candidate,
        semantics=None),
    # NER
    Explanation(
        condition="there are no people between X and Y",
        label=1,
        candidate=default_candidate,
        semantics=None),
]

count = [
    # Count0
    Explanation(
        condition="there are not three people in the sentence",
        label=1,
        candidate=default_candidate,
        semantics=None),
    # Count1
    Explanation(
        condition="the number of words between X and Y is less than 25",
        label=1,
        candidate=default_candidate,
        semantics=None),
    # Count2
    Explanation(
        condition="there are at least two words between X and Y",
        label=1,
        candidate=default_candidate,
        semantics=None),
    # Count3
    Explanation(
        condition="at least one word exists between X and Y",
        label=1,
        candidate=default_candidate,
        semantics=None),
    # Count4
    Explanation(
        condition="at least one word to the left of Y starts with a spouse word",
        label=1,
        candidate=default_candidate,
        semantics=None),
]

anaphora = [
    # Them
    Explanation(
        condition="'wife' is between X and Y and 'divorced' is not between them",
        label=1,
        candidate=default_candidate,
        semantics=None),
    # TODO: add handling for he/she, his/her, him/her?
]

tuples = [
    # Tuple
    Explanation(
        condition="the pair (X, Y) is the same as the tuple ('foo', 'bar')",
        label=1,
        candidate=('foo', 'bar'),
        semantics=('.root', ('.label', ('.int', 1), ('.call', ('.eq', ('.tuple', ('.list', ('.string', u'foo'), ('.string', u'bar')))), ('.tuple', ('.list', ('.arg_to_string', ('.arg', ('.int', 1))), ('.arg_to_string', ('.arg', ('.int', 2))))))))),
]

implicit_strings = [
    # Normal
    Explanation(
        condition='It says "wife"',
        label=1,
        candidate=default_candidate,
        semantics=None),
    # Not quoted unigram
    Explanation(
        condition='It says wife',
        label=1,
        candidate=default_candidate,
        semantics=None),
    # Not quoted bigram
    Explanation(
        condition='It says historic neighborhood',
        label=1,
        candidate=default_candidate,
        semantics=None),
    # Not quoted bigram with stopword
    Explanation(
        condition='It says his wife',
        label=1,
        candidate=default_candidate,
        semantics=None),
    # Implicit candidate
    Explanation(
        condition='wife comes after Daniel Ammann',
        label=1,
        candidate=default_candidate,
        semantics=None),
    # Don't quote existing quotation
    Explanation(
        condition='It says "the upscale historic neighborhood"',
        label=1,
        candidate=default_candidate,
        semantics=None),
]