# NO IMPORTS ALLOWED!

import json

def did_x_and_y_act_together(data, actor_id_1, actor_id_2):
    for e in data:
        if actor_id_1 in e:
            if actor_id_2 in e:
                return True
    return False 
def data_set_construction(data):#constructing a dictionary of sets, a helper function
    data_set  = {}
    for e in data:
        
        if e[0] in data_set:
            data_set[e[0]].add(e[1])
        else:
            data_set[e[0]]=set()
            data_set[e[0]].add(e[1])
        if e[1] in data_set:
            data_set[e[1]].add(e[0])
        else:
            data_set[e[1]]=set()
            data_set[e[1]].add(e[0])

    return data_set

def get_actors_with_bacon_number(data, n):
    bacon_number = {0:{4724}}
    data_set= data_set_construction(data)
    track_set = {4724}#keeping track so that the no each [erson gets the smallest bacon number and no person is repeated
    flag = True
    for i in range(1,n+1):
        bacon_number[i]= set()#empty set 
        for e in bacon_number[i-1]:
            for element in data_set[e]:
                if element not in track_set:#add only if the element not in track set 
                    bacon_number[i].add(element)
                    track_set.add(element)
        if len(track_set)==len(data_set) and i<n:
            flag = False
            break
    if flag == True:
        return bacon_number[n]
    else:
        return []

def get_bacon_path(data, actor_id):
    data_set= data_set_construction(data)
    track_set = {4724}
    path_search = {}
    i = 1
    bacon_number = {0:{4724}}
    if actor_id not in data_set:
        return None
    if actor_id== 4724:
        return [4724]
    while actor_id not in track_set:
        bacon_number[i]= set()
        flag = False 
        for e in bacon_number[i-1]:
           
            for element in data_set[e]:
                if element not in track_set:# if this condition is executed for at least one time ,flag will be true,else we should get out of the code or
                                            # we will be in an infinite loop 
                    flag = True
                    bacon_number[i].add(element)
                    track_set.add(element)
                    path_search[element] = e
        if flag == True:
            i = i+1
        else:
            break
    if not flag:
        return None 
                    
    list = []
    list.append(actor_id)
    while 4724 not in list:
        if path_search[actor_id]:
            list.append(path_search[actor_id])
            actor_id = path_search[actor_id] 
            
    
    return list[::-1]
def get_path(data, actor_id_1, actor_id_2):
    data_set= data_set_construction(data)
    track_set = {actor_id_2}
    path_search = {}
    i = 1
    first_number = {0:{actor_id_2}}
    if actor_id_1 not in data_set or actor_id_2 not in data_set:
        return None
    while actor_id_1 not in track_set:
        first_number[i]= set()
        flag = False
        for e in first_number[i-1]:
            
            for element in data_set[e]:
                if element not in track_set:
                    flag = True
                    first_number[i].add(element)
                    track_set.add(element)
                    path_search[element] = e
        if flag == True:   
            i = i+1
        else:
            break  
    if not flag:
        return None
        
                    
    path = []
    path.append(actor_id_1)
    while actor_id_2 not in path:
        if path_search[actor_id_1]:
            path.append(path_search[actor_id_1])
            actor_id_1 = path_search[actor_id_1] 

   
    return path
    

if __name__ == '__main__':
    # additional code here will be run only when lab.py is invoked directly
    # (not when imported from test.py), so this is a good place to put code
    # used, for example, to generate the results for the online questions.
    pass
        
