import csv

import sematch.sematch.semantic.similarity as smch
from nltk.corpus import stopwords
from similarity_maxtrix import matrix


class search():

    def __init__(self):
        matrix_obj = matrix()
        self.Similarity_matrix = matrix_obj.edge_matrix()
        self.Similarity_matrix_class = matrix_obj.class_matrix()
        self.wns = smch.WordNetSimilarity()

    def get_sim_between_2_edges(self, edge1, edge2):
        if edge2 in self.Similarity_matrix[edge1].keys():
            return self.Similarity_matrix[edge1][edge2]
        else:
            return self.Similarity_matrix[edge2][edge1]

    def get_type_sim(self, type1, type2):
        return self.Similarity_matrix_class[type1][type2]

    def first_similar_node(self, code_graph, query_text, query_graph):
        similarity_function = self.get_sim_between_2_nodes
        # print("Start finding the most similar vertex in the code graph to the first vertex of a query:")
        # print(str(query_text))
        max_similarity = 0
        node_id = -1
        for key in code_graph.vertex_info:
 #           if key == -4 or key == -9:
#                print()
            node_text = code_graph.vertex_info[key].split()
            type_1 = query_graph.get_type(-1)
            type_2 = code_graph.get_type(key)
            # print("[" + str(key) + "]: " + str(node_text) + " :: " + str(query_text))
            # print("similarity: " + str(similarity_function(node_text, query_text)))
            sim = (((similarity_function(node_text, query_text)) + self.get_type_sim(
                    type_1, type_2)))/ 2
            if sim > max_similarity:
                max_similarity = sim
                node_id = key
    #    print("The most similar node is: " + str(node_id))
      #  print()
        with open('first_similar_node.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([max_similarity, node_id])

        return [(max_similarity, node_id)]

    def next_similar_node(self, code_graph, query_text, query_arc, init_node, similarity_function, k, query_diagram,
                          id, is_visited_vertex, query_graph, id_query, th):
        # print("Start finding "+str(k)+" most similar vertices in the code graph to the vertex of a query:")
        # print(str(query_text))
        # print("The neighbors of vertex: " + str(init_node) + " are: " + str(code_graph.neighbors(init_node)))
        max_similarity = []
        for key in code_graph.neighbors(init_node):
            node_text = code_graph.vertex_info[key].split()
            node_arc = code_graph.arc_type(init_node, key)
            type_1 = query_diagram.get_type(id)
            type_2 = code_graph.get_type(key)
            similarity = (similarity_function(node_text, query_text) + self.get_sim_between_2_edges(node_arc,
                                                                                                    query_arc) + self.get_type_sim(
                type_1, type_2)) / 3
            # print("[" + str(key) + "]: " + str(node_text) + " :: " + str(query_text))
            # print("similarity: " + str(similarity))
            if similarity < th or is_visited_vertex[key]:
                continue
            if len(max_similarity) < k:
                max_similarity.append((similarity, key))
                max_similarity.sort(key=lambda tup: tup[0])
            elif similarity >= max_similarity[0][0]:
                del max_similarity[0]
                max_similarity.append((similarity, key))
                max_similarity.sort(key=lambda tup: tup[0])
        if len(max_similarity) == 0 and len(code_graph.neighbors(init_node)) != 0:
            for key in code_graph.neighbors(init_node):
                node_text = code_graph.vertex_info[key].split()
                node_arc = code_graph.arc_type(init_node, key)
                # similarity = (similarity_function(node_text, query_text) + get_sim_between_2_edges(node_arc,
                #                                                                                    "query_arc")) / 2
                similarity = (similarity_function(node_text, query_text)+ self.get_sim_between_2_edges(node_arc,
                                                                                                        query_arc) + self.get_type_sim(
                    type_1, type_2)) / 3
                if not is_visited_vertex[key]:
                    max_similarity.append((similarity, key))
        max_similarity.sort(key=lambda tup: tup[0])
        # print("The most similar node is: " + str(max_similarity))
        # print()
        with open('most_similar_node.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([max_similarity])
        return max_similarity

    def greedy_algorithm_recursive(self, nodelist, code_graph, query_graph, id_query, k, th, is_visited_vertex):
        results = {}
        if len(nodelist) == 0 or id_query * (-1) > query_graph.num_of_vertices():
            return results
        id_query = id_query - 1
        for tuple in nodelist:
            if is_visited_vertex[tuple[1]]:
                continue  # return resultscontinue#return results
            is_visited_vertex[tuple[1]] = True
            similar_nodes = self.next_similar_node(code_graph, query_graph.vertex_info[id_query + 1].split(),
                                                   query_graph.arc_type(id_query + 2, id_query + 1),
                                                   tuple[1], self.get_sim_between_2_nodes, k, query_graph, id_query + 1,
                                                   is_visited_vertex, query_graph, id_query + 1, th)
            results[tuple[1]] = similar_nodes

            if len(similar_nodes) == 0:
                result2 = self.greedy_algorithm_recursive(similar_nodes, code_graph, query_graph, id_query, k, th,
                                                          is_visited_vertex)
            else:
                if tuple[1] == similar_nodes[0][1] or nodelist == similar_nodes:
                    continue

                if similar_nodes[0][0] <= th:
                    result2 = self.greedy_algorithm_recursive(similar_nodes, code_graph, query_graph, id_query + 1, k,
                                                              th,
                                                              is_visited_vertex)
                else:
                    result2 = self.greedy_algorithm_recursive(similar_nodes, code_graph, query_graph, id_query, k, th,
                                                              is_visited_vertex)

            results.update(result2)

        return results

    def get_sim_between_2_nodes(self, node1, node2):
        # This function receives two nodes an returns the calculated semantic similarity between them.
        if node1 == node2:
            return 1
        stopwords_set = stopwords.words('english')
        node1 = list(set(node1) - set(stopwords_set))
        node2 = list(set(node2) - set(stopwords_set))
        sim = 0
        for word1 in node1:
            max = 0
            for word2 in node2:
                if word2 == word1:
                    add = 1
                else:
                    # if word1 not in self.wns.vocab or word2 not in self.wns.vocab:
                    #     add = 0.1
                    # else:
                    add = self.wns.word_similarity(word1, word2)  # model similarity # wns word_similarity
                if add > max:
                    max = add
                # add = add / len(node1) if len(node1) >= len(node2) else add / len(node2)
            sim = sim + max
        sim = sim / len(node1) if len(node1) >= len(node2) else sim / len(node2)

        return sim

    def get_sim_attributes(self, attributes1, attributes2):

        size_1 = len(attributes1)
        size_2 = len(attributes2)

        sim = 0

        if size_1 > size_2:
            lists_1 = attributes1
            lists_2 = attributes2
            weights = 1 / size_1
        else:
            lists_1 = attributes2
            lists_2 = attributes1
            weights = size_2

        for word1 in lists_1:
            max = 0
            for word2 in lists_2:
                if word2 == word1:
                    add = 1
                else:
                    # if word1 not in self.wns.vocab or word2 not in self.wns.vocab:
                    #     add = 0.1
                    # else:
                    add = self.wns.word_similarity(word1, word2)  # model similarity # wns word_similarity
                if add > max:
                    max = add
                # add = add / len(node1) if len(node1) >= len(node2) else add / len(node2)
            sim = sim + max * weights

        return sim
