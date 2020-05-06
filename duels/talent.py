import json
from copy import deepcopy

class Talent(object):
    def __init__(self):
        pass


class TalentNode(object):
    def __init__(self, id):
        self.name = ""
        self.desc = ""
        self.id = id
        self.cons = []


class TalentGraph(object):
    """Main object to keep track of and load talent graph data"""
    MAX_POINTS = 10
    def __init__(self):
        with open('talents.json', 'r') as f:
            nodes_dat = json.loads(f.read())
        self.nodes = [TalentNode(i) for i in range(len(nodes_dat))]
        for node in self.nodes:
            node.cons = [TalentNode(i) for i in nodes_dat[node.id]['cons']]

    def test_valid(self, node_is, visited_is, pos=0):
        pass
        # at_node = self.nodes[pos]
        # visited_is.append(at_node)
        # for to_node_i in at_node.cons:
        #     to_node = self.nodes[to_node_i]
        #     self.test_valid(deepcopy)

            
    