import pickle
import sys
import unittest

class TestBabbleBase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        DATA_FILE = 'tutorial/data/tutorial_data.pkl'
        with open(DATA_FILE, 'rb') as f:
            Cs, _ = pickle.load(f)

        cls.candidate_map = {}
        for c in Cs[0]:
            cls.candidate_map[c.mention_id] = c

    @classmethod
    def tearDownClass(cls):
        pass

    def check_explanations(self, explanations):
        num_explanations = len(explanations)
        num_parses = 0
        self.assertTrue(len(explanations))
        for exp in explanations:
            if isinstance(exp.candidate, str):
                exp.candidate = self.candidate_map[exp.candidate]
            parse_dict = self.sp.parse_and_evaluate(exp, show_erroring=True)
            num_correct = len(parse_dict['correct'])
            num_passing = len(parse_dict['passing'])
            num_failing = len(parse_dict['failing'])
            num_erroring = len(parse_dict['erroring'])
            num_acceptable = num_correct + num_passing
            if num_acceptable == 0:
                print(parse_dict)
                if num_failing:
                    for failing in parse_dict['failing']:
                        print("Failed parse:")
                        print(self.sp.grammar.translate(failing.semantics))
                if num_erroring:
                    print("It should not be possible to parse a function that throws an error:")
                    self.sp.grammar.print_chart()
                    parses = self.sp.parse(exp, return_parses=True)
            if exp.semantics:
                self.assertTrue(num_correct > 0)
            else:
                self.assertTrue(num_passing > 0)
            self.assertTrue(num_acceptable <= 3)
            num_parses += num_acceptable
        sys.stdout.write("{}/{} ({}%) - ".format(num_parses, num_explanations,
            float(num_parses)/num_explanations * 100))
        sys.stdout.flush()