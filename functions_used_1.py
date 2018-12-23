
# coding: utf-8

# In[1]:

#import libraries
from collections import defaultdict , Counter ,OrderedDict, deque
import json
import gzip
import networkx as nx
from tqdm import tqdm_notebook as tqdm
from collections import deque, defaultdict
from tqdm import tqdm_notebook as tqdm
import gzip
import functools
import json
import functionhw5
import time


# In[5]:

#COMPUTATION of distances from source node s to all other nodes of the graph
def BFS_13(adj,s):
    #adj: adjacency list describing a graph
    #source node 
    #return dictionary with distances
    color=defaultdict(str)
    d=defaultdict(int)
    #assign color white(unvisited) to all nodes
    for i in list(adj.keys()):
        
        color[i]="W"
    #once a node is visited is assigned color grey    
    color[s]="G" 
    d[s]=0
    #creation of queue
    Q=deque([s])
    #loop until queue is empty going through all nodes of the graph
    while Q:
        try:
            a=Q.popleft()
            for k in adj[a]:
                if (color[k]=="W"):
                    color[k]="G"
                    d[k]=d[a]+1
                    Q.append(k)
        except:
            pass

            
    return d

def median(list_c0,list_ci,list_inter):
    #list_c0: input category
    #list_ci: other category
    #list_inter: list with values
    n_of_elements=len(list_ci)*len(list_c0)
    if len(list_inter)>n_of_elements/2:
        list_inter.sort()
        n=int(n_of_elements/2)
        if n_of_elements%2==0:
         
            return (list_inter[n]+list_inter[n+1])/2
        else:
            
            return list_inter[n]
    else:
        return "999999999999999999"


#Remove repeated articles from the one which is not closest to the input category 
def categories_clean(ordered_list,category_dict):
    #ordered list:block ranking
    #category_dict:dictionary whose keys are the names of the categories and values are lists with all the articles
    union_1=set([])
    LIST=list(ordered_list)
    LIST.remove(LIST[0])
    LIST1=list(ordered_list)
    LIST1.remove(LIST1[len(LIST1)-1])
    ejempl=[]
    for i in tqdm(range(len(LIST))):
        union_1.update(category_dict[LIST1[i]])
        intersection_1=set(category_dict[LIST[i]])-union_1
        ejempl.append(intersection_1)
    ejempl.insert(0,set(category_dict[LIST1[0]]))
    qw=list(map(list,ejempl))

    return  qw

#CREATION of lists with nodes considered in each step
def step_creation(lista):
#lista: list with nodes in each category without repeated elements
    aux=[]
    step=[]
    for i in tqdm(lista):
        aux+=i
        step.append([e for e in aux])
    return step

#CREATION of block creation
def block_ranking_creation(category_dict, BFS_result,input_category):
    #category_dict_2: dictionary with articles ordered by categories
    #BFS_result: dictionary with distances to all other nodes
    #input_category:name with category creation
    p=list(category_dict.keys())
    distance=deque([])
    distance=defaultdict(int)
    #remove input category(always first) from median computation 
    p.remove(input_category)
    for i in tqdm(p):
        #group results from BFS by categories
        bd={k:v for k,v in BFS_result.items() if int(k) in category_dict[i]}
        u=deque([])
        for j in tqdm(list(bd.values())):
                u.extend(j)
        u=sorted(u)
        #compute the median from every category and store them in a dictionary
        distance[i]=median(category_dict[input_category],category_dict[i],u)
        #input category added with value -1, so it is the first in the block ranking
    distance[input_category]=-1
    
    return  OrderedDict(sorted(distance.items(), key=lambda t: float(t[1])))


#Returns lists with dictionary with the articles ordered by category
def articles_order(m,categories, steps_it):
    #m: adjacency list of the graph
    #categories: categories without repeated elements
    #steps_it: list with nodes considered in each iteration
    
    #creation of graph using the adjacency list
    DG=nx.DiGraph(m)
    #initially providing all edges weight 1
    nx.set_edge_attributes(DG,'weight',1)
    A=deque([])
    step_storage=defaultdict(dict)
    n=0
    #creation of a dictionary whose keys are the number of the category in the block ranking and the value each one of the subgraphs
    for i in tqdm(steps_it):
        step_storage[n]=DG.subgraph(steps_it[n])
        n+=1
    n=0
    for i in tqdm(categories):
        #compute weight for nodes in the subgraph
        A.append(step_storage[n].in_degree(i,weight='weight'))

        aux=deque([])
        #set weights to the edges for each iteration
        for j in tqdm(i):
            aux.extend([(k[0],k[1], step_storage[n].in_degree(j,'weight')) for k in DG.out_edges(j)])
        DG.add_weighted_edges_from(aux)
        n+=1
    
    return A

