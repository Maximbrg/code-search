from Diagram import Diagram as class_diagram
from greedy_search import search
import pandas as pd
import copy
import os
import numpy as np

#import read_from_cloud_storage


def print_all_path(to_print, path_dic, curr_node, diagram, similarity, i, results, url, is_visited_vertex):
    if curr_node not in path_dic.keys() or len(path_dic[curr_node]) == 0:
        results.append(
            (similarity / i, to_print + "" + str(diagram.vertex_text(curr_node)) + " Score: " + str(similarity / i), url
             ))

    else:
        for tuple in path_dic[curr_node]:
            if tuple[1] == curr_node:  # or is_visited_vertex[tuple[1]]:
                continue
            is_visited_vertex[tuple[1]] = True
            print_all_path(to_print + "" + str(diagram.vertex_text(curr_node)) + "->", path_dic, tuple[1], diagram,
                           similarity + tuple[0], i + 1, results, url, is_visited_vertex)


def print_results(results, info, post):
    i=1
    list1 = [str(info[1])]
    list2 = []
    final = []
    dic = {str(info[1]): info[0]}
    finished = False
    while not finished:
        finished = True
        for item in list1:
            if i == 1:
                list_ids = [info[1]]
                i = 0
            else:
                list_ids = item.split(',')
            idd = int(list_ids[len(list_ids)-1])
            if idd in results.keys():

                for info in results[idd]:
                    if str(info[1]) not in list_ids:
                        list2.append(str(item)+","+str(info[1]))
                        dic[str(item)+","+str(info[1])] = dic[str(item)] + info[0]
                        finished = False
                    else:
                        if str(item) not in final:
                            final.append(str(item))

        if not finished:
            list1 = copy.deepcopy(list2)
            list2 = []
    filtered = []
    for item1 in final:
        for item2 in final:
            if item1 != item2 and item1 in item2:
                if item1 not in filtered:
                    filtered.append(item1)
    abc = [item for item in final if item not in filtered]
    for key in abc:
        if key not in list1:
            list1.append(key)
    output = []
    for item in list1:
        path = ''
        split = item.split(',')
        i = 0
        for node in split:
            i += 1
            path = path + '->' + post.vertex_info[int(node)]
        output.append((path, dic[item] / i))

    return dic, list1, output


def split_query(query):
    i = 1
    list1 = [str(-1)]
    list2 = []
    final = []
    #dic = {str(info[1]): info[0]}
    finished = False
    while not finished:
        finished = True
        for item in list1:
            if i == 1:
                list_ids = [-1]
                i = 0
            else:
                list_ids = item.split(',')
            idd = int(list_ids[len(list_ids) - 1])
            if idd in query.graph.keys():

                for info in query.graph[idd]:
                    if str(info) not in list_ids:
                        list2.append(str(item) + "," + str(info))
                        #dic[str(item) + "," + str(info[1])] = dic[str(item)] + info[0]
                        finished = False
                    else:
                        if str(item) not in final:
                            final.append(str(item))

        if not finished:
            list1 = copy.deepcopy(list2)
            list2 = []
    filtered = []
    for item1 in final:
        for item2 in final:
            if item1 != item2 and item1 in item2:
                if item1 not in filtered:
                    filtered.append(item1)
    abc = [item for item in final if item not in filtered]
    for key in abc:
        if key not in list1:
            list1.append(key)
    return list1


def pathh(array):
    split = array.split(',')
    new_graph = {}
    for item in enumerate(split):
        if (int(item[1]) - 1)*-1 > len(split):
            new_graph[item[1]] = []
        else:
            new_graph[item[1]] = [split[item[0]+1]]
    return new_graph


search_component = search()
target_data = pd.read_csv("evaluation.csv")
target_results = {}
for index, row in target_data.iterrows():

    # if str(row['result2']) != 'nan' and str(row['result3']) != 'nan':
    #     target_results[row['query']] = (row['result1'], row['domain'], row['result2'], row['result3'])
    # elif str(row['result2']) != 'nan':
    #     target_results[row['query']] = (row['result1'], row['domain'], row['result2'])
    # else:
    #     target_results[row['query']] = (row['result1'], row['domain'])

    if str(row['result2']) != 'nan' and str(row['result3']) != 'nan':
        target_results[str(row['query'])+'.json'] = (row['result1'], row['domain'], row['result2'], row['result3'])
    elif str(row['result2']) != 'nan':
        target_results[str(row['query'])+'.json'] = (row['result1'], row['domain'], row['result2'])
    else:
        target_results[str(row['query'])+'.json'] = (row['result1'], row['domain'])


data_result_search = {}
for queryname in os.listdir("queries"): #OVER POST
    output = []

    query = class_diagram("queries/" + queryname)
    splited = split_query(query)
    for filename in os.listdir("data"): #OVER QUERY
        # if 'query3' in queryname:
        if 'h3' in queryname:
            bool = True
            counter = 0
            sum = 0
        else:
            bool = False

        if bool:
            output.append([])
            output.append([])
            output.append([])
            for item in splited:
                new_graph = pathh(item)
               # print(filename)
                post = class_diagram("data/" + filename)
                # post = class_diagram(read_from_cloud_storage().get_blobs())
                #todo
                query.update_query(new_graph)
                nodelist = search_component.first_similar_node(post, query.get_first_node().split(), query)
                visited_list = {}
                for key in post.vertex_info:
                    visited_list[key] = False
                results = search_component.greedy_algorithm_recursive(nodelist, post, query, -2, 2, 0.65, visited_list)
                #   draw.draw_class_diagran(results, post)
                dic, list1, printed_results = print_results(results, nodelist[0], post)
                print(printed_results)
                sum = sum + printed_results[len(printed_results) - 1][1]

                for item in list1:
                    numOfNodes = len(item.split(','))
                    output[counter].append((item, dic[item]/numOfNodes, filename))
                counter += 1
            #print("TOT similarity: " + str(sum / counter))

        else:
            #print(filename)
            post = class_diagram("data/" + filename)
            # print(filename)
            # todo
            # post = class_diagram(read_from_cloud_storage.get_blobs())
            nodelist = search_component.first_similar_node(post, query.get_first_node().split(), query)
            visited_list = {}
            for key in post.vertex_info:
                visited_list[key] = False
            results = search_component.greedy_algorithm_recursive(nodelist, post, query, -2, 2, 0.65, visited_list) # next_nude, k, tresh
            #   draw.draw_class_diagran(results, post)8
            dic, list1, printed_results = print_results(results, nodelist[0], post)
            # print(printed_results)
            for item in list1:
                numOfNodes = len(item.split(','))
                output.append((item, dic[item]/numOfNodes, filename))
    if bool:
        sorted_by_second = []
        for index, result in enumerate(output):

            sorted_by_second.append(sorted(output[index], key=lambda tup: tup[1]))
            sorted_by_second[index].reverse()

    else:
        sorted_by_second = sorted(output, key=lambda tup: tup[1])
        sorted_by_second.reverse()

    # print(printed_results)
    print(sorted_by_second)
    # print(sorted_by_second)
    data_result_search[queryname] = []
    j = 0

    if bool:
        data_result_search[queryname].append([])
        data_result_search[queryname].append([])
        data_result_search[queryname].append([])

        for part_item in sorted_by_second:
      #      try:

            i = 1
            for item in part_item:
                name1 = item[2]
                name2 = target_results[queryname][1] + '.json'
                if name1 == name2:
                    data_result_search[queryname][j].append(('domain', i))
                    a = item[0]
                    if j == 0:
                        b = target_results[queryname][0]
                    else:
                        b = target_results[queryname][j+1]
                    if a == b:
                        data_result_search[queryname][j].append(('exact', i, item[1]))
                i += 1
            j += 1
         #   except:
           #     print()

    else:
        i = 1
        for item in sorted_by_second:
            name1 = item[2]
            name2 = target_results[queryname][1]+'.json'
            if name1 == name2:
                data_result_search[queryname].append(('domain', i))
                a = item[0]
                b = target_results[queryname][0]
                if a == b:
                    data_result_search[queryname].append(('exact', i, item[1]))
            i += 1
#print("################################")
#for key in data_result_search.keys():
   # print(str(key) + ": " + str(data_result_search[key]))

avg_MRR_exact = 0
avg_MRR_domain = 0
avg_similarity = 0

i = 0
j = 0

for key in data_result_search.keys():
    if 'h3' not in key:
        isEntered_MRR_exact = False
        isEntered_exact_MRR_domain = False
        for result in data_result_search[key]:
          #  print(result)
            if result[0] == 'domain' and isEntered_exact_MRR_domain is False:
                avg_MRR_domain += 1/result[1]
                isEntered_exact_MRR_domain = True
            if result[0] == 'exact' and isEntered_MRR_exact is False:
                avg_MRR_exact += 1/result[1]
                avg_similarity += result[2]
                isEntered_MRR_exact = True
                j += 1
        i += 1
    else:
        for data in data_result_search[key]:
            isEntered_MRR_exact = False
            isEntered_exact_MRR_domain = False
            for result in data:
                #print(result)
                if result[0] == 'domain' and isEntered_exact_MRR_domain is False:
                    avg_MRR_domain += 1 / result[1]
                    isEntered_exact_MRR_domain = True
                if result[0] == 'exact' and isEntered_MRR_exact is False:
                    avg_MRR_exact += 1 / result[1]
                    avg_similarity += result[2]
                    isEntered_MRR_exact = True
                    j += 1
            i += 1


print("MRR exact " + str(avg_MRR_exact / i))
print("MRR domain " + str(avg_MRR_domain / i))
print("Similarity " + str(avg_similarity / j))










