import time
from tqdm import tqdm
from py2neo import Graph, Node, Relationship

graph = Graph(
    "http://localhost:7474",
    username="neo4j",
    password="netease-0114"
)
graph.delete_all()
t = 0
entity_cnt = 1
entity_dict = {}
relation_list = []
node_dict = {}
with open('../data/kbqa.kb','r', encoding='utf-8') as f:
    line = f.readline()
    while line:
        if t>10000: break
        t += 1
        temp = line.replace('\n', '').split('|||')
        assert len(temp) == 3, "length of the tripe (%s) is not 3 but %d " % (line, len(temp))
        for it in [temp[0].strip(), temp[-1].strip()]:
            if entity_dict.get(it, -1) == -1:
                entity_dict[it] = entity_cnt
                entity_cnt += 1
        relation_list.append([it.strip() for it in temp])
        line = f.readline()
print("load finish")
for key in tqdm(entity_dict.keys()):
    tmp = Node('N%d'% entity_dict[key], name=key)
    node_dict[key] = tmp
    graph.create(tmp)
print("create node finish")
for it in tqdm(relation_list):
    graph.create(Relationship(node_dict[it[0]], it[1], node_dict[it[2]]))
