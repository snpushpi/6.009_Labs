#!/usr/bin/env python3
import os.path
import lab
import json
import unittest
import types
import pickle

import sys
sys.setrecursionlimit(10000)

TEST_DIRECTORY = os.path.dirname(__file__)

# convert trie into a dictionary...
def dictify(t):
    out = {'value': t.value, 'children': {}}
    for ch, child in t.children.items():
        out['children'][ch] = dictify(child)
    return out

# ...and back
def from_dict(d):
    t = lab.Trie()
    for k, v in d.items():
        t[k] = v
    return t

# make sure the keys are not explicitly stored in any node
def any_key_stored(trie, keys):
    keys = [tuple(k) for k in keys]
    for i in dir(trie):
        try:
            val = tuple(getattr(trie, i))
        except:
            continue
        for j in keys:
            if j == val:
                return repr(i), repr(j)
    for child in trie.children.values():
        key_stored = any_key_stored(child, keys)
        if key_stored:
            return key_stored
    return None

# read in expected result
def read_expected(fname):
    with open(os.path.join(TEST_DIRECTORY, 'resources', 'testing_data', fname), 'rb') as f:
        return pickle.load(f)

class Test_1_Trie(unittest.TestCase):
    def test_01_set(self):
        trie = lab.Trie()
        trie['cat'] = 'kitten'
        trie['car'] = 'tricycle'
        trie['carpet'] = 'rug'
        expect = read_expected('1.pickle')
        self.assertTrue(dictify(trie) == expect, msg="Your trie is incorrect.")
        self.assertEqual(any_key_stored(trie, ('cat', 'car', 'carpet')), None)

        t = lab.Trie()
        t['a'] = 1
        t['an'] = 1
        t['ant'] = 1
        t['anteater'] = 1
        t['ants'] = 1
        t['a'] = 2
        t['an'] = 2
        t['a'] = 3
        expect = read_expected('2.pickle')
        self.assertTrue(dictify(t) == expect, msg="Your trie is incorrect.")
        self.assertEqual(any_key_stored(t, ('an', 'ant', 'anteater', 'ants')), None)
        with self.assertRaises(TypeError):
            t[(1, 2, 3)] = 20

        t = lab.Trie()
        t['man'] = 'person'
        t['mat'] = 'object'
        t['mattress'] = 'thing you sleep on'
        t['map'] = 'pam'
        t['me'] = 'you'
        t['met'] = 'tem'
        t['a'] = '?'
        t['map'] = -1000
        expect = read_expected('3.pickle')
        self.assertTrue(dictify(t) == expect, msg="Your trie is incorrect.")
        self.assertEqual(any_key_stored(t, ('man', 'mat', 'mattress', 'map', 'me', 'met', 'map')), None)
        with self.assertRaises(TypeError):
            t['something',] = 'pam'

    def test_02_get(self):
        d = {'name': 'John', 'favorite_numbers': [2, 4, 3], 'age': 39}
        t = from_dict(d)
        self.assertEqual(dictify(t), read_expected('person.pickle'))
        self.assertTrue(all(t[k] == d[k] for k in d))
        self.assertEqual(None, any_key_stored(t, tuple(d)))

        c = {'make': 'Toyota', 'model': 'Corolla', 'year': 2006, 'color': 'beige'}
        t = from_dict(c)
        self.assertEqual(dictify(t), read_expected('car.pickle'))
        self.assertTrue(all(t[k] == c[k] for k in c))
        self.assertEqual(None, any_key_stored(t, tuple(c)))
        for i in ('these', 'keys', 'dont', 'exist'):
            with self.assertRaises(KeyError):
                x = t[i]
        with self.assertRaises(TypeError):
            x = t[(1, 2, 3)]

    def test_03_contains(self):
        d = {'name': 'John', 'favorite_numbers': [2, 4, 3], 'age': 39}
        t = from_dict(d)
        self.assertEqual(dictify(t), read_expected('person.pickle'))
        self.assertTrue(all(i in t for i in d))

        c = {'make': 'Toyota', 'model': 'Corolla', 'year': 2006, 'color': 'beige'}
        t = from_dict(c)
        self.assertEqual(dictify(t), read_expected('car.pickle'))
        self.assertTrue(all(i in t for i in c))
        badkeys = ('these', 'keys', 'dont', 'exist', 'm', 'ma', 'mak', 'mo',
                   'mod', 'mode', 'ye', 'yea', 'y', '', 'car.pickle')
        self.assertTrue(all(i not in t for i in badkeys))

    def test_04_iter(self):
        t = lab.Trie()
        t['man'] = 'person'
        t['mat'] = 'object'
        t['mattress'] = 'thing you sleep on'
        t['map'] = 'pam'
        t['me'] = 'you'
        t['met'] = 'tem'
        t['a'] = '?'
        t['map'] = -1000
        self.assertTrue(hasattr(iter(t), '__next__'), "__iter__ must either produce a generator or an iterator")
        l = sorted(list(t))
        expected = [('a', '?'), ('man', 'person'), ('map', -1000), ('mat', 'object'),
                    ('mattress', 'thing you sleep on'), ('me', 'you'), ('met', 'tem')]
        self.assertEqual(expected, l)

    def test_05_delete(self):
        c = {'make': 'Toyota', 'model': 'Corolla', 'year': 2006, 'color': 'beige'}
        t = from_dict(c)
        self.assertEqual(read_expected('car.pickle'), dictify(t))
        del t['color']
        self.assertTrue(hasattr(iter(t), '__next__'), "__iter__ must either produce a generator or an iterator")
        self.assertEqual(set(t), set(c.items()) - {('color', 'beige')})
        t['color'] = 'silver'  # new paint job
        for i in t:
            if i[0] != 'color':
                self.assertIn(i, c.items())
            else:
                self.assertEqual('silver', i[1])

        t = lab.Trie()
        t['man'] = 'person'
        t['mat'] = 'object'
        t['mattress'] = 'thing you sleep on'
        t['map'] = 'pam'
        t['me'] = 'you'
        t['met'] = 'tem'
        t['a'] = '?'
        t['map'] = -1000
        self.assertTrue(hasattr(iter(t), '__next__'), "__iter__ must either produce a generator or an iterator")
        l = sorted(list(t))
        expected = [('a', '?'), ('man', 'person'), ('map', -1000), ('mat', 'object'),
                    ('mattress', 'thing you sleep on'), ('me', 'you'), ('met', 'tem')]
        self.assertEqual(expected, l)
        del t['mat']
        l = sorted(list(t))
        expected = [('a', '?'), ('man', 'person'), ('map', -1000),
                    ('mattress', 'thing you sleep on'), ('me', 'you'), ('met', 'tem')]
        self.assertEqual(expected, l)




class Test_2_TupleTrie(unittest.TestCase):
    def test_01_set(self):
        trie = lab.Trie()
        trie[(1, 2, 3)] = 'kitten'
        trie[(1, 2, 0)] = 'tricycle'
        trie[(1, 2, 0, 1)] = 'rug'
        expect = read_expected('4.pickle')
        self.assertTrue(dictify(trie) == expect, msg="Your trie is incorrect.")
        self.assertEqual(None, any_key_stored(trie, ((1, 2, 3), (1, 2, 0), (1, 2, 0, 1))))

        t = lab.Trie()
        t[(7, 8, 9)] = 1
        t[(7, 8, 9, 'hello')] = 1
        t[(7, 8, 9, 'hello', (1, 2))] = 1
        t[(1, )] = 1
        t[(7, )] = 1
        t[(7, 8, 9)] = 2
        t[(-1, -2, -3)] = 2
        t[('a', )] = 3
        expect = read_expected('5.pickle')
        self.assertTrue(dictify(t) == expect, msg="Your trie is incorrect.")
        self.assertEqual(None, any_key_stored(t, ((7, 8, 9), (7, 8, 9, 'hello'),
                                               (7, 8, 9, 'hello', (1, 2)), (1, ),
                                               (7, ), (-1, -2, -3), ('a', ))))

    def test_02_get(self):
        d = {'name': 'John', 'favorite_numbers': [2, 4, 3], 'age': 39}
        d = {tuple(k): v for k,v in d.items()}
        t = from_dict(d)
        self.assertEqual(read_expected('tuple_person.pickle'), dictify(t))
        self.assertTrue(all(t[k] == d[k] for k in d))
        self.assertEqual(None, any_key_stored(t, tuple(d)))
        with self.assertRaises(TypeError):
            t['string'] = 20

        c = {'make': 'Toyota', 'model': 'Corolla', 'year': 2006, 'color': 'beige'}
        c = {tuple(k): v for k,v in c.items()}
        t = from_dict(c)
        self.assertEqual(read_expected('tuple_car.pickle'), dictify(t))
        self.assertTrue(all(t[k] == c[k] for k in c))
        self.assertEqual(None, any_key_stored(t, tuple(c)))
        for i in ('these', 'keys', 'dont', 'exist'):
            with self.assertRaises(KeyError):
                x = t[tuple(i)]
        with self.assertRaises(TypeError):
            t[('yarn', 'twine', 'thread')[0]] = 20

    def test_03_contains(self):
        d = {'name': 'John', 'favorite_numbers': [2, 4, 3], 'age': 39}
        d = {tuple(k): v for k,v in d.items()}
        t = from_dict(d)
        self.assertEqual(read_expected('tuple_person.pickle'), dictify(t))
        self.assertTrue(all(i in t for i in d))
        with self.assertRaises(TypeError):
            x = t['string']

        c = {'make': 'Toyota', 'model': 'Corolla', 'year': 2006, 'color': 'beige'}
        c = {tuple(k): v for k,v in c.items()}
        t = from_dict(c)
        self.assertEqual(read_expected('tuple_car.pickle'), dictify(t))
        self.assertTrue(all(i in t for i in c))
        badkeys = ('these', 'keys', 'dont', 'exist', 'm', 'ma', 'mak', 'mo',
                   'mod', 'mode', 'ye', 'yea', 'y', '', 'car.pickle')
        self.assertTrue(all(tuple(i) not in t for i in badkeys))
        with self.assertRaises(TypeError):
            x = t[('yarn', 'twine', 'thread')[0]]

    def test_04_iter(self):
        t = lab.Trie()
        t[(7, 8, 9)] = 1
        t[(7, 8, 9, 'hello')] = 1
        t[(7, 8, 9, 'hello', (1, 2))] = 1
        t[(1, )] = 1
        t[(7, )] = 1
        t[(7, 8, 9)] = 2
        t[(-1, -2, -3)] = 2
        t[(2, )] = 3
        self.assertTrue(hasattr(iter(t), '__next__'), "__iter__ must either produce a generator or an iterator")
        l = sorted(list(t))
        expected = [((-1, -2, -3), 2), ((1,), 1), ((2,), 3), ((7,), 1),
                    ((7, 8, 9), 2), ((7, 8, 9, 'hello'), 1), ((7, 8, 9, 'hello', (1, 2)), 1)]
        self.assertEqual(expected, l)

    def test_05_delete(self):
        c = {'make': 'Toyota', 'model': 'Corolla', 'year': 2006, 'color': 'beige'}
        c = {tuple(k): v for k,v in c.items()}
        t = from_dict(c)
        self.assertEqual(read_expected('tuple_car.pickle'), dictify(t))
        del t[tuple('color')]
        self.assertTrue(hasattr(iter(t), '__next__'), "__iter__ must either produce a generator or an iterator")
        self.assertEqual(set(c.items()) - {(tuple('color'), 'beige')}, set(t))
        t[tuple('color')] = 'silver'  # new paint job
        self.assertTrue(hasattr(iter(t), '__next__'), "__iter__ must either produce a generator or an iterator")
        for i in t:
            if i[0] != tuple('color'):
                self.assertIn(i, c.items())
            else:
                self.assertEqual('silver', i[1])

        t = lab.Trie()
        t[(7, 8, 9)] = 1
        t[(7, 8, 9, 'hello')] = 1
        t[(7, 8, 9, 'hello', (1, 2))] = 1
        t[(1, )] = 1
        t[(7, )] = 1
        t[(7, 8, 9)] = 2
        t[(-1, -2, -3)] = 2
        t[(2, )] = 3
        self.assertTrue(hasattr(iter(t), '__next__'), "__iter__ must either produce a generator or an iterator")
        l = sorted(list(t))
        expected = [((-1, -2, -3), 2), ((1,), 1), ((2,), 3), ((7,), 1),
                    ((7, 8, 9), 2), ((7, 8, 9, 'hello'), 1), ((7, 8, 9, 'hello', (1, 2)), 1)]
        self.assertEqual(expected, l)
        del t[(7, 8, 9)]
        self.assertTrue(hasattr(iter(t), '__next__'), "__iter__ must either produce a generator or an iterator")
        l = sorted(list(t))
        expected = [((-1, -2, -3), 2), ((1,), 1), ((2,), 3), ((7,), 1),
                    ((7, 8, 9, 'hello'), 1), ((7, 8, 9, 'hello', (1, 2)), 1)]
        self.assertEqual(expected, l)


class Test_3_Corpora(unittest.TestCase):
    def test_01_word_trie(self):
        # small test
        l = lab.make_word_trie('toonces was a cat who could drive a car very fast until he crashed.')
        expected = read_expected('6.pickle')
        self.assertEqual(expected, dictify(l))

        l = lab.make_word_trie('a man at the market murmered that he had met a mermaid. '
                               'mark didnt believe the man had met a mermaid.')
        expected = read_expected('7.pickle')
        self.assertEqual(expected, dictify(l))

        l = lab.make_word_trie('what happened to the cat who had eaten the ball of yarn?  she had mittens!')
        expected = read_expected('8.pickle')
        self.assertEqual(expected, dictify(l))


    def test_02_phrase_trie(self):
        # small test
        l = lab.make_phrase_trie('toonces was a cat who could drive a car very fast until he crashed.')
        expected = read_expected('9.pickle')
        self.assertEqual(expected, dictify(l))

        l = lab.make_phrase_trie('a man at the market murmered that he had met a mermaid. '
                                 'i dont believe that he had met a mermaid.')
        expected = read_expected('10.pickle')
        self.assertEqual(expected, dictify(l))

        l = lab.make_phrase_trie(('What happened to the cat who ate the ball of yarn?  She had mittens!  '
                                   'What happened to the frog who was double parked?  He got toad!  '
                                   'What happened yesterday?  I dont remember.'))
        expected = read_expected('11.pickle')
        self.assertEqual(expected, dictify(l))


    def test_03_big_corpora(self):
        for bigtext in ('holmes', 'earnest', 'frankenstein'):
            with open(os.path.join(TEST_DIRECTORY, 'resources', 'testing_data', '%s.txt' % bigtext), encoding='utf-8') as f:
                text = f.read()
                w = lab.make_word_trie(text)
                p = lab.make_phrase_trie(text)

                w_e = read_expected('%s_words.pickle' % bigtext)
                p_e = read_expected('%s_phrases.pickle' % bigtext)

                self.assertEqual(w_e, dictify(w), 'word trie does not match for '+bigtext)
                self.assertEqual(p_e, dictify(p), 'phrase trie does not match for '+bigtext)


class Test_4_AutoComplete(unittest.TestCase):
    def test_01_autocomplete(self):
        # Autocomplete on simple trie with less than N valid words
        trie = lab.make_word_trie("cat car carpet")
        result = lab.autocomplete(trie, 'car', 3)
        self.assertIsInstance(result,list,"result not a list.")
        for w in result:
            self.assertIsInstance(w,str,"expecting list of strings.")
        result.sort()
        expect = ["car", "carpet"]
        self.assertEqual(expect,result,msg="incorrect result from autocomplete.")

        trie = lab.make_word_trie("a an ant anteater a an ant a")
        result = lab.autocomplete(trie, 'a', 2)
        self.assertIsInstance(result,list,"result not a list.")
        for w in result:
            self.assertIsInstance(w,str,"expecting list of strings.")
        result.sort()
        expect_one_of = [["a","an"],["a","ant"]]
        self.assertIn(result,expect_one_of,msg="incorrect result from autocomplete.")

        trie = lab.make_word_trie("man mat mattress map me met a man a a a map man met")
        result = lab.autocomplete(trie, 'm', 3)
        self.assertIsInstance(result,list,"result not a list.")
        for w in result:
            self.assertIsInstance(w,str,"expecting list of strings.")
        result.sort()
        expect = ["man","map","met"]
        self.assertEqual(expect,result,msg="incorrect result from autocomplete.")

        trie = lab.make_word_trie("hello hell history")
        result = lab.autocomplete(trie, 'help', 3)
        self.assertIsInstance(result,list,"result not a list.")
        for w in result:
            self.assertIsInstance(w,str,"expecting list of strings.")
        expect = []
        self.assertEqual(expect,result,msg="incorrect result from autocomplete.")
        with self.assertRaises(TypeError):
            result = lab.autocomplete(trie, ('tuple', ), None)

    def test_02_big_autocomplete_1(self):
        alphabet = a = "abcdefghijklmnopqrstuvwxyz"

        word_list = ["aa" + l1 + l2 + l3 + l4 for l1 in a for l2 in a for l3 in a for l4 in a]
        word_list.extend(["apple", "application", "apple", "apricot", "apricot", "apple"])
        word_list.append("bruteforceisbad")

        trie = lab.make_word_trie(' '.join(word_list))
        for i in range(10):
            result1 = lab.autocomplete(trie, 'ap', 1)
            result2 = lab.autocomplete(trie, 'ap', 2)
            result3 = lab.autocomplete(trie, 'ap', 3)
            result4 = lab.autocomplete(trie, 'ap')

            self.assertEqual(1, len(result1))
            self.assertEqual(2, len(result2))
            self.assertEqual(3, len(result3))
            self.assertEqual(3, len(result4))
            self.assertEqual(["apple"], result1)
            self.assertEqual(set(["apple", "apricot"]), set(result2))
            self.assertEqual(set(["apple", "apricot", "application"]), set(result3))
            self.assertEqual(set(result4), set(result3))

    def test_03_big_autocomplete_2(self):
        nums = {'t': [0, 1, 25, None],
                'th': [0, 1, 21, None],
                'the': [0, 5, 21, None],
                'thes': [0, 1, 21, None]}
        with open(os.path.join(TEST_DIRECTORY, 'resources', 'testing_data', 'frankenstein.txt'), encoding='utf-8') as f:
            text = f.read()
        w = lab.make_word_trie(text)
        for i in sorted(nums):
            for n in nums[i]:
                result = lab.autocomplete(w, i, n)
                expected = read_expected('frank_autocomplete_%s_%s.pickle' % (i, n))
                self.assertEqual(len(expected), len(result), msg=('missing' if len(result) < len(expected)\
                    else 'too many') + ' autocomplete results for ' + repr(i) + ' with maxcount = ' + str(n))
                self.assertEqual(set(expected), set(result), msg='autocomplete included ' + repr(set(result) - set(expected))\
                    + ' instead of ' + repr(set(expected) - set(result)) + ' for ' + repr(i) + ' with maxcount = '+str(n))
        with self.assertRaises(TypeError):
            result = lab.autocomplete(w, ('tuple', ), None)

    def test_04_big_autocomplete_3(self):
        with open(os.path.join(TEST_DIRECTORY, 'resources', 'testing_data', 'frankenstein.txt'), encoding='utf-8') as f:
            text = f.read()
        w = lab.make_word_trie(text)
        the_word = 'accompany'
        for ix in range(len(the_word)+1):
            test = the_word[:ix]
            result = lab.autocomplete(w, test)
            expected = read_expected('frank_autocomplete_%s_%s.pickle' % (test, None))
            self.assertEqual(len(expected), len(result), msg=('missing' if len(result) < len(expected)\
                else 'too many') + ' autocomplete results for ' + repr(test) + ' with maxcount = None')
            self.assertEqual(set(expected), set(result), msg='autocomplete included ' + repr(set(result) - set(expected))\
                + ' instead of ' + repr(set(expected) - set(result)) + ' for ' + repr(test) + ' with maxcount = None')
        with self.assertRaises(TypeError):
            result = lab.autocomplete(w, ('tuple', ), None)


    def test_05_big_phrase_autocomplete(self):
        nums = {('i', ): [0, 1, 2, 5, 11, None],
                ('i', 'do'): [0, 1, 2, 5, 8, None],
                ('i', 'do', 'not', 'like', 'them'): [0, 1, 2, 4, 100, None],
                ('i', 'do', 'not', 'like', 'them', 'here'): [0, 1, 2, 100, None]}
        with open(os.path.join(TEST_DIRECTORY, 'resources', 'testing_data', 'seuss.txt'), encoding='utf-8') as f:
            text = f.read()
        p = lab.make_phrase_trie(text)
        for i in sorted(nums):
            for n in nums[i]:
                result = lab.autocomplete(p, i, n)
                expected = read_expected('seuss_autocomplete_%s_%s.pickle' % (len(i), n))
                self.assertEqual(len(expected), len(result), msg=('missing' if len(result) < len(expected)\
                    else 'too many') + ' autocomplete results for ' + repr(i) + ' with maxcount = ' + str(n))
                self.assertEqual(set(expected), set(result), msg='autocomplete included ' + repr(set(result) - set(expected))\
                    + ' instead of ' + repr(set(expected) - set(result)) + ' for ' + repr(i) + ' with maxcount = '+str(n))

        with self.assertRaises(TypeError):
            result = lab.autocomplete(p, 'string', None)


class Test_5_AutoCorrect(unittest.TestCase):
    def test_01_autocorrect(self):
        # Autocorrect on cat in small corpus
        trie = lab.make_word_trie("cats cattle hat car act at chat crate act car act")
        result = lab.autocorrect(trie, 'cat',4)
        self.assertIsInstance(result,list,"result not a list.")
        for w in result:
            self.assertIsInstance(w,str,"expecting list of strings.")
        result.sort()
        expect = ["act", "car", "cats", "cattle"]
        self.assertEqual(expect,result,msg="incorrect result from autocorrect.")

    def test_02_big_autocorrect(self):
        nums = {'thin': [0, 8, 10, None],
                'tom': [0, 2, 4, None],
                'mon': [0, 2, 15, 17, 20, None]}
        with open(os.path.join(TEST_DIRECTORY, 'resources', 'testing_data', 'frankenstein.txt'), encoding='utf-8') as f:
            text = f.read()
        w = lab.make_word_trie(text)
        for i in sorted(nums):
            for n in nums[i]:
                result = lab.autocorrect(w, i, n)
                expected = read_expected('frank_autocorrect_%s_%s.pickle' % (i, n))
                self.assertEqual(len(expected), len(result), msg=('missing' if len(result) < len(expected)\
                    else 'too many') + ' autocorrect results for ' + repr(i) + ' with maxcount = ' + str(n))
                self.assertEqual(set(expected), set(result), msg='autocorrect included ' + repr(set(result) - set(expected))\
                    + ' instead of ' + repr(set(expected) - set(result)) + ' for ' + repr(i) + ' with maxcount = '+str(n))


class Test_6_Filter(unittest.TestCase):
    def test_01_filter(self):
        # Filter to select all words in trie
        trie = lab.make_word_trie("man mat mattress map me met a man a a a map man met")
        result = lab.word_filter(trie, '*')
        self.assertIsInstance(result,list,"result not a list.")
        result.sort()
        expect = [("a", 4), ("man", 3), ("map", 2), ("mat", 1), ("mattress", 1), ("me", 1), ("met", 2)]
        self.assertEqual(expect,result,msg="incorrect result from filter.")

        # All three-letter words in trie
        result = lab.word_filter(trie, '???')
        self.assertIsInstance(result,list,"result not a list.")
        result.sort()
        expect = [("man", 3), ("map", 2), ("mat", 1), ("met", 2)]
        self.assertEqual(expect,result,msg="incorrect result from filter.")

        # Words beginning with 'mat'
        result = lab.word_filter(trie, 'mat*')
        self.assertIsInstance(result,list,"result not a list.")
        result.sort()
        expect = [("mat", 1), ("mattress", 1)]
        self.assertEqual(expect,result,msg="incorrect result from filter.")

        # Words beginning with 'm', third letter is t
        result = lab.word_filter(trie, 'm?t*')
        self.assertIsInstance(result,list,"result not a list.")
        result.sort()
        expect = [("mat", 1), ("mattress", 1), ("met", 2)]
        self.assertEqual(expect,result,msg="incorrect result from filter.")

        # Words with at least 4 letters
        result = lab.word_filter(trie, '*????')
        self.assertIsInstance(result,list,"result not a list.")
        result.sort()
        expect = [("mattress", 1)]
        self.assertEqual(expect,result,msg="incorrect result from filter.")

        # All words
        result = lab.word_filter(trie, '**')
        self.assertIsInstance(result,list,"result not a list.")
        result.sort()
        expect = [("a", 4), ("man", 3), ("map", 2), ("mat", 1), ("mattress", 1), ("me", 1), ("met", 2)]
        self.assertEqual(expect,result,msg="incorrect result from filter.")


    def test_02_big_filter_1(self):
        alphabet = a = "abcdefghijklmnopqrstuvwxyz"

        word_list = ["aa" + l1 + l2 + l3 + l4 for l1 in a for l2 in a for l3 in a for l4 in a]
        word_list.extend(["apple", "application", "apple", "apricot", "apricot", "apple"])
        word_list.append("bruteforceisbad")

        trie = lab.make_word_trie(' '.join(word_list))
        for i in range(20):
            result = lab.word_filter(trie, "ap*")
            expected = [('apple', 3), ('apricot', 2), ('application', 1)]
            self.assertEqual(len(expected), len(result), msg='incorrect word_filter of ap*')
            self.assertEqual(set(expected), set(result), msg='incorrect word_filter of ap*')

    def test_03_big_filter_2(self):
        patterns = ('*ing', '*ing?', '****ing', '**ing**', '????', 'mon*',
                    '*?*?*?*', '*???')
        with open(os.path.join(TEST_DIRECTORY, 'resources', 'testing_data', 'frankenstein.txt'), encoding='utf-8') as f:
            text = f.read()
        w = lab.make_word_trie(text)
        for ix, i in enumerate(patterns):
            result = lab.word_filter(w, i)
            expected = read_expected('frank_filter_%s.pickle' % (ix, ))
            self.assertEqual(len(expected), len(result), msg='incorrect word_filter of '+repr(i))
            self.assertEqual(set(expected), set(result), msg='incorrect word_filter of '+repr(i))


if __name__ == '__main__':
    res = unittest.main(verbosity=3, exit=False)
