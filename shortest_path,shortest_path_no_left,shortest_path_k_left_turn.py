"""6.009 Lab 5 -- Don't Turn Left!"""

# NO ADDITIONAL IMPORTS

def shortest_path(edges, origin, destination):
    """
    Finds a shortest path from start to end using the provided edges

    Args:
        edges: a list of dictionaries, where each dictionary has two items. 
            These items have keys `"start"` and `"end"` and values that are 
            tuples (two integers), to specify grid locations.
        start: a tuple representing our initial location.
        end: a tuple representing the target location.

    Returns:
        A list containing the edges taken in the resulting path if one exists, 
            None if there is no path

        formatted as:
            [{"start":(x1,y1), "end":(x2,y2)}, {"start":(x2,y2), "end":(x3,y3)}]
    """
    #creating a dictionary where keys are vertices and each vertice is mapping to the set of vertices it is connected with
    data_set = {}
    for e in edges:
        if e["start"] in data_set:
            data_set[e["start"]].add(e["end"])
        else:
            data_set[e["start"]]=set()
            data_set[e["start"]].add(e["end"])
    #keeping track of which vertices are added here
    track_set = {origin}
    #path_search is dictionary mapping child node to parent node
    path_search = {}
    i = 1
    first_number ={0:{origin}}
    if origin not in data_set :
        return None
    while destination not in track_set:
        first_number[i]=set()
        flag = False
        for e in first_number[i-1]:
            if e in data_set:
                for element in data_set[e]:
                    if element not in track_set:
                        flag= True
                        first_number[i].add(element)
                        track_set.add(element)
                        path_search[element]=e
        if flag == True:
            i=i+1
        else:
            break
    if not flag:
        return None
    #finding opath from path_search
    path = []
    path.append(destination)
    while origin not in path:
        if path_search[destination]:
            path.append(path_search[destination])
            destination = path_search[destination]
    path.reverse()
    new_dict = []
    for i in range(len(path)-1):
        new_dict.append({"start":path[i],"end":path[i+1]})
    return new_dict



def shortest_path_no_lefts(edges, origin, destination):
    """
    Finds a shortest path without any left turns that goes
        from start to end using the provided edges. 
        (reversing turns are also not allowed)

    Args:
        edges: a list of dictionaries, where each dictionary has two items. 
            These items have keys `"start"` and `"end"` and values that are 
            tuples (two integers), to specify grid locations.
        start: a tuple representing our initial location.
        end: a tuple representing the target location.

    Returns:
        A list containing the edges taken in the resulting path if one exists, 
            None if there is no path

        formatted as:
            [{"start":(x1,y1), "end":(x2,y2)}, {"start":(x2,y2), "end":(x3,y3)}]
    """
    #creating a dictionary where keys are vertices and each vertice is mapping to the set of vertices it is connected with
    data_set = {}
    for e in edges:
        if e["start"] in data_set:
            data_set[e["start"]].add(e["end"])
        else:
            data_set[e["start"]]=set()
            data_set[e["start"]].add(e["end"])
    #creating another data_set where edges are the keys, from each edge we will travel to the valid edges.
    data_set2 = {}
    for e in data_set:
        for element in data_set[e]:
            if (e,element) not in data_set2:
                data_set2[(e,element)]=set()
                if element in data_set:
                    for elt in data_set[element]:#now we will start computing cross and dot products and check the conditions
                        if (element[0]-e[0])*(elt[1]-element[1])-(element[1]-e[1])*(elt[0]-element[0])==0:
                            if (element[0]-e[0])*(elt[0]-element[0])+(element[1]-e[1])*(elt[1]-element[1])>0:
                                data_set2[(e,element)].add((element,elt))

                        elif (element[0]-e[0])*(elt[1]-element[1])-(element[1]-e[1])*(elt[0]-element[0])>0:
                            data_set2[(e,element)].add((element,elt))
                if data_set2[(e,element)]==set():
                    del data_set2[(e,element)]
    
    track_set = set()
    for element in data_set[origin]:
        track_set.add((origin,element))#track set is checking any edge is visited twice
    path_search = {}
    i = 1
    edge_level={}
    edge_level[0]=set()
    
    for element in data_set[origin]:
        edge_level[0].add((origin,element))
    
    if origin not in data_set :
        return None
    #edge_level is the main BFS part
    #path_search is a dictionary with child node mapping to parent node, here nodes are edges 
    while True:
       
        edge_level[i]=set()
        flag = False
        check_done = False
        for e in edge_level[i-1]:
            if e in data_set2:
                for element in data_set2[e]:
                    if element not in track_set:
                        flag= True
                        edge_level[i].add(element)
                        track_set.add(element)
                        path_search[element]=e
                    if element[1]==destination:
                        check_done = True
                        break
            if check_done== True:
                break
             

    
        if flag == True and check_done == False:
            i=i+1
        elif flag == False and check_done == True:
            break
        else:
            break
    if flag==False:
        return None 
    #creating paths from destination. 
    path = []
    code_check = False
    for e in path_search:
        if code_check == False:
            if e[1]==destination:
                path = []
                path.append(e)
                f = e
                while f[0]!=origin:
                    if f in path_search:
                        path.append(path_search[f])
                        f = path_search[f]
                    else:
                        if f[1]==origin:
                            code_check = True
                        else:
                            break
        else:
            break
    path.reverse()
    new_dict = []
    for i in range(len(path)):
        new_dict.append({"start":path[i][0],"end":path[i][1]})
    return new_dict

    
    

def shortest_path_k_lefts(edges, origin, destination, k):
    """
    Finds a shortest path with no more than k left turns that 
        goes from start to end using the provided edges.
        (reversing turns are also not allowed)

    Args:
        edges: a list of dictionaries, where each dictionary has two items. 
            These items have keys `"start"` and `"end"` and values that are 
            tuples (two integers), to specify grid locations.
        start: a tuple representing our initial location.
        end: a tuple representing the target location.
        k: the max number of allowed left turns.

    Returns:
        A list containing the edges taken in the resulting path if one exists, 
            None if there is no path

        formatted as:
            [{"start":(x1,y1), "end":(x2,y2)}, {"start":(x2,y2), "end":(x3,y3)}]
    """
    data_set = {}
    for e in edges:
        if e["start"] in data_set:
            data_set[e["start"]].add(e["end"])
        else:
            data_set[e["start"]]=set()
            data_set[e["start"]].add(e["end"])
    #creating another data_set where edges are the keys, from each edge we will travel to the valid edges.This time we are going to make k+1 copies.
    data_set2= {}
    i=k
    while i>=0:
        for e in data_set:
            for element in data_set[e]:
                if ((e,element),i) not in data_set2:
                    data_set2[((e,element),i)]=set()
                    if element in data_set:
                        for elt in data_set[element]:#now we will start computing cross and dot products and check the conditions
                            if (element[0]-e[0])*(elt[1]-element[1])-(element[1]-e[1])*(elt[0]-element[0])==0:
                                if (element[0]-e[0])*(elt[0]-element[0])+(element[1]-e[1])*(elt[1]-element[1])>0:
                                    data_set2[((e,element),i)].add(((element,elt),i))

                            elif (element[0]-e[0])*(elt[1]-element[1])-(element[1]-e[1])*(elt[0]-element[0])>0:
                                data_set2[((e,element),i)].add(((element,elt),i))
                            elif (element[0]-e[0])*(elt[1]-element[1])-(element[1]-e[1])*(elt[0]-element[0])<0 :
                                if i>=1:
                                    data_set2[((e,element),i)].add(((element,elt),i-1))
                    if data_set2[((e,element),i)]==set():
                        del data_set2[((e,element),i)]
        i=i-1
    track_set = set()
    for element in data_set[origin]:
        track_set.add(((origin,element),k))#track set is checking any edge is visietd twice
    path_search = {}
    i = 1
    edge_level={}
    edge_level[0]=set()
    
    for element in data_set[origin]:
        edge_level[0].add(((origin,element),k))
    
    while True:
       
        edge_level[i]=set()
        flag = False
        check_done = False
        for e in edge_level[i-1]:
            if e in data_set2:
                for element in data_set2[e]:
                    if element not in track_set:
                        flag= True
                        edge_level[i].add(element)
                        track_set.add(element)
                        path_search[element]=e
                    if element[0][1]==destination:
                        check_done = True
                        break
            if check_done== True:
                break
             

    
        if flag == True and check_done == False:
            i=i+1
        elif flag == False and check_done == True:
            break
        else:
            break
    if flag==False:
        return None 
    #creating paths from destination. 
    path = []
    code_check = False
    for e in path_search:
        if code_check == False:
            if e[0][1]==destination:
                path = []
                path.append(e)
                f = e
                while f[0][0]!=origin:
                    if f in path_search:
                        path.append(path_search[f])
                        f = path_search[f]
                    else:
                        if f[0][1]==origin:
                            code_check = True
                        else:
                            break
        else:
            break
    path.reverse()
    new_dict = []
    for i in range(len(path)):
        new_dict.append({"start":path[i][0][0],"end":path[i][0][1]})
    return new_dict

    



if __name__ == "__main__":
    # additional code here will be run only when lab.py is invoked directly
    # (not when imported from test.py), so this is a good place to put code
    # used for testing.
    pass


