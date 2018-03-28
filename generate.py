from collections import defaultdict
import random

class PCFG(object):

    def __init__(self, use_trees):
        self._rules = defaultdict(list)
        self._sums = defaultdict(float)
        self._use_trees = use_trees
        self._rule_stack = []

    def print_tree(self):
        self._rule_stack.reverse()
        segment_string = ""
        while len(self._rule_stack) > 0:
            leaf = self._rule_stack.pop()

            if leaf == ')':
                print segment_string + "\n"
                segment_string = ""
            segment_string += leaf + " "

    def add_rule(self, lhs, rhs, weight):
        assert (isinstance(lhs, str))
        assert (isinstance(rhs, list))
        self._rules[lhs].append((rhs, weight))
        self._sums[lhs] += weight

    @classmethod
    def from_file(cls, filename, use_trees):
        grammar = PCFG( use_trees)
        with open(filename) as fh:
            for line in fh:
                line = line.split("#")[0].strip()
                if not line: continue
                w, l, r = line.split(None, 2)
                r = r.split()
                w = float(w)
                grammar.add_rule(l, r, w)
        return grammar

    def is_terminal(self, symbol):
        return symbol not in self._rules

    def gen(self, symbol):
        if self.is_terminal(symbol):
            return symbol
        else:
            expansion = self.random_expansion(symbol)
            tmp_list = []
            for s in expansion:
                if self.is_terminal(s):
                    tmp_list.append(s)
                else:
                    tmp_list += [[s] + (self.gen(s))]
            return (tmp_list)


    def random_sent(self):
        # Empty the rule stack
        self._rule_stack = []

        graph_list = ["ROOT"] + self.gen("ROOT")
        words, graph_str = self.extract_words_graph(graph_list)

        if self._use_trees:
            print("\n".join(graph_str))

        return words

    def extract_words_graph(self, lst, level=0):
        words = []
        graph_row_str = []
        graph_row_str += ['    ' * (level - 1) + '+---' * (level > 0) + lst[0]]
        for l in lst[1:]:
            if type(l) is list:
                tmp_w, tmp_g_print = self.extract_words_graph(l, level + 1)
                words += tmp_w
                graph_row_str += (tmp_g_print)
            else:
                graph_row_str += ['    ' * level + '+---' + l]
                words.append(l)
        return words, graph_row_str

    def print_sentence(self, graph):
        pass

    def random_expansion(self, symbol):
        """
        Generates a random RHS for symbol, in proportion to the weights.
        """
        p = random.random() * self._sums[symbol]
        for r, w in self._rules[symbol]:
            p = p - w
            if p < 0: return r
        return r


def _print_sentences(grammar_file, num_sentences, use_trees):
    pcfg = PCFG.from_file(grammar_file, use_trees)
    for i in xrange(num_sentences):
        sentence = pcfg.random_sent()
        print " ".join(sentence)
        print ""
        print "--------------------------------------------------------------"


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("grammar", help="enter a grammar")

    parser.add_argument("-n", "--num_sentences", type=int,
                        help="number of sentences to generate")

    parser.add_argument("-t", "--trees", help="generate a grammar tree", action="store_true")

    args = parser.parse_args()

    num_sentences = args.num_sentences or 1
    _print_sentences(args.grammar, num_sentences, args.trees)

