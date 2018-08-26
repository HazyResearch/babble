import pickle
import os
import unittest

from babble import SemanticParser

from test_babble_base import TestBabbleBase
import text_explanations

class TestBabbleText(TestBabbleBase):

    @classmethod
    def setUpClass(cls):
        cls.sp = SemanticParser(aliases=text_explanations.get_aliases(),
                                string_format='implicit')

        DATA_FILE = 'tutorial/data/tutorial_data.pkl'
        with open(DATA_FILE, 'rb') as f:
            Cs, _ = pickle.load(f)

        cls.candidate_map = {}
        for c in Cs[0]:
            cls.candidate_map[c.mention_id] = c

    def test_strings(self):
        self.check_explanations(text_explanations.strings)

    def test_string_lists(self):
        self.check_explanations(text_explanations.string_lists)

    def test_candidate_helpers(self):
        self.check_explanations(text_explanations.candidate_helpers)

    def test_index_words(self):
        self.check_explanations(text_explanations.index_words)

    def test_index_chars(self):
        self.check_explanations(text_explanations.index_chars)

    def test_pos_ner(self):
        self.check_explanations(text_explanations.ner)

    def test_count(self):
        self.check_explanations(text_explanations.count)

    def test_anaphora(self):
        self.check_explanations(text_explanations.anaphora)

    def test_tuples(self):
        self.check_explanations(text_explanations.tuples)

    def test_implicit_strings(self):
        self.check_explanations(text_explanations.implicit_strings)