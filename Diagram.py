import json
from Vertex import Vertex
from Edge import Edge


class Diagram:

    def __init__(self, path):
        with open(path) as f:
           data = json.load(f)
        self.graph = {}
        self.vertex_info = {}
        self.vertex_type = {}
        self.edge_info = {}
        for node in data["nodeDataArray"]:
            self.graph[node["key"]] = []
            self.vertex_info[node["key"]] = node["text"]
            self.vertex_type[node["key"]] = node["category"]

        for edge in data["linkDataArray"]:
            self.graph[edge["from"]].append(edge["to"])
            self.edge_info[(edge["from"], edge["to"])] = edge["text"]

    def num_of_vertices(self):
        return len(self.vertex_info)

    def neighbors(self, key):
        return self.graph[key]

    def arc_type(self, from_node, to_node):
        return self.edge_info[(from_node, to_node)]

    def vertex_text(self, key):
        return self.vertex_info[key]

    def get_first_node(self):
        return self.vertex_info[-1]

    def get_type(self, id):
        return self.vertex_type[id]

    def bfs(self):
        print(str(self.vertex_info))
        print(str(self.graph))
        queue = [-1]
        visited = {}
        for key in self.graph:
            visited[key] = False
        while queue:
            vertex = queue.pop(0)
            visited[vertex] = True
            print("ID:"+str(vertex)+" Text: "+self.vertex_info[vertex])
            print("My neighbor:")
            i = 0
            for key in self.graph[vertex]:
                count = count + len(key.split())
                i += 1
            #     if not visited[key]:
            #         queue.append(key)
            #     print("ID:"+str(key)+" Text: "+self.vertex_info[key])
            # print("--------------------------------------------------")
        print("AVG " + count /i )



