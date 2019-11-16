"""6.009 Lab 8: Graphs, Paths, Matrices."""

from abc import ABC, abstractmethod
# NO ADDITIONAL IMPORTS ALLOWED!


class Graph(ABC):
    """Interface for a mutable directed, weighted graph."""

    @abstractmethod
    def add_node(self, node):
        """Add a node to the graph.

        Arguments:
            node (str): the node to add

        Raises:
            ValueError: if the node already exists.

        """
        pass

    @abstractmethod
    def add_edge(self, start, end, weight):
        """Add a directed edge to the graph.

        If the edge already exists, then set its weight to `weight`.

        Arguments:
            start (str): the node where the edge starts
            end (str): the node where the edge ends
            weight (int or float): the weight of the edge, assumed to be a nonnegative number

        Raises:
            LookupError: if either of these nodes doesn't exist

        """
        pass

    @abstractmethod
    def nodes(self):
        """Return the nodes in the graph.

        Returns:
            set: all of the nodes in the graph

        """
        pass

    @abstractmethod
    def neighbors(self, node):
        """Return the neighbors of a node.

        Arguments:
            node (str): a node name

        Returns:
            set: all tuples (`neighbor`, `weight`) for which `node` has an
                 edge to `neighbor` with weight `weight`

        Raises:
            LookupError: if `node` is not in the graph

        """
        pass

    @abstractmethod
    def get_path_length(self, start, end):
        """Return the length of the shortest path from `start` to `end`.

        Arguments:
            start (str): a node name
            end (str): a node name

        Returns:
            float or int: the length (sum of edge weights) of the path or
                          `None` if there is no such path.

        Raises:
            LookupError: if either `start` or `end` is not in the graph

        """
        pass

    @abstractmethod
    def get_path(self, start, end):
        """Return the shortest path from `start` to `end`.

        Arguments:
            start (str): a node name
            end (str): a node name

        Returns:
            list: nodes, starting with `start` and, ending with `end`, which
                  comprise the shortest path from `start` to `end` or `None`
                  if there is no such path

        Raises:
            LookupError: if either `start` or `end` is not in the graph

        """
        pass

    @abstractmethod
    def get_all_path_lengths(self):
        """Return lengths of shortest paths between all pairs of nodes.

        Returns:
            dict: map from tuples `(u, v)` to the length of the shortest path
                  from `u` to `v`

        """
        pass
        

    @abstractmethod
    def get_all_paths(self):
        """Return shortest paths between all pairs of nodes.

        Returns:
            dict: map from tuples `(u, v)` to a list of nodes (starting with
                  `u` and ending with `v`) which is a shortest path from `u`
                  to `v`

        """
        pass


class AdjacencyDictGraph(Graph):
    """A graph represented by an adjacency dictionary."""

    def __init__(self):
        """Create an empty graph."""
        self.vertices= {}
        self.pred = {}
        self.dist = {}

    def add_node(self, node):
        """Add a node to the graph.

        Arguments:
            node (str): the node to add

        Raises:
            ValueError: if the node already exists.

        """
        if node not in self.vertices:
            self.vertices[node]=set()
        else:
            raise ValueError

 
    def add_edge(self, start, end, weight):
        """Add a directed edge to the graph.

        If the edge already exists, then set its weight to `weight`.

        Arguments:
            start (str): the node where the edge starts
            end (str): the node where the edge ends
            weight (int or float): the weight of the edge, assumed to be a nonnegative number

        Raises:
            LookupError: if either of these nodes doesn't exist

        """
        if start not in self.vertices or end not in self.vertices:
            raise LookupError
   
        flag = True
        for e in self.vertices[start]:
            if e[0] == end:
                print('n')
                flag = False
                break
                
            
        if flag:
            self.vertices[start].add((end,weight))
        else:
            self.vertices[start].discard(e)
            e = e[:-1]+(weight,)
            self.vertices[start].add(e)
        
            

    def nodes(self):
        """Return the nodes in the graph.

        Returns:
            set: all of the nodes in the graph

        """
        res_set = {elt for elt in self.vertices}
        return res_set
            

    def neighbors(self, node):
        """Return the neighbors of a node.

        Arguments:
            node (str): a node name

        Returns:
            set: all tuples (`neighbor`, `weight`) for which `node` has an
                 edge to `neighbor` with weight `weight`

        Raises:
            LookupError: if `node` is not in the graph

        """
        if node not in self.vertices:
            raise LookupError
        else:
            return self.vertices[node]
    def path_updater(self):#this function does the basic part of updating distance and pred dictionaries
        marker_dict = {}
        for e in self.vertices:
            for (f,y) in self.vertices[e]:
                marker_dict[(e,f)]=y
        for node in self.vertices:#
            for node1 in self.vertices:
                if node!=node1:
                    self.pred[(node,node1)]= node1
      
  
        for node in self.vertices:
            for node1 in self.vertices:
                if node1!=node:
                    if (node,node1) not in marker_dict:
                        self.dist[(node,node1)]=float('inf')
                    else:
                        self.dist[(node,node1)]=marker_dict[(node,node1)]
                else:
                    self.dist[(node,node1)]=0

        for node in self.vertices:
            for node1 in self.vertices:
                for node2 in self.vertices:
                    if self.dist[(node1,node2)] > self.dist[(node1,node)]+self.dist[(node,node2)]:
                        self.dist[(node1,node2)] = self.dist[(node1,node)]+self.dist[(node,node2)]
                        self.pred[(node1,node2)] = self.pred[(node1,node)]
        
    def path_length_counter(self,start,end):# a helper function for faster process
        if self.dist[(start,end)]!=float('inf'):
            return self.dist[(start,end)]
        else:
            return None

    def get_path_length(self, start, end):
        """Return the length of the shortest path from `start` to `end`.

        Arguments:
            start (str): a node name
            end (str): a node name

        Returns:
            float or int: the length (sum of edge weights) of the path or
                          `None` if there is no such path.

        Raises:
            LookupError: if either `start` or `end` is not in the graph

        """
        self.path_updater()
        if start not in self.vertices or end not in self.vertices:
            raise LookupError
        return self.path_length_counter(start,end)
    def path_creater(self,start,end):# helper method for faster process which takes two nodes and create tha path
        path = [start]
        while start!=end:
            start = self.pred[(start,end)]
            path.append(start)
        return path
    
    def get_path(self, start, end):
        """Return the shortest path from `start` to `end`.

        Arguments:
            start (str): a node name
            end (str): a node name

        Returns:
            list: nodes, starting with `start` and, ending with `end`, which
                  comprise the shortest path from `start` to `end` or `None`
                  if there is no such path

        Raises:
            LookupError: if either `start` or `end` is not in the graph

        """
        self.path_updater()
        
        if start not in self.vertices or end not in self.vertices:
            raise LookupError
        if self.dist[(start,end)]==float('inf'):
            return None
        return self.path_creater(start,end)
        

    
    def get_all_path_lengths(self):
        """Return lengths of shortest paths between all pairs of nodes.

        Returns:
            dict: map from tuples `(u, v)` to the length of the shortest path
                  from `u` to `v`

        """
        self.path_updater()
        result_dict = {}
        for node in self.vertices:
            for node1 in self.vertices:
                if self.dist[(node,node1)]!=float('inf'):
                    result_dict[(node,node1)]=self.path_length_counter(node,node1)
        return result_dict
        

    
    def get_all_paths(self):
        """Return shortest paths between all pairs of nodes.

        Returns:
            dict: map from tuples `(u, v)` to a list of nodes (starting with
                  `u` and ending with `v`) which is a shortest path from `u`
                  to `v`

        """
        self.path_updater()
        result_dict = {}
        for node in self.vertices:
            for node1 in self.vertices:
                if self.dist[(node,node1)]!=float('inf'):
                    result_dict[(node,node1)]=self.path_creater(node,node1)
        return result_dict
         


class AdjacencyMatrixGraph(Graph):
    """A graph represented by an adjacency matrix."""

    def __init__(self):
        """Create an empty graph."""
        self.vertices = []
        self.tracker1 = {}
        self.tracker2 = {}
        self.dist_matrix = []
        self.path_matrix = []
    def add_node(self,start):
        """Add a node to the graph.

        Arguments:
            node (str): the node to add

        Raises:
            ValueError: if the node already exists.

        """
        n = len(self.tracker1)
        if start in self.tracker1:
            raise ValueError
        else:
            self.tracker1[start]= n
            self.tracker2[n]=start
            for e in self.vertices:
                e.append(float('inf'))
            new_list = []
            for i in range(n+1):
                new_list.append(float('inf'))
            self.vertices.append(new_list)
    def add_edge(self,start,end,weight):
        """Add a directed edge to the graph.

        If the edge already exists, then set its weight to `weight`.

        Arguments:
            start (str): the node where the edge starts
            end (str): the node where the edge ends
            weight (int or float): the weight of the edge, assumed to be a nonnegative number

        Raises:
            LookupError: if either of these nodes doesn't exist

        """
        
        if start not in self.tracker1 or end not in self.tracker1:
            raise LookupError
        self.vertices[self.tracker1[start]][self.tracker1[end]]=weight
    def nodes(self):
        """Return the nodes in the graph.

        Returns:
            set: all of the nodes in the graph

        """
        
        return set(self.tracker1.keys())
    def neighbors(self,node):
        """Return the neighbors of a node.

        Arguments:
            node (str): a node name

        Returns:
            set: all tuples (`neighbor`, `weight`) for which `node` has an
                 edge to `neighbor` with weight `weight`

        Raises:
            LookupError: if `node` is not in the graph

        """
        
        
        if node not in self.tracker1:
            raise LookupError
        return_set = set()
        l = len(self.tracker1)
        for i in range(l):
            if self.vertices[self.tracker1[node]][i]!=float('inf'):
                return_set.add((self.tracker2[i],self.vertices[self.tracker1[node]][i]))
        return return_set
    def path_developer(self):#main function which creates dist_matrix,path_,matrix
        l = len(self.vertices)
        self.dist_matrix = self.vertices[:]
        for i in range(l):
            self.dist_matrix[i][i]=0

        for i in range(l):
            self.path_matrix.append([])
            for f in range(l):
                if self.vertices[i][f]== float('inf'):
                    self.path_matrix[i].append((None))
                else:
                    self.path_matrix[i].append(f)
        for i in range(l):
            for j in range(l):
                for k in range(l):
                    if self.dist_matrix[j][k] > self.dist_matrix[j][i]+self.dist_matrix[i][k]:
                        self.dist_matrix[j][k] = self.dist_matrix[j][i]+self.dist_matrix[i][k]
                        self.path_matrix[j][k] = self.path_matrix[j][i]
    def path_length_counter(self,m,n):#a helper function for counting path length
        if self.dist_matrix[m][n]!=float('inf'):
            return self.dist_matrix[m][n]
        else:
            return None
        

                    
    def get_path_length(self,start,end):
        """Return the length of the shortest path from `start` to `end`.

        Arguments:
            start (str): a node name
            end (str): a node name

        Returns:
            float or int: the length (sum of edge weights) of the path or
                          `None` if there is no such path.

        Raises:
            LookupError: if either `start` or `end` is not in the graph

        """
        if start not in self.tracker1 or end not in self.tracker1:
            raise LookupError
        m = self.tracker1[start]
        n = self.tracker1[end]
        self.path_developer()
        return self.path_length_counter(m,n)
        
        
                    
                    
            
            
            
    def get_path(self,start,end):
        """Return the shortest path from `start` to `end`.

        Arguments:
            start (str): a node name
            end (str): a node name

        Returns:
            list: nodes, starting with `start` and, ending with `end`, which
                  comprise the shortest path from `start` to `end` or `None`
                  if there is no such path

        Raises:
            LookupError: if either `start` or `end` is not in the graph

        """
        if start not in self.tracker1 or end not in self.tracker1:
            raise LookupError
        m = self.tracker1[start]
        n = self.tracker1[end]
        self.path_developer()
        return self.path_creator(m,n)
    def get_all_path_lengths(self):
        """Return lengths of shortest paths between all pairs of nodes.

        Returns:
            dict: map from tuples `(u, v)` to the length of the shortest path
                  from `u` to `v`

        """
        self.path_developer()
        result_dict = {}
        l = len(self.tracker1)
        for i in range(l):
            for j in range(l):
                if self.dist_matrix[i][j]!=float('inf'):
                    result_dict[(self.tracker2[i],self.tracker2[j])]= self.path_length_counter(i,j)
        return result_dict
                                                 
    def path_creator(self,m,n):#takes two indices and create path between them 
        if self.dist_matrix[m][n]==float('inf'):
            return None
        path = [m]
        while m!=n:
            m = self.path_matrix[m][n]
            path.append(m)
        path2 = []
        for e in path:
            path2.append(self.tracker2[e])
        return path2
        

    
    def get_all_paths(self):
        """Return shortest paths between all pairs of nodes.

        Returns:
            dict: map from tuples `(u, v)` to a list of nodes (starting with
                  `u` and ending with `v`) which is a shortest path from `u`
                  to `v`

        """
        self.path_developer()
        result_dict = {}
        l = len(self.tracker1)
        for i in range(l):
            for j in range(l):
                if self.dist_matrix[i][j]!=float('inf'):
                    result_dict[(self.tracker2[i],self.tracker2[j])]= self.path_creator(i,j)
        return result_dict
        
        
        

class GraphFactory:
    """Factory for creating instances of `Graph`."""

    def __init__(self, cutoff=0.5):
        """Create a new factory that creates instances of `Graph`.

        Arguments:
            cutoff (float): the maximum density (as defined in the lab handout)
                            for which the an `AdjacencyDictGraph` should be
                            instantiated instead of an `AdjacencyMatrixGraph`

        """
        self.cutoff = cutoff

    def from_edges_and_nodes(self, weighted_edges, nodes):
        """Create a new graph instance.

        Arguments:
            weighted_edges (list): the edges in the graph given as
                                   (start, end, weight) tuples
            nodes (list): nodes in the graph

        Returns:
            Graph: a graph containing the given edges

        """
        e = len(weighted_edges)
        n = len(nodes)
        print(e)
        print(n)
        d = e/(n*(n-1))#checking density
        print(d,self.cutoff)
        if d <= self.cutoff:
            g = AdjacencyDictGraph()
            [g.add_node(n) for n in nodes]
            for e in weighted_edges:
                g.add_edge(e[0],e[1],e[2])
            return g
            
                
                
        elif d>self.cutoff:
            g = AdjacencyMatrixGraph()
            [g.add_node(n) for n in nodes]
            for e in weighted_edges:
                g.add_edge(e[0],e[1],e[2])
            return g
        


def get_most_central_node(graph):
    """Return the most central node in the graph.

    "Most central" is defined as having the shortest average round trip to any
    other node.

    Arguments:
        graph (Graph): a graph with at least one node from which round trips
                       to all other nodes are possible

    Returns:
        node (str): the most central node in the graph; round trips to all
                    other nodes must be possible from this node

    """
    length = len(graph.nodes())
    check_dict = {}# a dictionary of all nodes from which there are paths to every other node and from every other node, there is a path to that
    #node
    my_set = graph.nodes()
    for e in graph.nodes():
        flag = True
        for elt in my_set-{e}:
            if graph.get_path(elt,e)== None or graph.get_path(e,elt)==None:
                flag = False
        if flag:
            sum = 0
            for elt in my_set-{e}:
                sum+=graph.get_path_length(e,elt)+graph.get_path_length(elt,e)
            check_dict[e]=sum
                
  
    return min(check_dict, key=check_dict.get)
        


if __name__ == "__main__":
    # You can place code (like custom test cases) here that will only be
    # executed when running this file from the terminal.
    graph = AdjacencyDictGraph()
    [graph.add_node(n) for n in 'abcde']
    graph.add_edge('a', 'b', 2)
    graph.add_edge('b', 'a', 1.5)
    graph.add_edge('a', 'd', 1.5)
    graph.add_edge('d', 'a', 1.5)
    graph.add_edge('d', 'b', 4)
    graph.add_edge('b', 'd', 4)
    graph.add_edge('d', 'c', 5)
    graph.add_edge('c', 'd', 1)
    graph.add_edge('b', 'c', 99)
    graph.add_edge('c', 'b', 95)
    graph.add_edge('b', 'e', 1)
    graph.add_edge('e', 'b', 4)
    print(get_most_central_node(graph))
    
    
    pass
