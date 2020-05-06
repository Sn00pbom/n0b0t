import json


class Talent(object):
    def __init__(self):
        pass


class TalentNode(object):
    def __init__(self, id):
        self.name = ""
        self.desc = ""
        self.id = id
        self.cons = []
        self.alloc = False


class TalentGraph(object):
    """Main object to keep track of and load talent graph data"""
    MAX_POINTS = 10
    def __init__(self):
        with open('duels/talents.json', 'r') as f:
            nodes_dat = json.loads(f.read())
        self.nodes = [TalentNode(i) for i in range(len(nodes_dat))]
        for node in self.nodes:
            node.cons = [i for i in nodes_dat[node.id]['cons']]

    def test_valid(self, node_is, visited_is=list(), pos=0):
        if len(node_is) > self.MAX_POINTS: return False
        at_node = self.nodes[pos]
        visited_is.append(pos)

        if pos in node_is: node_is.remove(pos)
        else: return

        for to_node_i in at_node.cons:
            if to_node_i in node_is and not to_node_i in visited_is:
                self.test_valid(node_is, visited_is, to_node_i)

        if pos is 0:
            return len(node_is) is 0


if __name__ == "__main__":
    graph = TalentGraph()
    node_is = [0, 1, 2, 4]
    print(graph.test_valid(node_is, []))
            
    