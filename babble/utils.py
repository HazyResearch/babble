from collections import Counter, defaultdict
import csv
import json
import os
import random
import sys
from time import time

from metal.contrib.info_extraction.mentions import RelationMention
from metal.contrib.info_extraction.utils import mark_entities
import numpy as np
import torch
from scipy.sparse import issparse

from .explanation import Explanation


class PrintTimer:
    """Prints msg at start, total time taken at end."""
    def __init__(self, msg, prefix="###"):
        self.msg = msg
        self.prefix = prefix + " " if len(prefix) > 0 else prefix

    def __enter__(self):
        self.t0 = time()
        print("{0}{1}".format(self.prefix, self.msg))

    def __exit__(self, type, value, traceback):
        print ("{0}Done in {1:.1f}s.\n".format(self.prefix, time() - self.t0))


class ProgressBar(object):
    def __init__(self, N, length=40):
        # Protect against division by zero (N = 0 results in full bar being printed)
        self.N      = max(1, N)
        self.nf     = float(self.N)
        self.length = length
        # Precalculate the i values that should trigger a write operation
        self.ticks = set([round(i/100.0 * N) for i in range(101)])
        self.ticks.add(N-1)
        self.bar(0)

    def bar(self, i):
        """Assumes i ranges through [0, N-1]"""
        if i in self.ticks:
            b = int(np.ceil(((i+1) / self.nf) * self.length))
            sys.stdout.write(
                "\r[{0}{1}] {2}%".format(
                    "="*b, " "*(self.length-b), int(100*((i+1) / self.nf))))
            sys.stdout.flush()

    def close(self):
        # Move the bar to 100% before closing
        self.bar(self.N-1)
        sys.stdout.write("\n\n")
        sys.stdout.flush()


class ExplanationIO(object):
    def write(self, explanations, fpath):
        explanations = explanations if isinstance(explanations, list) else [explanations]
        with open(fpath, 'w') as tsvfile:
            tsvwriter = csv.writer(tsvfile, delimiter='\t')
            for exp in explanations:
                if isinstance(exp.candidate, str):
                    candidate_id = exp.candidate
                else:
                    candidate_id = exp.candidate.mention_id
                tsvwriter.writerow([
                                    exp.name,
                                    exp.label,
                                    candidate_id,
                                    exp.condition,
                                    ])
        fpath = fpath if len(fpath) < 50 else fpath[:20] + '...' + fpath[-30:]
        print("Wrote {} explanations to {}".format(len(explanations), fpath))

    def read(self, fpath):
        with open(fpath, 'r') as tsvfile:
            tsvreader = csv.reader(tsvfile, delimiter='\t')
            num_read = 0
            explanations = []
            for (name, label, candidate_id, condition) in tsvreader:
                explanations.append(
                    Explanation(
                        name=name,
                        label=int(label),
                        candidate=candidate_id,
                        condition=condition.strip(),
                        )
                )
                num_read += 1
        fpath = fpath if len(fpath) < 50 else fpath[:20] + '...' + fpath[-30:]
        print("Read {} explanations from {}".format(num_read, fpath))
        return explanations


def link_explanation_candidates(explanations, candidates):
    """Doc string goes here."""

    target_candidate_ids = set()
    linked = 0
    print("Building list of target candidate ids...")
    for e in explanations:
        if e.candidate is not None and not isinstance(e.candidate, RelationMention):
            target_candidate_ids.add(e.candidate)
        elif e.candidate:
            linked += 1
    if linked == len(explanations):
        print("All {} explanations are already linked to candidates.".format(
            len(explanations)))
        return explanations
    else:
        print("Collected {} unique target candidate ids from {} explanations.".format(
            len(target_candidate_ids), len(explanations)))
    if not target_candidate_ids:
        print("No candidate hashes were provided. Skipping linking.")
        return explanations

    candidate_map = {}
    print("Gathering desired candidates...")
    for candidate in candidates:
        if candidate.mention_id in target_candidate_ids:
            candidate_map[candidate.mention_id] = candidate
    if len(candidate_map) < len(target_candidate_ids):
        num_missing = len(target_candidate_ids) - len(candidate_map)
        print("Could not find {} target candidates with the following mention_ids (first 5):".format(
            num_missing))
        num_reported = 0
        for i, c_hash in enumerate(target_candidate_ids):
            if c_hash not in candidate_map:
                print(c_hash)
                num_reported += 1
                if num_reported >= 5:
                    break

    print("Found {}/{} desired candidates".format(
        len(candidate_map), len(target_candidate_ids)))

    print("Linking explanations to candidates...")
    for e in explanations:
        if not isinstance(e.candidate, RelationMention):
            try:
                e.candidate = candidate_map[e.candidate]
                linked += 1
            except KeyError:
                pass

    print("Linked {}/{} explanations".format(linked, len(explanations)))

    return explanations

def sparse_to_indices(X):
    """Converts a sparse matrix into a tensor of the nonzero indices
    Args:
        X: an [n, num_features] one-hot scipy.sparse matrix
    Returns:
        X_idx: an [n, h] tensor where X_idx[i,:] is a zero-padded 1D tesnor of
            the nonzero indices of X[i,:]
    """
    if not issparse(X):
        raise ValueError("X must be a scipy.sparse matrix")
    nonzeros = X.nonzero()
    indices = defaultdict(list)
    for i, v in zip(nonzeros[0], nonzeros[1]):
        indices[i].append(v + 1)

    max_len = max(map(lambda x: len(x), indices.values()))
    X_idx = torch.zeros(X.shape[0], max_len).long()
    for i, values in indices.items():
        X_idx[i, :len(values)] = torch.LongTensor(values)
    return X_idx

def display_candidate(candidate):
    tokens = candidate.tokens
    positions = list(zip(candidate.word_starts, candidate.word_ends))
    markers = ['{', '}', '{', '}']
    marked = mark_entities(tokens, positions, markers, style='concatenate')
    print(' '.join(marked))
    print()
    print(marked)

class CandidateViewer(object):
    def __init__(self, candidates, shuffle=False, seed=None):
        if seed:
            random.seed(seed)

        self.candidates = candidates
        self.idx = -1
        self.order = list(range(len(candidates)))
        # Shuffle indirectly to not mess up alignment between candidates and
        # other objects in the workspace (e.g., labels).
        if shuffle:
            random.shuffle(self.order)

    def view(self):
        self.idx += 1
        if self.idx > len(self.order):
            print("Exhausted provided candidate set")
            return
        c = self.candidates[self.order[self.idx]]
        display_candidate(c)
        return c