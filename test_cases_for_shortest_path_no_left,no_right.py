
import lab
import unittest
import os.path
import sys
import json
from verifier import check_is_valid

sys.setrecursionlimit(5000)

def check_path_format(result):
    if result is None:
        return
    assert isinstance(result, list), "returned object is not a list!"
    for obj in result:
        assert isinstance(obj, dict), "element in the returned list is not a dictionary!"
        assert "start" in obj, "edge in list does not contain a start coordinate!"
        assert "start" in obj, "edge in list does not contain an end coordinate!"
        assert len(obj) == 2, "edge in list contains extra coordinates!"
        for k, i in obj.items(): 
            assert isinstance(i, tuple) and len(i) == 2, \
                "return coordinate is not a tuple of len two!"

def verify_path(result, input_data):
    check_path_format(result)
    d = input_data["inputs"]
    graph = d["graph"]
    start = d["start"]
    end = d["end"]
    if "k" in d.keys():
        num_left_turns = d["k"]
    else:
        num_left_turns = None
    func = input_data["function"]
    return check_is_valid(
        result,
        graph,
        start,
        end,
        num_left_turns,
        func,
    )

def copy_graph(graph):
    new_graph = []
    for edge in graph:
        new_graph.append(edge.copy())
    return new_graph

def convert_to_tuples(input_data):
    input_data['inputs']["start"] = tuple(input_data['inputs']["start"])
    input_data['inputs']["end"] = tuple(input_data['inputs']["end"])
    input_data['inputs']["graph"] = [{key:tuple(coord) for key, coord in edge.items()} for edge in input_data['inputs']["graph"]]

class Test_1_ShortestPath(unittest.TestCase):
    def validate(self, input_data, expected, actual):
        if actual is None:
            self.assertEqual(
                expected, 
                actual, 
                "did not find an existing valid path!",
            )
        elif expected is None:
            self.assertEqual(
                expected, 
                actual, 
                "a valid path does not exist!",
            )
        else:
            input_data["many_lefts"] = True
            ok, message = verify_path(actual, input_data)
            self.assertTrue(ok, message)
            self.assertEqual(
                len(actual), 
                expected, 
                "the length of the path is not as expected!",
            )

    def run_test(self, input_data):
        result = lab.shortest_path(
            copy_graph(input_data['inputs']["graph"]), 
            input_data['inputs']["start"], 
            input_data['inputs']["end"], 
        )
        return result

    def load(self, case):
        with open("cases/"+case+'.in', 'r') as f:
            input_data = json.loads(f.read())
        with open("cases/" + case + '.out', 'r') as f:
            output_data = json.loads(
                f.read().replace("\'", '"').replace("(", '[').replace(")", ']')
            )
        convert_to_tuples(input_data)
        return input_data, output_data

    def test_01(self):
        """Shortest path, small graph"""
        case = '1'
        input_data, output_data = self.load(case)
        result = self.run_test(input_data)
        self.validate(input_data, output_data, result)

    def test_02(self):
        """Shortest path, medium graph"""
        case = '2'
        input_data, output_data = self.load(case)
        result = self.run_test(input_data)
        self.validate(input_data, output_data, result)

    def test_03(self):
        """Shortest path, medium graph 2"""
        case = '3'
        input_data, output_data = self.load(case)
        result = self.run_test(input_data)
        self.validate(input_data, output_data, result)

    def test_04(self):
        """Shortest path, no valid path exists"""
        case = '4'
        input_data, output_data = self.load(case)
        result = self.run_test(input_data)
        self.validate(input_data, output_data, result)

    def test_05(self):
        """Shortest Path, large graph"""
        case = '5'
        input_data, output_data = self.load(case)
        result = self.run_test(input_data)
        self.validate(input_data, output_data, result)


class Test_2_NoLefts(unittest.TestCase):
    def validate(self, input_data, expected, actual):
        if actual is None:
            self.assertEqual(
                expected, 
                actual, 
                "did not find an existing valid path!",
            )
        elif expected is None:
            self.assertEqual(
                expected, 
                actual, 
                "a valid path does not exist!",
            )
        else:
            ok, message = verify_path(actual, input_data)
            self.assertTrue(ok, message)
            self.assertEqual(
                len(actual), 
                expected, 
                "the length of the path is not as expected!",
            )

    def run_test(self, input_data):
        result = lab.shortest_path_no_lefts(
            copy_graph(input_data['inputs']["graph"]), 
            input_data['inputs']["start"], 
            input_data['inputs']["end"], 
        )
        return result

    def load(self, case):
        with open("cases/"+case+'.in', 'r') as f:
            input_data = json.loads(f.read())
        with open("cases/" + case + '.out', 'r') as f:
            output_data = json.loads(
                f.read().replace("\'", '"').replace("(", '[').replace(")", ']')
            )
        convert_to_tuples(input_data)
        return input_data, output_data

    def test_06(self):
        """No left turns, multiple valid paths, small graph"""
        case = '6'
        input_data, output_data = self.load(case)
        result = self.run_test(input_data)
        self.validate(input_data, output_data, result)

    def test_07(self):
        """No left turns, no path exists, small graph"""
        case = '7'
        input_data, output_data = self.load(case)
        result = self.run_test(input_data)
        self.validate(input_data, output_data, result)

    def test_08(self):
        """No left turns, no path exists, small graph"""
        case = '8'
        input_data, output_data = self.load(case)
        result = self.run_test(input_data)
        self.validate(input_data, output_data, result)

    def test_09(self):
        """No left turns, medium graph"""
        case = '9'
        input_data, output_data = self.load(case)
        result = self.run_test(input_data)
        self.validate(input_data, output_data, result)

    def test_10(self):
        """No left turns, no path exists, medium graph"""
        case = '10'
        input_data, output_data = self.load(case)
        result = self.run_test(input_data)
        self.validate(input_data, output_data, result)

    def test_11(self):
        """No left turns, large graph"""
        case = '11'
        input_data, output_data = self.load(case)
        result = self.run_test(input_data)
        self.validate(input_data, output_data, result)

class Test_3_KLefts(unittest.TestCase):
    def validate(self, input_data, expected, actual):
        if actual is None:
            self.assertEqual(
                expected, 
                actual, 
                "did not find an existing valid path!",
            )
        elif expected is None:
            self.assertEqual(
                expected, 
                actual, 
                "a valid path does not exist!",
            )
        else:
            ok, message = verify_path(actual, input_data)
            self.assertTrue(ok, message)
            self.assertEqual(
                len(actual), 
                expected, 
                "the length of the path is not as expected!",
            )

    def run_test(self, input_data):
        result = lab.shortest_path_k_lefts(
            copy_graph(input_data['inputs']["graph"]), 
            input_data['inputs']["start"], 
            input_data['inputs']["end"], 
            input_data['inputs']["k"],
        )
        return result

    def load(self, case):
        with open("cases/"+case+'.in', 'r') as f:
            input_data = json.loads(f.read())
        with open("cases/" + case + '.out', 'r') as f:
            output_data = json.loads(
                f.read().replace("\'", '"').replace("(", '[').replace(")", ']')
            )
        convert_to_tuples(input_data)
        return input_data, output_data

    def test_12(self):
        """Multiple possible paths, medium graph"""
        case = '12'
        input_data, output_data = self.load(case)
        result = self.run_test(input_data)
        self.validate(input_data, output_data, result)

    def test_13(self):
        """2 valid paths of different lengths, medium graph"""
        case = '13'
        input_data, output_data = self.load(case)
        result = self.run_test(input_data)
        self.validate(input_data, output_data, result)

    def test_14(self):
        """No valid path, medium graph"""
        case = '14'
        input_data, output_data = self.load(case)
        result = self.run_test(input_data)
        self.validate(input_data, output_data, result)

    def test_15(self):
        """Multiple valid paths of different lengths, large graph"""
        case = '15'
        input_data, output_data = self.load(case)
        result = self.run_test(input_data)
        self.validate(input_data, output_data, result)

    def test_16(self):
        """Multiple valid paths of different lengths, large graph"""
        case = '16'
        input_data, output_data = self.load(case)
        result = self.run_test(input_data)
        self.validate(input_data, output_data, result)

    def test_17(self):
        """Small regular grid, lots of left turns"""
        case = '17'
        input_data, output_data = self.load(case)
        result = self.run_test(input_data)
        self.validate(input_data, output_data, result)


if __name__ == '__main__':
    res = unittest.main(verbosity = 3, exit = False)
