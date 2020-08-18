class Item:
    #initialiser
    def __init__(self, key, value):
        self._key = float(key)
        self._value = value
        self._index = None

    #String method for element
    def __str__(self):
        return "Key: %s,  Value: %s, index - %s" %  (self._key, self._value, self._index)

    def __lt__(self, other):
        return self._key < other._key

    def __eq__(self, other):
        return self._key == other._key

    def wipe(self):
        self._key = None
        self._value = None
        self._index = None

class ADP:
    #the queue heap structure will be in the form of a list, for item manipulation
    def __init__(self):
        self.Heap = []

    #string representation for the Queue,all on new line, will also rreturn a heaped list of all the edge values..
    def __str__(self):
        outputStr = ''
        for element in self.Heap:
            outputStr += element.__str__()

        global edge_List
        edge_List = []
        for element in self.Heap:

            edge_List.append(str(element._key))

        print("Order of weight of each edge in Queue:"  , edge_List)
        return outputStr

    def add(self, key,  item):
        #adding item to the heap whilst maintining the heap
        #and taking into account the heap itself being empty
        element = Item(key, item)
        self.Heap.append(element)
        if self.__len__() > 0:
            element._index = len(self.Heap) - 1
        else:
            element._index = 0
            return
        self._shift_Down(0, len(self.Heap) - 1)
        return element

    def __len__(self):
        return len(self.Heap)

    def min(self):
        return self.Heap[0]

    def remove(self, element):
        removed_index = element._index
        element._wipe()
        self.Heap.remove(self.Heap[removed_index])

        length_Of_Heap = len(self.Heap)
        # here we rebalance the heap after removing the item
        self._heapify()


    def remove_Min(self):
        #pop smallest item off of the heap whilst maintaining the heap
        last_Item = self.Heap.pop(0)
        if self.__len__() > 0:

            self._shift_Up(0)

        return last_Item

    def update_Key(self, element, newkey):
        #updates key value of node and then resets the heap to correct positioning
        element._key = newkey
        self._heapify()

    def isEmpty(self):
        if self.__len__() == 0:
            return True
        else:
            return False

    def get_Key(self, element):
        searched_Element = self.Heap[element._index]
        return searched_Element._key

    def _shift_Down(self, start_Position, end_Position):
        added_Item = self.Heap[end_Position]

        # Follow the path to the root, moving parents down until finding a place newitem fits

        while end_Position > start_Position:
            parent_Position = (end_Position -1) >> 1

            parent_Item = self.Heap[parent_Position]
            if added_Item.__lt__(parent_Item) == True:
                added_Item._index = parent_Position
                parent_Item._index = end_Position
                self.Heap[end_Position] = parent_Item
                end_Position = parent_Position
                continue
            break

        self.Heap[end_Position] = added_Item


    def _shift_Up(self, top_Position):
        end_Position = len(self.Heap)
        # newitem = self.Heap[top_Position]

        starting_Position = top_Position
        new_Root = self.Heap[top_Position]
        #bubble up the smaller child position until a leaf node is hit
        Child_Pos = 2 * top_Position + 1
        count = 0
        while Child_Pos < end_Position:
            count += 1
            # Set childpos to index of smaller child.
            right_Pos = Child_Pos + 1
            if right_Pos < end_Position and not self.Heap[Child_Pos].__lt__(self.Heap[right_Pos]):
                Child_Pos = right_Pos

            old_index = self.Heap[top_Position]._index

            self.Heap[top_Position] = self.Heap[Child_Pos]
            top_Position = Child_Pos
            Child_Pos = 2 * top_Position + 1
        self.Heap[top_Position] = new_Root
        # The leaf at pos is empty now.  Put newitem there, and bubble it up
        # to its final resting place (by sifting its parents down).

        self._shift_Down(starting_Position, top_Position)
        #resetting all indexes needed as the shift operations change all
        self._set_indexes()


    def _heapify(self):
        length = len(self.Heap)

        for i in reversed(range(length//2)):
            self._shift_Up(i)

    def _set_indexes(self):
        for item in self.Heap:
            curr_index = self.Heap.index(item)
            item._index = curr_index



class Vertex:
    """ A Vertex in a graph. """

    def __init__(self, element):
        """ Create a vertex, with data element. """
        self._element = element

    def __str__(self):
        """ Return a string representation of the vertex. """
        return str(self._element)

    def __lt__(self, v):
        return self._element < v.element()

    def element(self):
        """ Return the data for the vertex. """
        return self._element

    __repr__ = __str__ #kept getting obj error, realised obj ref was being returmed not a str

class Edge:
    """ An edge in a graph.

        Implemented with an order, so can be used for directed or undirected
        graphs. Methods are provided for both. It is the job of the Graph class
        to handle them as directed or undirected.
    """

    def __init__(self, v, w, element):
        """ Create an edge between vertice v and w, with label element.

            element can be an arbitrarily complex structure.
        """
        self._vertices = (v, w)
        self._element = element

    def __str__(self):
        """ Return a string representation of this edge. """
        return ('(' + str(self._vertices[0]) + '--'
                + str(self._vertices[1]) + ' : '
                + str(self._element) + ')')

    def vertices(self):
        """ Return an ordered pair of the vertices of this edge. """
        return self._vertices

    def start(self):
        """ Return the first vertex in the ordered pair. """
        return self._vertices[0]

    def end(self):
        """ Return the second vertex in the ordered. pair. """
        return self._vertices[1]

    def opposite(self, v):
        """ Return the opposite vertex to v in this edge. """
        if self._vertices[0] == v:
            return self._vertices[1]
        elif self._vertices[1] == v:
            return self._vertices[0]
        else:
            return None

    def element(self):
        """ Return the data element for this edge. """
        return self._element


class Graph:
    """ Represent a simple graph.

        This version maintains only undirected graphs, and assumes no
        self loops.
    """

    # Implement as a Python dictionary
    #  - the keys are the vertices
    #  - the values are the edges for the corresponding vertex
    #    Each edge set is also maintained as a dictionary,
    #    with opposite vertex as the key and the edge object as the value

    def __init__(self):
        """ Create an initial empty graph. """
        self._structure = dict()

    def __str__(self):
        """ Return a string representation of the graph. """
        hstr = ('|V| = ' + str(self.num_vertices())
                + '; |E| = ' + str(self.num_edges()))
        vstr = '\nVertices: '
        for v in self._structure:
            vstr += str(v) + '-'
        edges = self.edges()
        estr = '\nEdges: '
        for e in edges:
            estr += str(e) + ' '
        return hstr + vstr + estr

    # --------------------------------------------------#
    # ADT methods to query the graph

    def num_vertices(self):
        """ Return the number of vertices in the graph. """
        return len(self._structure)

    def num_edges(self):
        """ Return the number of edges in the graph. """
        num = 0
        for v in self._structure:
            num += len(self._structure[v])  # the dict of edges for v
        return num // 2  # divide by 2, since each edege appears in the
        # vertex list for both of its vertices

    def vertices(self):
        """ Return a list of all vertices in the graph. """
        return [key for key in self._structure]

    def get_vertex_by_label(self, element):
        """ get the first vertex that matches element. """
        for v in self._structure:
            if v.element() == element:
                return v
        return None

    def edges(self):
        """ Return a list of all edges in the graph. """
        edgelist = []
        for v in self._structure:
            for w in self._structure[v]:
                # to avoid duplicates, only return if v is the first vertex
                if self._structure[v][w].start() == v:
                    edgelist.append(self._structure[v][w])
        return edgelist

    def get_edges(self, v):
        """ Return a list of all edges incident on v. """
        if v in self._structure:
            edgelist = []
            for w in self._structure[v]:
                edgelist.append(self._structure[v][w])
            return edgelist
        return None

    def get_edge(self, v, w):
        """ Return the edge between v and w, or None. """
        if (self._structure != None
                and v in self._structure
                and w in self._structure[v]):
            return self._structure[v][w]
        return None

    def degree(self, v):
        """ Return the degree of vertex v. """
        return len(self._structure[v])

        # ADT methods to modify the graph

    def add_vertex(self, element):
        """ Add a new vertex with data element.

            If there is already a vertex with the same data element,
            this will create another vertex instance.
        """
        v = Vertex(element)
        self._structure[v] = dict()
        return v

    def add_vertex_if_new(self, element):
        """ Add and return a vertex with element, if not already in graph.

            Checks for equality between the elements. If there is special
            meaning to parts of the element (e.g. element is a tuple, with an
            'id' in cell 0), then this method may create multiple vertices with
            the same 'id' if any other parts of element are different.

            To ensure vertices are unique for individual parts of element,
            separate methods need to be written.
        """
        for v in self._structure:
            if v.element() == element:
                # print('Already there')
                return v
        return self.add_vertex(element)

    def add_edge(self, v, w, element):
        """ Add and return an edge between two vertices v and w, with  element.

            If either v or w are not vertices in the graph, does not add, and
            returns None.

            If an edge already exists between v and w, this will
            replace the previous edge.
        """
        if not v in self._structure or not w in self._structure:
            return None
        e = Edge(v, w, element)
        self._structure[v][w] = e
        self._structure[w][v] = e
        return e

    def add_edge_pairs(self, elist):
        """ add all vertex pairs in elist as edges with empty elements. """
        for (v, w) in elist:
            self.add_edge(v, w, None)

    ##################################

    def dijkstras(self, s):
        open = ADP()
        locs = {}
        closed = {}
        predecessors = {s: None}
        first = open.add(0, s)
        locs[s] = first

        while open.isEmpty() == False:

            rem_Min = open.remove_Min()
            node = rem_Min._value
            weight = rem_Min._key
            locs.pop(node) #remove entry of min element from locs
            pre = predecessors.pop(node) #remove entry of min element from predecessors
            closed[node] = (weight, pre) #adding entry into closed
            all_edges = self.get_edges(node) #getting edges to iterate through
            for edge in all_edges:
                opposite_Vertex = edge.opposite(node) #getting the opposite vertex to node in edge
                if opposite_Vertex not in closed:
                    newCost = weight + edge.element() # weight plus new weight
                    if opposite_Vertex not in locs: #basically if not yet added into open
                        predecessors[opposite_Vertex] = node
                        new_Element = open.add(newCost, opposite_Vertex)
                        locs[opposite_Vertex] = new_Element
                    elif newCost < open.get_Key(locs[opposite_Vertex]): #else if newcost is better (shorter) than the older cost
                        predecessors[opposite_Vertex] = node    #we predecessors
                        open.update_Key(locs[opposite_Vertex], newCost) # and update the cost in open to new cost

        return  closed


if __name__ == '__main__':
    def graphreader(filename):
        """ Read and return the route map in filename. """
        graph = Graph()
        file = open(filename, 'r')
        entry = file.readline()  # either 'Node' or 'Edge'
        num = 0
        while entry == 'Node\n':
            num += 1
            nodeid = int(file.readline().split()[1])
            vertex = graph.add_vertex(nodeid)
            entry = file.readline()  # either 'Node' or 'Edge'
        print('Read', num, 'vertices and added into the graph')
        num = 0
        while entry == 'Edge\n':
            num += 1
            source = int(file.readline().split()[1])
            sv = graph.get_vertex_by_label(source)

            target = int(file.readline().split()[1])
            tv = graph.get_vertex_by_label(target)

            length = float(file.readline().split()[1])

            edge = graph.add_edge(sv, tv, length)
            file.readline()  # read the one-way data
            entry = file.readline()  # either 'Node' or 'Edge'
        print('Read', num, 'edges and added into the graph')

        return graph

    def code_Test():
        print("First Test File")        #running both text files and returning the path in a dictionary for both test files
        first_Graph = graphreader('simplegraph1.txt')
        first_Vertex = first_Graph.get_vertex_by_label(4.0)
        print(first_Graph.dijkstras(first_Vertex))
        print("\n")

        print("Second Test File")
        second_Graph = graphreader('simplegraph2.txt')
        second_Vertex = second_Graph.get_vertex_by_label(17.0)
        print(second_Graph.dijkstras(second_Vertex))
    code_Test()