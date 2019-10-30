
# NO IMPORTS ALLOWED!

# Uncomment below and comment/rename the solveLinear defined in this file to
# use the sample solveLinear function.
# Remember to comment it out before submitting!

#from solve_linear_sample import solveLinear

def substituteEquation(equation, substitutedVariable, substitutionEquation):
    """
        Note that implementing this function is optional. You might want to
        consider implementing it to break up your code into more managable
        chunks.
        
        Given:
            equation: An equation represented by a dictionary that maps the
                      variables or 1 to its coefficient in the equation.
                      E.g. {1: 2, 'x': 2, 'y': 3} represents 2 + 2x + 3y = 0.
            substitutedVariable: The variable to be substituted out of the
                                 equation.
            substitutionEquation: The substitution equation represented as a
                                  dictionary.
        Return:
            finalEquation: A dictionary representing the resulting equation
                           after the substitution is performed. 
    """
    
    if substitutedVariable not in equation:
        return equation
    for element in substitutionEquation:
        
        if element in equation and element!= substitutedVariable:
            

            equation[element]= equation[element] - (equation[substitutedVariable]*substitutionEquation[element])/substitutionEquation[substitutedVariable]
            
            if equation[element] == 0:
                del equation[element]
        else:
            if element!= substitutedVariable:
                equation[element] = -(equation[substitutedVariable]*substitutionEquation[element])/substitutionEquation[substitutedVariable]
                if equation[element] == 0:
                    del equation[element]
        
    del equation[substitutedVariable]
    
    return equation


def solveLinear(variables, equations):
    """
        Given:
            variables: A set of strings or tuples representing the independent
                       variables. E.g. {'x', 'y', 'z'}
            equations: A list of linear equations where each equation is
                       represented as a dictionary. Each dictionary maps the
                       variables or 1 to its coefficient in the equation.
                       E.g. {1: 2, 'x': 2, 'y': 3} represents 2 + 2x + 3y = 0.
                       Note that all variables may not appear in all of the
                       equations. Moreover, you may assume that the equations
                       are independent.
        Return:
            result: A dictionary mapping each variable to the numerical value
            that solves the system of equations. Assume that there is exactly
            one solution. Some inaccuracy as typical from floating point
            computations will be acceptable.
    """
    # dealing with base case
    if len(equations) == 1:
        if len(equations[0])==1:
            for key in equations[0]:
                return {key:0}
        else:
            list1 = list(equations[0].keys())
            list1.remove(1)
            return { list1[0]: -(equations[0][1])/equations[0][list1[0]]}
    # deleting those keys which has value zero            
    for element in equations:
        selected_keys = []
        for e in element:
            if element[e] == 0:
                selected_keys.append(e)
        for key in selected_keys:
            if key in element:
                del element[key]
    #finding the equation with minimum length    
    minimum = len(equations[0])
    temp =0
    for i in range(len(equations)):
        if minimum > len(equations[i]):
            minimum = len(equations[i])
            temp = i
    #creating a dummy equation for finding the maximum value co-efficient 
    equations_dummy = {}
    for element in equations[temp]:
        if element!=1:
            equations_dummy[abs(equations[temp][element])] = element
    var = equations_dummy[max(equations_dummy.keys())]
    # now substitution in all equations except for one which was used for substitution   
    substitutedVariable = var
    substitutionEquation = equations[temp]
    for i in range(len(equations)):
        if i !=temp:
            equations[i] = substituteEquation(equations[i],substitutedVariable,substitutionEquation)
    equation = equations.pop(temp)
    #now resetting variables and equations, removing the substituted variable and removing one equation 
    variables.remove(var)
    #now doing recursive call and using the solutions for (n-1) solutions to get the value of variable which wa substituted 
    result_dictionary = solveLinear(variables, equations)
    summation = 0
    for element in equation:
        if element!= var and element!= 1:
        
            
            summation = equation[element]*result_dictionary[element]+summation
    summation += equation.get(1,0)
    
    result_dictionary[var] = -summation/ equation[var]
    
    return result_dictionary 
    

    
def solveCircuit(junctions, wires, resistances, voltages):
    """
        Given:
            junctions:  A set of junctions. Each junction is labeled by a string
                        or a tuple.
            wires:      A dictionary mapping a unique wire ID (a string or tuple)
                        to a tuple of two elements representing the starting and
                        ending junctions of the wire, respectively. The set of
                        wire IDs is disjoint from the set of junction labels.
                        Note that although electricity can flow in either
                        directions, each wire between a pair of junctions will
                        appear exactly once in the list. Moreover, the starting
                        and ending junctions are distinct.
            resistances:A dictionary mapping each unique wire ID to a numeric
                        value representing the magnitude of the resistance of
                        the wire in Ohms. This dictionary has the same set of
                        keys as the wires dictionary.
            voltages:   A dictionary mapping each unique wire ID to a numeric
                        value representing the voltage (EMF or potential
                        difference) of the battery connected along the wire in 
                        Volts. The positive terminal of the battery is next to
                        the ending junction (as defined in the wires dictionary)
                        if the voltage is positive whereas it is next to the 
                        starting junction otherwise. This dictionary also has
                        the same set of keys as the wires dictionary.
        Return:
            result: A dictionary mapping the label of each wire to the current
                    it carries. The labels must be the keys in the wires
                    dictionary and the current should be considered positive if
                    it is flowing from the starting junction to the ending
                    junction as specified in the wires dictionary.
    """
    #for all junnctions , creating a dictionary where the keys are the junctions and these keys are mapping to a list with two elements , first element is
    # a list of wire IDS entering that junction and another is a list with wire IDs getting out of that junction.
    dictionary = {}
    for e in wires:
        if type(e) == str:
            if wires[e][0] not in dictionary:
                dictionary[wires[e][0]] = [[],[]]
                dictionary[wires[e][0]][0].append(str(e))
            else:
                dictionary[wires[e][0]][0].append(str(e))
            if wires[e][1] not in dictionary:
                dictionary[wires[e][1]] = [[],[]]
                dictionary[wires[e][1]][1].append(str(e))
            else:
                dictionary[wires[e][1]][1].append(str(e))
        else:
            if wires[e][0] not in dictionary:
                dictionary[wires[e][0]] = [[],[]]
                dictionary[wires[e][0]][0].append(e)
            else:
                dictionary[wires[e][0]][0].append(e)
            if wires[e][1] not in dictionary:
                dictionary[wires[e][1]] = [[],[]]
                dictionary[wires[e][1]][1].append(e)
            else:
                dictionary[wires[e][1]][1].append(e)

            #creating equations from dictionary, where for j junctions , we will get j-1 effective equations . For further conveniences , we are creating a list of
            #equations , where each equation is represented by a dictionary
    equations = []
    i = 1
    for e in dictionary:
        variable_dictionary = {}
        for elt in dictionary[e][0]:
            variable_dictionary[elt] = 1
        for elt in dictionary[e][1]:
            variable_dictionary[elt] = -1
        equations.append(variable_dictionary)
    
    del equations[-1]#from this J equations , one is basically dependent and any equation can be like that, so we are removing one equation
    origin = 0 
    for e in wires:
        origin = wires[e][0]# here we have basically set one voltage to be zero .
        break
     #creating equations from volatege relations , for w wires , we will have w relations 
    for e in wires:
        if wires[e][1]!= origin and wires[e][0]!= origin:
            equations.append({wires[e][1]:1,wires[e][0]:-1,1:-voltages[e],e:resistances[e]})
        else:
            if wires[e][1]==origin:
                equations.append({wires[e][0]:-1,1:-voltages[e],e:resistances[e]})

            else:
                equations.append({wires[e][1]:1,1:-voltages[e],e:resistances[e]})
    #now we are going to use our recursive function solvelinear , here vaiables are the junctions and wire IDs and equations we have got earlier
    variables  = set()
    for e in wires :
        variables.add(e)
    for j in junctions:
        variables.add(j)
    result_dictionary = solveLinear(variables, equations)
    circuit_solution = {}
    for e in wires :
        circuit_solution[e] = result_dictionary[e]
    return circuit_solution
         
    


def findMaximumDeviationJunction(junctions, wires, resistances, voltages, currents):
    """
        Note that this part is completely optional and would not contribute to your grade.
        
        Given:
            junctions:  A set of junctions. Each junction is labeled by a
                        string or a tuple.
            wires:      A dictionary mapping a unique wire ID (a string or tuple)
                        to a tuple of two elements representing the starting and
                        ending junctions of the wire respectively. The set of
                        wire IDs is disjoint from the set of junction labels.
                        Note that although electricity can flow in either
                        direction, each wire between a pair of junctions will
                        appear exactly once in the list. Moreover, the starting
                        and ending junctions are distinct.
            resistances:A dictionary mapping each unique wire ID to a numeric
                        value representing the magnitude of the resistance of
                        the wire in Ohms. This dictionary has the same set of
                        keys as the wires dictionary.
            voltages:   A dictionary mapping each unique wire ID to a numeric
                        value representing the voltage (EMF or potential
                        difference) of the battery connected along the wire in
                        Volts. The positive terminal of the battery is next to
                        the ending junction (as defined in the wires dictionary)
                        if the voltage is positive whereas it is next to the
                        starting junction otherwise. This dictionary also has 
                        the same set of keys as the wires dictionary.
            currents:   A dictionary mapping each unique wire ID to a numeric
                        value representing the indicated current flowing along
                        the wire. The format is identical to that of the output 
                        of the previous function. Note that the values will not
                        necessarily be correct.
        Return:
            result: A junction with the maximum deviation from current
                    conservation. Note that any junction with maximal deviation
                    will be accepted.
    """
    raise NotImplementedError

def findMaximumDeviationLoop(junctions, wires, resistances, voltages, currents):
    """
        Note that this part is completely optional and would not contribute to your grade.
        
        Given:
            junctions:  A set of junctions. Each junction is labeled by a string
                        or a tuple.
            wires:      A dictionary mapping a unique wire ID (a string or tuple)
                        to a tuple of two elements representing the starting and
                        ending junctions of the wire respectively. The set of
                        wire IDs is disjoint from the set of junction labels.
                        Note that although electricity can flow in either
                        directions, each wire between a pair of junctions will
                        appear exactly once in the list. Moreover, the starting
                        and ending junctions are distinct.
            resistances:A dictionary mapping each unique wire ID to a numeric
                        value representing the magnitude of the resistance of 
                        the wire in Ohms. This dictionary has the same set of
                        keys as the wires dictionary.
            voltages:   A dictionary mapping each unique wire ID to a numeric
                        value representing the voltage (EMF or potential
                        difference) of the battery connected along the wire in
                        Volts. The positive terminal of the battery is next to
                        the ending junction (as defined in the wires dictionary)
                        if the voltage is positive whereas it is next to the 
                        starting junction otherwise. This dictionary also has
                        the same set of keys as the wires dictionary.
            currents:   A dictionary mapping each unique wire ID to a numeric
                        value representing the indicated current flowing along
                        the wire. The format is identical to that of the output
                        of the previous function. Note that the values will not
                        necessarily be correct.
        Return:
            result: A list of wires IDs representing the edges along a loop with
                    maximal (additive) deviation from Kirchoff's loop law.
                    The wires should be in order along the cycle but the
                    starting node and the direction may be arbitrary.
    """
    raise NotImplementedError

if __name__ == '__main__':
    # additional code here will be run only when lab.py is invoked directly
    # (not when imported from test.py), so this is a good place to put code
    # used for testing.
    pass
