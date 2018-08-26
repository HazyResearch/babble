from collections import defaultdict, namedtuple
import itertools
import random

import numpy as np
from pandas import DataFrame, Series
from scipy.sparse import csr_matrix, coo_matrix, lil_matrix
import scipy.sparse as sparse

from metal.analysis import lf_summary

from babble.filter_bank import FilterBank
from babble.explanation import Explanation
from babble.parsing import Parse, SemanticParser
from babble.utils import PrintTimer, ProgressBar, link_explanation_candidates

class BabbleStream(object):
    """
    Iteratively displays candidates, collects and parses explanations.

    Args:
        Cs: a list of lists containing the candidates for each split
        Ys: a list of arrays containing the ground truth labels for each split
        aliases: a dictionary of a aliases for the grammar
        entity_names: a list of two strings corresponding to custom names that
            will be recognized as referring to the first and second entity of
            each relation
        apply_filters: if True, apply the filter bank
        seed: an optional seed for the CandidateGenerator
        verbose: controls verbosity of print statements
    """
    def __init__(self, Cs, Ys, aliases={}, entity_names=[], apply_filters=True,
                 seed=None, verbose=True, **kwargs):
        self.Cs = Cs
        self.Ys = Ys
        self.aliases = aliases
        self.verbose = verbose
        self.entity_names = entity_names
        self.apply_filters = apply_filters

        self.splits = list(range(len(self.Cs)))
        self.candidate_generator = CandidateGenerator(self, seed=seed, **kwargs)

        self._build_semparser()
        self.filter_bank = FilterBank()
        self.filter_split = None

        self.parses = []
        self.label_matrix = None
        self.label_triples = [[[],[],[],0,0], [[],[],[],0,0], [[],[],[],0,0]]

        # Temporary storage
        self.temp_parses = None
        self.temp_label_matrix = None
        self.last_parses = []

        # Evaluation tools
        self.dev_size = len(Ys[1])
        for Y in Ys:
            if (Y == 0).sum() > 0:
                raise ValueError("Y matrices should not contain 0s.")

    def next(self):
        c = self.candidate_generator.next()
        self.temp_candidate = c
        return c

    def _build_semparser(self):
        self.semparser = SemanticParser(
            entity_names=self.entity_names,
            aliases=self.aliases, beam_width=10)

    def add_aliases(self, new_aliases):
        """
        Adds additional aliases and rebuilds SemanticParser.

        :param new_aliases: A dict {k: v, ...}
            k = (string) list name
            v = (list) words belonging to the alias
        """
        self.aliases.update(new_aliases)
        self._build_semparser()

    def preload(self, explanations=None, aliases=None, label_others=True):
        """
        Load and commit the provided aliases and/or explanations.
        """
        if aliases:
            self.add_aliases(aliases)
        if explanations:
            parses, _, = self.apply(explanations)
            if parses:
                self.commit()

    def apply(self, explanations, split=0):
        """
        :param explanations: an Explanation or list of Explanations.
        :param split: the split to use for the filter bank
        """
        # Flush all uncommmitted results from previous runs
        self.commit([])
        # Store the number of the split the filter bank will use
        self.filter_split = split

        candidates = self.Cs[split]
        explanations = explanations if isinstance(explanations, list) else [explanations]

        # Replace candidate ids with actual candidate objects in explanations
        # if they don't already have candidate objects stored
        explanations = link_explanation_candidates(
            explanations, itertools.chain(*(self.Cs)))

        parses, unparseable_explanations = self._parse(explanations)
        if self.apply_filters:
            parses, filtered_parses, label_matrix = self._filter(
                parses, explanations, candidates)
        else:
            print("Because apply_filters=False, no parses are being filtered.")
            filtered_parses = {}
            label_matrix = self.filter_bank.label(parses, candidates)

        filtered_objects = filtered_parses
        filtered_objects['UnparseableExplanations'] = unparseable_explanations

        # Hold results in temporary space until commit
        self.temp_parses = parses if isinstance(parses, list) else [parses]
        self.temp_label_matrix = label_matrix
        self.temp_filtered_objects = filtered_objects

        return parses, filtered_objects

    def _parse(self, explanations):
        """
        :param explanations: an Explanation or list of Explanations.
        :return: a list of Parses.
        """
        parses = self.semparser.parse(explanations,
            return_parses=True, verbose=self.verbose)
        used_explanations = set([p.explanation for p in parses])
        unparseable_explanations = [FilteredExplanation(exp, 'Unparseable')
            for exp in explanations if exp not in used_explanations]

        return parses, unparseable_explanations

    def _filter(self, parses, explanations, candidates):
        """
        :param parses: a Parse or list of Parses.
        :param explanations: the Explanation or list of Explanations from which
            the parse(s) were produced.
        :return: the outputs from filter_bank.apply()
        """
        return self.filter_bank.apply(parses, explanations, candidates)

    def analyze(self, parses):
        lf_names = []
        L = lil_matrix((len(self.Cs[1]), len(parses)))
        for j, p in enumerate(parses):
            lf_names.append(p.function.__name__)
            for i, c in enumerate(self.Cs[1]):
                L[i,j] = p.function(c)
        return lf_summary(L.tocsr(), Y=self.Ys[1], lf_names=lf_names)

    def filtered_analysis(self, filtered_parses=None):
        if filtered_parses is None:
            # Use the last set of filtered parses to be produced.
            filtered_parses = self.temp_filtered_objects

        if filtered_parses is None or not any(filtered_parses.values()):
            print("No filtered parses to analyze.")
            return

        filter_names = [
            'UnparseableExplanations',
            'DuplicateSemanticsFilter',
            'ConsistencyFilter',
            'UniformSignatureFilter',
            'DuplicateSignatureFilter',
            'LowestCoverageFilter',
        ]

        num_filtered = 0
        print("SUMMARY")
        print("{} TOTAL:".format(
            sum([len(p) for p in filtered_parses.values()])))
        print("{} Unparseable Explanation".format(
            len(filtered_parses.get('UnparseableExplanations', []))))
        print("{} Duplicate Semantics".format(
            len(filtered_parses.get('DuplicateSemanticsFilter', []))))
        print("{} Inconsistency with Example".format(
            len(filtered_parses.get('ConsistencyFilter', []))))
        print("{} Uniform Signature".format(
            len(filtered_parses.get('UniformSignatureFilter', []))))
        print("{} Duplicate Signature".format(
            len(filtered_parses.get('DuplicateSignatureFilter', []))))
        print("{} Lowest Coverage".format(
            len(filtered_parses.get('LowestCoverageFilter', []))))

        for filter_name in filter_names:
            parses = filtered_parses.get(filter_name, [])

            for filtered_parse in parses:
                num_filtered += 1

                if filtered_parse.reason == 'Unparseable':
                    parse_str = filtered_parse.parse.condition
                else:
                    parse_str = self.semparser.grammar.translate(filtered_parse.parse.semantics)

                if filter_name == 'UnparseableExplanations':
                    filter_str = "Unparseable Explanation"
                    reason_str = "This explanation couldn't be parsed."

                elif filter_name == 'DuplicateSemanticsFilter':
                    filter_str = "Duplicate Semantics"
                    reason_str = 'This parse is identical to one produced by the following explanation:\n\t"{}"'.format(
                        filtered_parse.reason.explanation.condition)

                elif filter_name == 'ConsistencyFilter':
                    candidate = filtered_parse.reason
                    filter_str = "Inconsistency with Example"
                    reason_str = "This parse abstained on its own candidate ({})".format(
                        candidate)

                elif filter_name == 'UniformSignatureFilter':
                    filter_str = "Uniform Signature"
                    reason_str = "This parse labeled {} of the {} development examples".format(
                        filtered_parse.reason, self.dev_size)

                elif filter_name == 'DuplicateSignatureFilter':
                    filter_str = "Duplicate Signature"
                    reason_str = "This parse labeled identically to the following existing parse:\n\t{}".format(
                        self.semparser.grammar.translate(filtered_parse.reason.explanation))

                elif filter_name == 'LowestCoverageFilter':
                    filter_str = "Lowest Coverage"
                    reason_str = "This parse had the lowest coverage of all parses passing the other filters"

                print("\n[#{}]: {}".format(num_filtered, filter_str))
                # print("\nFilter: {}".format(filter_str))
                if filtered_parse.reason == 'Unparseable':
                    print("\nExplanation: {}".format(parse_str))
                else:
                    print("\nParse: {}".format(parse_str))
                print("\nReason: {}\n".format(reason_str))

                print("Semantics: {}\n".format(filtered_parse.parse.semantics))

    def commit(self, idxs='all'):
        """
        :param idxs: The indices of the parses (from the most recently returned
            list of parses) to permanently keep.
            If idxs = 'all', keep all of the parses.
            If idxs is an integer, keep just that one parse.
            If idxs is a list of integers, keep all parses from that list.
            If idxs = None or [], keep none of the parses.
        """
        if not self.temp_parses:
            idxs = []

        if idxs == 'all':
            idxs = list(range(len(self.temp_parses)))
        elif isinstance(idxs, int):
            idxs = [idxs]
        elif idxs == [] or idxs is None:
            idxs = []
            if self.temp_parses:
                print("Flushing all parses from previous explanation set.")

        if (isinstance(idxs, list) and len(idxs) > 0 and
            all(isinstance(x, int) for x in idxs)):
            if max(idxs) >= len(self.temp_parses):
                raise Exception("Invalid idx: {}.".format(max(idxs)))

            parses_to_add = [p for i, p in enumerate(self.temp_parses) if i in idxs]
            explanations_to_add = set([parse.explanation for parse in parses_to_add])

            # Update label matrix for label split
            self.parses.extend(parses_to_add)
            if self.label_matrix is None:
                self.label_matrix = self.temp_label_matrix
            else:
                self.label_matrix = sparse.hstack((self.label_matrix, self.temp_label_matrix))

            self.last_parses = parses_to_add
            if self.verbose:
                print("Added {} parse(s) from {} explanations to set. (Total # parses = {})\n".format(
                    len(parses_to_add), len(explanations_to_add), len(self.parses)))

            # Update label matrix for other splits
            for split in self.splits:
                if split == self.filter_split:
                    continue
                self.label_split(split)

        # Permanently store the semantics and signatures in duplicate filters
        self.filter_bank.commit(idxs)

        self.temp_parses = None
        self.temp_label_matrix = None

    def label_split(self, split):
        """Label a single split with the most recently committed LFs."""
        print("Applying labeling functions to split {}".format(split))
        lfs = [parse.function for parse in self.last_parses]
        candidates = self.Cs[split]
        num_existing_lfs = self.label_triples[split][4]

        rows = []
        cols = []
        data = []
        pb = ProgressBar(len(candidates) * len(lfs))
        count = 0
        for j, lf in enumerate(lfs):
            for i, c in enumerate(candidates):
                pb.bar(count)
                count += 1
                label = int(lf(c))
                if label:
                    rows.append(i)
                    cols.append(j + num_existing_lfs)
                    data.append(label)
        pb.close()
        # NOTE: There is potential for things to go wrong if the user calls
        # this function twice and the label matrix ends up wonky.
        self.label_triples[split][0].extend(rows)
        self.label_triples[split][1].extend(cols)
        self.label_triples[split][2].extend(data)
        self.label_triples[split][3] = len(candidates)
        self.label_triples[split][4] += len(lfs)
        m, n = self.label_triples[split][3], self.label_triples[split][4]
        print(f"Added {len(data)} labels to split {split}: "
            f"L.nnz = {len(self.label_triples[split][2])}, "
            f"L.shape = ({m}, {n}).")

    def get_label_matrix(self, split):
        """Retrieve the given split's label matrix from all commited parses"""
        if self.temp_parses is not None:
            print("You must commit before retrieving the label matrix.")
            return None

        if split == self.filter_split:
            L = self.label_matrix
            L = self.label_matrix
        else:
            rows, cols, data, shape_row, shape_col = self.label_triples[split]
            L = coo_matrix((data, (rows, cols)), shape=(shape_row, shape_col))

        if self.verbose:
            print(f"Retrieved label matrix for split {split}: L.nnz = {L.nnz}, "
                f"L.shape = {L.shape}")
        return L.astype(int).tocsr()

    def error_buckets(self, parse):
        correct = []
        incorrect = []
        for c, l in zip(self.Cs[1], self.Ys[1]):
            vote = parse.function(c)
            if vote == 0:
                continue
            elif vote == l:
                correct.append(c)
            else:
                incorrect.append(c)
        return (correct, incorrect)

    def view_parse(self, parse):
        print(f"Name: {parse.function.__name__}")
        print(f"Parse: {self.semparser.grammar.translate(parse.semantics)}")

    def get_parses(self, idx=None, translate=True):
        if idx is None:
            parses = self.parses
        elif isinstance(idx, int):
            parses = [self.parses[idx]]
        elif isinstance(idx, list):
            parses = [parse for i, parse in enumerate(self.parses) if i in idx]

        if translate:
            return [self.semparser.grammar.translate(parse.semantics) for parse in parses]
        else:
            return parses

    def get_lfs(self, idx=None):
        return [parse.function for parse in self.get_parses(idx=idx, translate=False)]

    def get_explanations(self, idx=None):
        explanations = []
        explanations_set = set()
        for parse in self.get_parses(idx=idx, translate=False):
            explanation = parse.explanation
            if explanation not in explanations_set:
                explanations.append(explanation)
                explanations_set.add(explanation)
        return explanations


class Babbler(BabbleStream):
    def apply(self, *args, **kwargs):
        BabbleStream.apply(self, *args, **kwargs)
        self.commit()

# Use 'parse' as field instead of 'explanation' to match with FilteredParse object.
FilteredExplanation = namedtuple('FilteredExplanation', ['parse', 'reason'])

class CandidateGenerator(object):
    """
    A generator for returning a list of candidates in a certain order.
    """
    def __init__(self, babble_stream, seed=None,
                 balanced=False, active=False, shuffled=False,
                 priority_candidate_ids=[]):
        """
        If active = True, return only candidates that have no labels so far
        If balanced = True, alternate between candidates with True/False gold labels
        If random = True, return the candidates (passing the above conditions,
            if applicable) in random order.
        """
        candidates = babble_stream.Cs[1]
        labels = babble_stream.Ys[1]

        candidates, labels, priority_generator = self.make_priority_generator(
            candidates, labels, priority_candidate_ids)
        self.priority_generator = priority_generator

        if active:
            raise NotImplementedError
        else:
            if balanced:
                self.candidate_generator = itertools.chain(
                    priority_generator, self.balanced_generator(
                        candidates, labels, seed, shuffled=shuffled))
            else:
                self.candidate_generator = itertools.chain(
                    priority_generator, self.linear_generator(
                        candidates, seed, shuffled=shuffled))

    def next(self):
        return self.candidate_generator.__next__()

    def make_priority_generator(self, candidates, labels, priority_candidate_ids):
        # Pull out priority candidates to view first if applicable
        # Go for the slightly more wasteful but easy-to-understand solution

        if priority_candidate_ids:
            def simple_generator(candidates):
                for c in candidates:
                    yield c

            priority_set = set(priority_candidate_ids)
            priority = []
            other = []

            # Pull out all priority candidates
            for c, l in zip(candidates, labels):
                if c.mention_id in priority_set:
                    priority.append(c)
                else:
                    # Hold on to the labels for a possible balanced_generator downstream
                    other.append((c, l))
            # Put them in desired order
            priority_idxs = {c: i for i, c in enumerate(priority_candidate_ids)}
            priority.sort(key=lambda x: priority_idxs[x.mention_id])
            priority_generator = simple_generator(priority)
            # Restore remaining candidates and labels to normal lists
            candidates, labels = zip(*other)
        else:
            priority_generator = iter(())

        return candidates, labels, priority_generator

    @staticmethod
    def linear_generator(candidates, seed, shuffled=False):
        if shuffled:
            if seed is not None:
                random.seed(seed)
            random.shuffle(candidates)
        for c in candidates:
            yield c

    @staticmethod
    def balanced_generator(candidates, labels, seed, shuffled=False):
        candidates_labels = list(zip(candidates, labels))
        if shuffled:
            if seed is not None:
                random.seed(seed)
            random.shuffle(candidates_labels)

        groups = defaultdict(list)
        for c, l in candidates_labels:
            groups[l].append(c)

        counters = {k: 0 for k, _ in groups.items()}
        candidate_queue = []
        label_queue = []
        total = 0
        while total < len(candidates):
            for label, cands in sorted(groups.items()):
                if counters[label] < len(cands):
                    candidate_queue.append(cands[counters[label]])
                    label_queue.append(label)
                    counters[label] += 1
                    total += 1
        for c in candidate_queue:
            yield c