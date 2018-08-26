import re

class Explanation(object):
    def __init__(self, condition, label, candidate=None, name=None,
                 semantics=None, paraphrase=None):
        """
        Constructs an Explanation object.

        :param condition: A string explanation that expresses a Boolean
            condition (e.g., "The sentence is at least 5 words long.")
        :param label: The categorical label (1,...,k) to apply to candidates
            for which the condition evaluates to True.
        :param candidate: A candidate that the explanation is consistent with.
            May be a candidate object or the candidate's stable_id (for linking
            later.)
        :param name: The name of this explanation.
        :param semantics: The intended semantic representation of the
            explanation (if known).
        """
        assert(isinstance(condition, str))
        condition = re.sub(r'\s+', ' ', condition)
        self.condition = condition
        self.label = label
        self.candidate = candidate
        self.name = name
        self.semantics = semantics

    def __hash__(self):
        return hash((self.label, self.condition, self.candidate))

    def __repr__(self):
        if self.name:
            return 'Explanation(%s: %s, "%s")' % (self.name, self.label, self.condition)
        else:
            return 'Explanation(%s, "%s")' % (self.label, self.condition)

    def display(self):
        """Prints the explanation in a format that can be copied and pasted"""
        if isinstance(self.candidate, str):
            candidate_id = self.candidate
        else:
            candidate_id = self.candidate.mention_id()
        tab = '    '

        print(
            f"Explanation(\n"
                f"{tab}name='{self.name}',\n"
                f"{tab}label='{self.label}',\n"
                f"{tab}condition='{self.condition}',\n"
                f"{tab}candidate='{candidate_id}',\n"
            f")"
        )