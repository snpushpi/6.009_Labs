#!/usr/bin/env python3

import lab
import unittest
import pickle
import os.path
import sys

sys.setrecursionlimit(5000)

TEST_DIRECTORY = os.path.dirname(__file__)

ERROR_THRESHOLD = 1e-5

def loadData(fileName):
    data = []
    with open(os.path.join(TEST_DIRECTORY, 'resources', 'testing_data', fileName), 'rb') as file:
        while True:
            try:
                data.append(pickle.load(file))
            except EOFError:
                break
    return data

def sorting_func(value):
    return repr(value)

def sorted_dictionary(dictionary):
    keys = sorted(list(dictionary), key = sorting_func)
    result = '{'
    for key in keys:
        result += repr(key) + ': ' + repr(dictionary[key]) +', '
    return result[:-2] + '}'

class Test_1_SolveLinear(unittest.TestCase):
    def validateEqual(self, expected, returned):
        self.assertEqual(type(expected), type(returned),                             \
                f"\nYour solution returned an instance of type: {type(returned)} "   \
                f"whereas we expect an instance of type: {type(expected)}.")
        
        self.assertEqual(len(expected), len(returned),                                                  \
                "\nYour solution doesn't have the correct number of variables."                         \
                f"\nYour solution has variables: \n{sorted(list(returned), key = sorting_func)}"        \
                f"\n whereas it should have variables: \n{sorted(list(expected), key = sorting_func)}")
        
        self.assertEqual(expected.keys(), returned.keys(),                                              \
                "\nYour solution has an incorrect set of variables.\nYour "                             \
                f"solution has variables: \n{sorted(list(returned.keys()), key = sorting_func)}"        \
                f"\n whereas it should have variables: \n{sorted(list(expected.keys()), key = sorting_func)}")

        try:
            maxDifference = max([abs(expected[variable] - returned[variable]) for variable in expected])
        except:
            self.assertTrue(False, f"Your solution produces:\n{returned}\n which contains non numeric values.")

        if maxDifference > ERROR_THRESHOLD:
            self.assertTrue(False, "Your solution differs from the correct "                       \
                    f"solution by more than the specified error threshold of {ERROR_THRESHOLD}.\n" \
                    "The maximum difference between the correct and returned "                     \
                    f"value of a variable was {maxDifference}.\nIf this difference is relatively " \
                    "small, you might be facing precision issues.\nYour solution "                 \
                    f"produced the output: \n{sorted_dictionary(returned)}"                        \
                    f"\nwhereas the correct solution is: \n{sorted_dictionary(expected)}")

    def loadAndRun(self, file):
        num = 0
        print()
        for testCase in loadData('SolveLinear_' + file + '.pickle'):
            num += 1
            print("Running sub-test", num)
            sub = lab.solveLinear(testCase['variables'], testCase['equations'])
            self.validateEqual(testCase['soln'], sub)
            
    def test_01(self):
        """ Single variable, single equation with constant. """
        #self.loadAndRun("SingleVariable")
        variables = {'x'}
        equations = [{1: 2, 'x': 1}]
        soln = {'x': -2}
        sub = lab.solveLinear(variables, equations)
        self.validateEqual(soln, sub)

    def test_02(self):
        """ Simple 2 variable system. """
        #self.loadAndRun("TwoVariables")
        variables = {('x', 1), ('y', 2)}
        equations = [{('x', 1): 1, ('y', 2): 1, 1: -3},
                     {('x', 1): 1, ('y', 2): -1, 1: 1}]
        soln = {('x', 1): 1.0, ('y', 2): 2.0}
        sub = lab.solveLinear(variables, equations)
        self.validateEqual(soln, sub)
        
    def test_03(self):
        """ Multiple variables and equations. """
        #self.loadAndRun("FourVariables")
        variables = {'x', 'y', 'z', 'w'}
        equations = [{'w': 3,'x': 2, 'y': 2, 'z': -6, 1: 32},
                     {'w': 2,'x': -1, 'y': 5, 'z': 1, 1: 3},
                     {'w': 1,'x': 3, 'y': 3, 'z': -1, 1: 47},
                     {'w': 5,'x': -2, 'y': -3, 'z': 3, 1: -49}]
        soln = {'w': 2.0, 'x': -12.0, 'y': -4.0, 'z': 1.0}
        sub = lab.solveLinear(variables, equations)
        self.validateEqual(soln, sub)

    def test_04(self):
        """ Multiple variables with sparse equations. """
        #self.loadAndRun("SparseVariables")
        variables = {'x', 'y'}
        equations = [{'x': 1, 'y': 1, 1: 1}, {'x': 0, 'y': 2}]
        soln = {'x': -1.0, 'y': 0.0}
        sub = lab.solveLinear(variables, equations)
        self.validateEqual(soln, sub) 
        
        variables = {'x', 'y', 'z', 'w'}
        equations = [{'w': 2, 'x': 3, 1: -5},
                     {'y': 4, 'z': 7, 1: -5},
                     {'w': 1, 'y': -1},
                     {'w': 4, 'z': 2, 1: -6}]
        soln = {'w': 1.6, 'x': 0.6, 'y': 1.6, 'z': -0.2}
        sub = lab.solveLinear(variables, equations)
        self.validateEqual(soln, sub)       

    def test_05(self):
        """ Moderately big system. """
        #self.loadAndRun("Moderate")
        variables = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'}
        equations = [{'a': 1, 'b': 2, 'e': 3, 1: -2},
                     {'b': 2, 'e': 4, 'd': 6, 'h': 4, 1: -8},
                     {'a': -1, 'c': 5, 'd': -4, 1: 2},
                     {'b': 2, 'd': -2, 'f': 3, 1: 10},
                     {'e': -1, 'g': 3, 1: 8},
                     {'a': 2, 'd': 3, 'h': -1, 1: -18},
                     {'b': -3, 'c': 2, 'f': 1, 1: 2},
                     {'c': 1, 'd': 2, 'e': -1, 1: -12}]
        soln = {'a': 1.0, 'b': 2.0, 'c': 3.0, 'd': 4.0,
                'e': -1.0, 'f': -2.0, 'g': -3.0, 'h': -4.0}
        sub = lab.solveLinear(variables, equations)
        self.validateEqual(soln, sub)
        
    def test_06(self):
        """ Chain test: Equations with the substitution forming a chain. """
        #self.loadAndRun('Chain')
        variables = {'x_0', 'x_1', 'x_2'}
        equations = [{'x_0': 1, 'x_1': 1, 'x_2': 1, 1: 605.6501525259827},
                     {'x_0': -1, 'x_1': 1, 1: -624.7011143847456},
                     {'x_0': 1, 'x_2': -1, 1: -504.7742434222988}]
        soln = {'x_0': -241.85900782947647, 'x_1': 382.8421065552691,
                'x_2': -746.6332512517753}
        sub = lab.solveLinear(variables, equations)
        self.validateEqual(soln, sub)
        
        variables = {'x_0', 'x_1', 'x_2', 'x_3', 'x_4'}
        equations = [{'x_0': 1, 'x_1': 1, 'x_2': 1, 'x_3': 1,
                      'x_4': 1, 1: -813.4395352127917},
                     {'x_1': 1, 'x_4': -1, 1: 326.41732529672777},
                     {'x_3': -1, 'x_4': 1, 1: 568.8808193175969},
                     {'x_0': -1, 'x_3': 1, 1: -1412.1723541148942},
                     {'x_0': 1, 'x_2': -1, 1: 1067.871995258968}]
        soln = {'x_0': -605.3541116917875, 'x_1': -88.47990219121789,
                'x_2': 462.51788356718043, 'x_3': 806.8182424231068,
                'x_4': 237.93742310550988}
        sub = lab.solveLinear(variables, equations)
        self.validateEqual(soln, sub)
        
        variables = {'x_0', 'x_1', 'x_2', 'x_3', 'x_4', 'x_5', 'x_6', 'x_7',
                     'x_8', 'x_9'}
        equations = [{'x_0': 1, 'x_1': 1, 'x_2': 1, 'x_3': 1, 'x_4': 1,
                      'x_5': 1, 'x_6': 1, 'x_7': 1, 'x_8': 1, 'x_9': 1,
                      1: -1940.8341367024948},
                     {'x_0': 1, 'x_2': -1, 1: -461.45058177597764},
                     {'x_2': 1, 'x_5': -1, 1: -513.5225887753505},
                     {'x_5': 1, 'x_7': -1, 1: 515.0777658363475},
                     {'x_4': -1, 'x_7': 1, 1: -669.9402141522244},
                     {'x_4': 1, 'x_9': -1, 1: 1642.537172193359},
                     {'x_8': -1, 'x_9': 1, 1: -506.0479494085198},
                     {'x_1': -1, 'x_8': 1, 1: -212.78696755169676},
                     {'x_1': 1, 'x_3': -1, 1: 664.3367796183902},
                     {'x_3': 1, 'x_6': -1, 1: -471.39377453506677}]
        soln = {'x_0': 420.87540615686726, 'x_1': 214.7420425228047,
                'x_2': -40.57517561911038, 'x_3': 879.0788221411949,
                'x_4': -708.9602127103378, 'x_5': -554.0977643944609,
                'x_6': 407.68504760612814, 'x_7': -39.01999855811346,
                'x_8': 427.52901007450146, 'x_9': 933.5769594830213}
        sub = lab.solveLinear(variables, equations)
        self.validateEqual(soln, sub)

    def test_07(self):
        """ Precision test: If you fail this test, you might have precision issues from dividing by values close to 0. """
        #self.loadAndRun("PrecisionTestSmall")
        variables = {'x', 'y', 'z', 'w'}
        equations = [{'x': 1e-12, 'y': 1e-12, 'z': -25, 'w': 10, 1: -13},
                     {'x': -1, 'y': 1, 'z': -3, 'w': 10, 1: -1},
                     {'x': 7, 'y': 6, 'z': 6, 'w': 15, 1: 22},
                     {'x': 6, 'y': 7, 'z': 3, 'w': 20, 1: 10}] 
        soln = {'x': -7.184615384615717, 'y': 11.61538461538483,
                'z': -1.3999999999998238, 'w': -2.200000000000002}
        sub = lab.solveLinear(variables, equations)
        self.validateEqual(soln, sub)

        variables = {'x', 'y', 'z', 'w'}
        equations = [{'x': 6, 'y': 7, 'z': 3, 'w': 20, 1: 10},
                     {'x': 7, 'y': 6, 'z': 6, 'w': 15, 1: 22},
                     {'x': -1, 'y': 1, 'z': -3, 'w': 10, 1: -1},
                     {'x': 1e-12, 'y': 1e-12, 'z': -25, 'w': 10, 1: -13}]
        soln = {'x': -7.184615384615717, 'y': 11.61538461538483,
                'z': -1.3999999999998238, 'w': -2.200000000000002}
        sub = lab.solveLinear(variables, equations)
        self.validateEqual(soln, sub)

    def test_08(self):
        """ Precision test: Larger but slightly weaker."""
        self.loadAndRun('PrecisionTestBig')

    def test_09(self):
        """ Big test: Uniformly and randomly generated equations. """
        self.loadAndRun('BigUniformRandom')

    def test_10(self):
        """ Big test: Uniformly and randomly generated equations with relatively few non-zero coefficients. """
        self.loadAndRun('BigUniformRandomSparse')

    def test_11(self):
        """ Big test: Chains of substitutions with a lot of zero coefficients """
        self.loadAndRun('Chain_Big')

class Test_2_SolveCircuit(unittest.TestCase):
    def validateEqual(self, expected, returned):
        self.assertEqual(type(expected), type(returned),                           \
                f"\nYour solution returned an instance of type: {type(returned)} " \
                f"whereas we expect an instance of type: {type(expected)}.")
        
        self.assertEqual(len(expected), len(returned), f"\nYour solution doesn't " \
                f"have the correct number of wires.\nYour solution has wires:"     \
                f"\n{sorted(list(returned.keys()), key = sorting_func)}\n"         \
                f"whereas it should have wires: \n{sorted(list(expected.keys()), key = sorting_func)}")
        
        self.assertEqual(expected.keys(), returned.keys(),                         \
                f"\nYour solution has an incorrect set of wires.\nYour solution "  \
                f"has wires: \n{sorted(list(returned), key = sorting_func)}\n "    \
                f"whereas it should have wires: \n{sorted(list(expected), key = sorting_func)}")

        try:
            maxDifference = max([abs(expected[variable] - returned[variable]) for variable in expected])
        except:
            self.assertTrue(False, f"Your solution produces:\n{returned}\n which contains non numeric values.")

        if maxDifference > ERROR_THRESHOLD:
            self.assertTrue(False, "Your solution differs from the correct "                       \
                    f"solution by more than the specified error threshold of {ERROR_THRESHOLD}.\n" \
                    "The maximum difference between the correct and returned "                     \
                    f"value of a current was {maxDifference}.\nIf this difference is relatively "  \
                    "small, you might be facing precision issues.\nYour solution "                 \
                    f"produced the output: \n{sorted_dictionary(returned)}"                        \
                    f"\nwhereas the correct solution is: \n{sorted_dictionary(expected)}")

    def loadAndRun(self, file):
        num = 0
        print()
        for testCase in loadData('SolveCircuit_' + file + '.pickle'):
            num += 1
            print("Running sub-test", num)
            sub = lab.solveCircuit(testCase['junctions'], testCase['wires'], testCase['resistances'], testCase['voltages'])
            self.validateEqual(testCase['soln'], sub)
            
    def test_01(self):
        """ Series triangle """
        #self.loadAndRun('SeriesTriangle')
        junctions = {'A', 'B', 'C'}
        wires = {'0': ('A', 'B'), '1': ('B', 'C'), '2': ('C', 'A')}
        resistances = {'0': 0, '1': 2, '2': 3}
        voltages = {'0': 5, '1': 0, '2': 0}
        soln = {'0': 1, '1': 1, '2': 1}
        sub = lab.solveCircuit(junctions, wires, resistances, voltages)
        self.validateEqual(soln, sub)

    def test_02(self):
        """ Parallel with single battery """
        #self.loadAndRun('SingleBatteryParallel')
        junctions = {'A', 'B'}
        wires = {'0': ('A', 'B'), '1': ('A', 'B'), '2': ('A', 'B')}
        resistances = {'0': 2, '1': 4, '2': 4}
        voltages = {'0': 5, '1': 0, '2': 0}
        soln = {'0': 1.25, '1': -0.625, '2': -0.625}
        sub = lab.solveCircuit(junctions, wires, resistances, voltages)
        self.validateEqual(soln, sub)
        
    def test_03(self):
        """ Parallel with multiple batteries """
        #self.loadAndRun('MultiBatteryParallel')
        junctions = {'A', 'B'}
        wires = {'0': ('A', 'B'), '1': ('A', 'B'), '2': ('A', 'B')}
        resistances = {'0': 2, '1': 4, '2': 4}
        voltages = {'0': 6, '1': 12, '2': 16}
        soln = {'0': -2, '1': 0.5, '2': 1.5}
        sub = lab.solveCircuit(junctions, wires, resistances, voltages)
        self.validateEqual(soln, sub)

    def test_04(self):
        """ Wire sticking out of triangle """
        #self.loadAndRun('StrayWire')
        junctions = {'A', 'B', 'C', 'D'}
        wires = {'0': ('A', 'B'), '1': ('B', 'C'), '2': ('C', 'A'), '3': ('C', 'D')}
        resistances = {'0': 1.5, '1': 2.0, '2': 0, '3': 0}
        voltages = {'0': 30, '1': 20, '2': 20, '3': 1000000}
        soln = {'0': 20.0, '1': 20.0, '2': 20.0, '3': 0.0}
        sub = lab.solveCircuit(junctions, wires, resistances, voltages)
        self.validateEqual(soln, sub)

    def test_05(self):
        """ Short circuit """
        #self.loadAndRun('ShortCircuit')
        junctions = {'A', 'B'}
        wires = {'0': ('A', 'B'), '1': ('A', 'B'), '2': ('A', 'B'), '3': ('B', 'A')}
        resistances = {'0': 7, '1': 17.34348, '2': 420.6921, '3': 0}
        voltages = {'0': 21, '1': 0, '2': 0, '3': 0}
        soln = {'0': 3.0, '1': 0.0, '2': 0.0, '3': 3.0}
        sub = lab.solveCircuit(junctions, wires, resistances, voltages)
        self.validateEqual(soln, sub)

    def test_06(self):
        """ Cube """
        #self.loadAndRun('Cube')
        junctions = {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'}
        wires = {('B', 'F'): ('B', 'F'), ('A', 'B'): ('A', 'B'),
                 ('B', 'C'): ('B', 'C'), ('E', 'F'): ('E', 'F'),
                 ('D', 'H'): ('D', 'H'), ('G', 'H'): ('G', 'H'),
                 ('C', 'D'): ('C', 'D'), ('D', 'A'): ('D', 'A'),
                 ('H', 'E'): ('H', 'E'), ('C', 'G'): ('C', 'G'),
                 ('F', 'G'): ('F', 'G'), ('A', 'E'): ('A', 'E'),
                 'battery': ('A', 'G')}
        resistances = {('B', 'F'): 30, ('A', 'B'): 30, ('B', 'C'): 30,
                       ('E', 'F'): 30, ('D', 'H'): 30, ('G', 'H'): 30,
                       ('C', 'D'): 30, ('D', 'A'): 30, ('H', 'E'): 30,
                       ('C', 'G'): 30, ('F', 'G'): 30, ('A', 'E'): 30,
                       'battery': 0}
        voltages = {('B', 'F'): 0, ('A', 'B'): 0, ('B', 'C'): 0,
                    ('E', 'F'): 0, ('D', 'H'): 0, ('G', 'H'): 0,
                    ('C', 'D'): 0, ('D', 'A'): 0, ('H', 'E'): 0,
                    ('C', 'G'): 0, ('F', 'G'): 0, ('A', 'E'): 0,
                    'battery': -300}
        soln = {('A', 'B'): 4.0, ('B', 'C'): 2.0, ('C', 'D'): -2.0, ('D', 'A'): -4.0,
                ('E', 'F'): 2.0, ('F', 'G'): 4.0, ('G', 'H'): -4.0, ('H', 'E'): -2.0,
                ('A', 'E'): 4.0, ('B', 'F'): 2.0, ('C', 'G'): 4.0, ('D', 'H'): 2.0,
                'battery': -12.0}
        sub = lab.solveCircuit(junctions, wires, resistances, voltages)
        self.validateEqual(soln, sub)
        
        junctions = {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'}
        wires = {('D', 'H'): ('D', 'H'), ('A', 'E'): ('A', 'E'),
                 ('C', 'D'): ('C', 'D'), ('E', 'F'): ('E', 'F'),
                 ('G', 'H'): ('G', 'H'), ('B', 'F'): ('B', 'F'),
                 ('C', 'G'): ('C', 'G'), ('F', 'G'): ('F', 'G'),
                 ('H', 'E'): ('H', 'E'), ('B', 'C'): ('B', 'C'),
                 ('D', 'A'): ('D', 'A'), ('A', 'B'): ('A', 'B'),
                 'battery': ('A', 'G')}
        resistances = {('D', 'H'): 60, ('A', 'E'): 9, ('C', 'D'): 60, ('E', 'F'): 60,
                       ('G', 'H'): 36, ('B', 'F'): 60, ('C', 'G'): 36, ('F', 'G'): 36,
                       ('H', 'E'): 60, ('B', 'C'): 60, ('D', 'A'): 9, ('A', 'B'): 9,
                       'battery': 0}
        voltages = {('D', 'H'): 0, ('A', 'E'): 0, ('C', 'D'): 0, ('E', 'F'): 0,
                    ('G', 'H'): 0, ('B', 'F'): 0, ('C', 'G'): 0, ('F', 'G'): 0,
                    ('H', 'E'): 0, ('B', 'C'): 0, ('D', 'A'): 0, ('A', 'B'): 0,
                    'battery': -300}
        soln = {('A', 'B'): 4.0, ('B', 'C'): 2.0, ('C', 'D'): -2.0, ('D', 'A'): -4.0,
                ('E', 'F'): 2.0, ('F', 'G'): 4.0, ('G', 'H'): -4.0, ('H', 'E'): -2.0,
                ('A', 'E'): 4.0, ('B', 'F'): 2.0, ('C', 'G'): 4.0, ('D', 'H'): 2.0,
                'battery': -12.0}
        sub = lab.solveCircuit(junctions, wires, resistances, voltages)
        self.validateEqual(soln, sub)

    def test_07(self):
        """ Balanced Wheatstone bridges """
        self.loadAndRun('Wheatstone')

    def test_08(self):
        """ Unbalanced Wheatstone bridge (star-delta)"""
        self.loadAndRun('UnbalancedWheatstone')

    def test_09(self):
        """ Ladder """
        self.loadAndRun('Ladder')

    def test_10(self):
        """ Big Tests """
        print()
        print('Long Series', end = '')
        self.loadAndRun('LongSeries')
        print('Wide Parallel', end = '')
        self.loadAndRun('WideParallel')
        print('Ladder', end = '')
        self.loadAndRun('Ladder_Big')
        print('Wheatstone Bridge', end = '')
        self.loadAndRun('Wheatstone_Big')
        print('Unbalanced Wheatstone Bridge', end = '')
        self.loadAndRun('UnbalancedWheatstone_Big')
        print('Small Random Circuits', end = '')
        self.loadAndRun('SmallRandom')
        print('Big Random Circuits', end = '')
        self.loadAndRun('BigRandom')

    def test_11(self):
        """ Really Big Test: Based on a famous problem from I.E. Irodov: Problems in General Physics """
        self.loadAndRun('Irodov')

# Uncomment the following class definitions to test your implementations of findMaximumDeviationJunction and findMaximumDeviationLoop

"""
class Test_3_FindMaximumDeviationJunction(unittest.TestCase):
    def validateEqual(self, expected, junctions, returned):
        self.assertTrue(returned in junctions, f"\nYour solution produced {returned}, which is not a valid junction.")
        self.assertTrue(returned in expected, f"\nYour solution produced {returned}, which does not have the maximal deviation.")

    def loadAndRun(self, file):
        num = 0
        print()
        for testCase in loadData('FindMaximumDeviationJunction_' + file + '.pickle'):
            num += 1
            print("Running sub-test", num)
            sub = lab.findMaximumDeviationJunction(testCase['junctions'], testCase['wires'], testCase['resistances'], testCase['voltages'], testCase['currents'])
            self.validateEqual(testCase['soln'], testCase['junctions'], sub)

    def test_01(self):
        ''' Small tests '''
        self.loadAndRun('SmallTests')
        #Series triangle
        junctions = {'A', 'B', 'C'}
        wires = {'0': ('A', 'B'), '1': ('B', 'C'), '2': ('C', 'A')}
        resistances = {'0': 0, '1': 2, '2': 3}
        voltages = {'0': 5, '1': 0, '2': 0}
        currents = {'0': 1, '1': 2, '2': 1}
        soln = {'B', 'C'}
        sub = lab.findMaximumDeviationJunction(junctions, wires, resistances, voltages, currents)
        self.validateEqual(soln, junctions, sub)

        #Parallel
        junctions = {'A', 'B'}
        wires = {'0': ('A', 'B'), '1': ('A', 'B'), '2': ('A', 'B')}
        resistances = {'0': 2, '1': 4, '2': 4}
        voltages = {'0': 6, '1': 12, '2': 16}
        currents = {'0': -2, '1': 1, '2': 1}
        soln = {'A', 'B'}
        sub = lab.findMaximumDeviationJunction(junctions, wires, resistances, voltages, currents)
        self.validateEqual(soln, junctions, sub)

        #Wire sticking out of triangle
        junctions = {'A', 'B', 'C', 'D'}
        wires = {'0': ('A', 'B'), '1': ('B', 'C'), '2': ('C', 'A'), '3': ('C', 'D')}
        resistances = {'0': 1.5, '1': 2.0, '2': 0, '3': 0}
        voltages = {'0': 30, '1': 20, '2': 20, '3': 1000000}
        currents = {'0': 20, '1': 20.0005, '2': 20, '3': 0.001}
        soln = {'D'}
        sub = lab.findMaximumDeviationJunction(junctions, wires, resistances, voltages, currents)
        self.validateEqual(soln, junctions, sub)
        
        #Square with large deivation and single answer
        junctions = {'A', 'B', 'C', 'D'}
        wires = {'0': ('A', 'B'), '1': ('A', 'C'), '2': ('A', 'D'), '3': ('A', 'D'), '4': ('B', 'D'), '5': ('C', 'D')}
        resistances = {'0': 1, '1': -1, '2': 5, '3': 10, '4': 5, '5': 2}
        voltages = {'0': -1, '1': 1, '2': 2, '3': 1, '4': 4, '5': 15}
        currents = {'0': -1, '1': -1, '2': 10, '3': 10, '4': 20, '5': 30}
        soln = {'D'}
        sub = lab.findMaximumDeviationJunction(junctions, wires, resistances, voltages, currents)
        self.validateEqual(soln, junctions, sub)

        #Square with small deviations and single answer 
        junctions = {'A', 'B', 'C', 'D'}
        wires = {'0': ('A', 'C'), '1': ('C', 'D'), '2': ('D', 'B'), '3': ('B', 'A'), '4': ('C', 'B')}
        resistances = {'0': 2, '1': 1, '2': 1, '3': 2, '4': 1}
        voltages = {'0': 1, '1': 1, '2': 1, '3': 1, '4': 1}
        currents = {'0': 1.99, '1': 1, '2': 0.9, '3': 1.95, '4': 1}
        soln = {'D'}
        sub = lab.findMaximumDeviationJunction(junctions, wires, resistances, voltages, currents)
        self.validateEqual(soln, junctions, sub)

        #Square with no deviation - satisfies KCL and Ohm's Law
        junctions = {'A', 'B', 'C', 'D'}
        wires = {'0': ('A', 'C'), '1': ('C', 'D'), '2': ('D', 'B'), '3': ('B', 'A'), '4': ('C', 'B')}
        resistances = {'0': 2, '1': 1, '2': 2, '3': 1, '4': 1}
        voltages = {'0': 1, '1': 1, '2': 0.5, '3': 2, '4': 1}
        currents = {'0': 2, '1': 1, '2': 1, '3': 2, '4': 1}
        soln = {'A', 'B', 'C', 'D'}
        sub = lab.findMaximumDeviationJunction(junctions, wires, resistances, voltages, currents)
        self.validateEqual(soln, junctions, sub)

        #Square with no deviation - satisfies KCL but not Ohm's Law
        junctions = {'A', 'B', 'C', 'D'}
        wires = {'0': ('A', 'C'), '1': ('C', 'D'), '2': ('D', 'B'), '3': ('B', 'A'), '4': ('C', 'B')}
        resistances = {'0': 1, '1': 1, '2': 3, '3': 1, '4': 1}
        voltages = {'0': 1, '1': 1, '2': 1, '3': 2, '4': 1}
        currents = {'0': 2, '1': 1, '2': 1, '3': 2, '4': 1}
        soln = {'A', 'B', 'C', 'D'}
        sub = lab.findMaximumDeviationJunction(junctions, wires, resistances, voltages, currents)
        self.validateEqual(soln, junctions, sub)
        
    def test_02(self):
        ''' Medium tests '''
        self.loadAndRun('SmallRandom')

    def test_03(self):
        ''' Large tests '''
        self.loadAndRun('BigRandom')

class Test_4_FindMaximumDeviationLoop(unittest.TestCase):
    def validateEqual(self, wires, deviations, expectedDeviation, returned):
        self.assertEqual(type([]), type(returned), f"\nYour solution returned an instance of type: {type(returned)} whereas we expect an instance of type: {type([])}.")

        self.assertTrue(set(returned) <= set(wires), f"\nYour solution includes wire labels:\n{set(returned) - set(wires)}\nwhich are not given in the input.")

        self.assertTrue(len(returned) >= 2 and len(set(wires[returned[0]]) & set(wires[returned[1]])) >= 1, f"\nThe first two elements of your solution:\n{returned}\nare incorrect or incomplete.")
        
        currentJunction = list(set(wires[returned[0]]) & set(wires[returned[1]]))[0]
        deviation = 0.0
        visited = {currentJunction}
        
        if wires[returned[0]][1] == currentJunction:
            startingJunction = wires[returned[0]][0]
            deviation += deviations[returned[0]]
        else:
            startingJunction = wires[returned[0]][1]
            deviation -= deviations[returned[0]]
            
        for wire in returned[1:]:
            if currentJunction == wires[wire][0]:
                currentJunction = wires[wire][1]
                deviation += deviations[wire]
            elif currentJunction == wires[wire][1]:
                currentJunction = wires[wire][0]
                deviation -= deviations[wire]
            else:
                self.assertTrue(False, f"\nYour solution:\n{returned}\n is not a cycle. The edge {wires[wire]} is not adjacent to {currentJunction}")
            visited.add(currentJunction)

        self.assertEqual(len(returned), len(visited), f"\nYour solution:\n{returned}\nis not a simple cycle. Make sure that you do not have duplicates.")

        self.assertEqual(currentJunction, startingJunction, f"\nYour solution:\n{returned}\nis a path, not a cycle.")

        self.assertLess(expectedDeviation - 1e-8, abs(deviation), f"\nYour solution produced a deviation of {abs(deviation)}, but the best value is {expectedDeviation}")

    def loadAndRun(self, file):
        num = 0
        print()
        for testCase in loadData('FindMaximumDeviationLoop_' + file + '.pickle'):
            num += 1
            print("Running sub-test", num)
            sub = lab.findMaximumDeviationLoop(testCase['junctions'], testCase['wires'], testCase['resistances'], testCase['voltages'], testCase['currents'])
            self.validateEqual(testCase['wires'], testCase['deviations'], testCase['soln'], sub)
            
    def test_01(self):
        ''' Series triangle '''
        #self.loadAndRun('SeriesTriangle')
        #Correct currents
        junctions = {'A', 'B', 'C'}
        wires = {'0': ('A', 'B'), '1': ('B', 'C'), '2': ('C', 'A')}
        resistances = {'0': 0, '1': 2, '2': 3}
        voltages = {'0': 5, '1': 0, '2': 0}
        currents = {'0': 1, '1': 1, '2': 1}
        deviations = {'0': 0, '1': 0, '2': 0}
        soln = 0.0
        sub = lab.findMaximumDeviationLoop(junctions, wires, resistances, voltages, currents)
        self.validateEqual(wires, deviations, soln, sub)

        #Incorrect currents but no deviation
        junctions = {'A', 'B', 'C'}
        wires = {'0': ('A', 'B'), '1': ('B', 'C'), '2': ('C', 'A')}
        resistances = {'0': 0, '1': 2, '2': 3}
        voltages = {'0': 5, '1': 0, '2': 0}
        currents = {'0': 2, '1': 1, '2': 1}
        deviations = {'0': 0, '1': 0, '2': 0}
        soln = 0.0
        sub = lab.findMaximumDeviationLoop(junctions, wires, resistances, voltages, currents)
        self.validateEqual(wires, deviations, soln, sub)

        #Incorrect currents with deviation
        junctions = {'A', 'B', 'C'}
        wires = {'0': ('A', 'B'), '1': ('B', 'C'), '2': ('C', 'A')}
        resistances = {'0': 0, '1': 2, '2': 3}
        voltages = {'0': 5, '1': 0, '2': 0}
        currents = {'0': 1, '1': 2, '2': 1}
        deviations = {'0': 0, '1': -4, '2': 0}
        soln = 4.0
        sub = lab.findMaximumDeviationLoop(junctions, wires, resistances, voltages, currents)
        self.validateEqual(wires, deviations, soln, sub)
        
    def test_02(self):
        ''' Parallel '''
        #self.loadAndRun('Parallel')
        junctions = {'A', 'B'}
        wires = {'0': ('A', 'B'), '1': ('A', 'B'), '2': ('A', 'B')}
        resistances = {'0': 2, '1': 4, '2': 4}
        voltages = {'0': 6, '1': 12, '2': 16}
        currents = {'0': -2, '1': 1, '2': 1}
        deviations = {'0': 10, '1': 8, '2': 12}
        soln = 4.0
        sub = lab.findMaximumDeviationLoop(junctions, wires, resistances, voltages, currents)
        self.validateEqual(wires, deviations, soln, sub)

        # Correct circuit
        junctions = {'A', 'B'}
        wires = {'0': ('A', 'B'), '1': ('A', 'B'), '2': ('A', 'B')}
        resistances = {'0': 2, '1': 4, '2': 4}
        voltages = {'0': 6, '1': 12, '2': 16}
        currents = {'0': -2, '1': 0.5, '2': 1.5}
        deviations = {'0': 0, '1': 8, '2': 0}
        soln = 0.0
        sub = lab.findMaximumDeviationLoop(junctions, wires, resistances, voltages, currents)
        self.validateEqual(wires, deviations, soln, sub)

    def test_03(self):
        ''' Square circuit '''
        #self.loadAndRun('Square')
        junctions = {'A', 'B', 'C', 'D'}
        wires = {'0': ('A', 'B'), '1': ('C','A'), '2': ('D', 'B'), '3': ('C', 'B'), '4': ('D', 'C'), '5': ('A', 'D')}
        resistances = {'0': 3, '1': 2, '2': 2, '3': 1, '4': 1, '5': 4}
        voltages = {'0': 5, '1': 0, '2': 15, '3': 0, '4': -2, '5': 0}
        currents = {'0': -1, '1': -1, '2': 10, '3': 10, '4': 20, '5': 20}
        deviations = {'0': 1.0, '1': 1.3333333333333333, '2': -5.666666666666667,
                      '3': -14.333333333333334, '4': -24.0, '5': -19.666666666666668}
        soln = 59.0
        sub = lab.findMaximumDeviationLoop(junctions, wires, resistances, voltages, currents)
        self.validateEqual(wires, deviations, soln, sub)

        # Correct circuit
        junctions = {'A', 'B', 'C', 'D'}
        wires = {'0': ('A', 'B'), '1': ('C','A'), '2': ('D', 'B'), '3': ('C', 'B'), '4': ('D', 'C'), '5': ('A', 'D')}
        resistances = {'0': 3, '1': 2, '2': 2, '3': 1, '4': 1, '5': 4}
        voltages = {'0': 5, '1': 0, '2': 15, '3': 0, '4': -2, '5': 0}
        currents = {'0': 0.0, '1': 0.3333333333333333, '2': -3.25, '3': -3.25, '4': -4, '5': 0.3333333333333333}
        deviations = {'0': 0, '1': 0, '2': 0, '3': 0, '4': 0, '5': 0}
        soln = 0.0
        sub = lab.findMaximumDeviationLoop(junctions, wires, resistances, voltages, currents)
        self.validateEqual(wires, deviations, soln, sub)

    def test_04(self):
        ''' Concept question circuit '''
        #self.loadAndRun('ConceptQuestion')
        junctions = {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'}
        wires = {'W1': ('H', 'A'), 'W2': ('A', 'B'), 'W3': ('B', 'C'),
                 'W4': ('C', 'D'), 'W5': ('D', 'E'), 'W6': ('E', 'F'),
                 'W7': ('F', 'G'), 'W8': ('G', 'H'), 'W9': ('B', 'I'),
                 'W10': ('H', 'I'), 'W11': ('D', 'I'), 'W12': ('F', 'I')}
        resistances = {'W1': 0, 'W2': 2, 'W3': 4, 'W4': 0, 'W5': 1, 'W6': 12,
                       'W7': 7, 'W8': 0, 'W9': 0, 'W10': 9, 'W11': 6, 'W12': 0}
        voltages = {'W1': 3, 'W2': 0, 'W3': 1, 'W4': 1, 'W5': -1, 'W6': 0,
                    'W7': 0, 'W8': 0, 'W9': 0, 'W10': 10, 'W11': 8, 'W12': -2}
        currents = {'W1': -0.25, 'W2': -0.25, 'W3': 0.5, 'W4': 0.25, 'W5': -0.25,
                    'W6': -0.5, 'W7': 1, 'W8': 1, 'W9': -1, 'W10': 0.75, 'W11': 1, 'W12': -1}
        deviations = {'W1': 3.0, 'W2': 0.5, 'W3': -1.0, 'W4': 1.0, 'W5': -0.75, 'W6': 6.0,
                      'W7': -7, 'W8': 0, 'W9': 0, 'W10': 3.25, 'W11': 2, 'W12': -2}
        soln = 3.5
        sub = lab.findMaximumDeviationLoop(junctions, wires, resistances, voltages, currents)
        self.validateEqual(wires, deviations, soln, sub)

    def test_05(self):
        ''' Long series '''
        self.loadAndRun('Series')

    def test_06(self):
        ''' Structured '''
        self.loadAndRun('Structured')

    def test_07(self):
        ''' Random '''
        self.loadAndRun('Random')
"""

if __name__ == '__main__':
    res = unittest.main(verbosity = 3, exit = False)
