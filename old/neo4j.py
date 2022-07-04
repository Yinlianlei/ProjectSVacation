#!/usr/bin/env python3
# coding: utf-8
# File: MedicalGraph.py
# Author: lhy<lhy_in_blcu@126.com,https://huangyong.github.io>
# Date: 18-10-3

import os
import json
from py2neo import Graph,Node


'''

neo = ""


def test4neo():
    #node1 = Node("Person",name="test1")
    #node2 = Node("Person",name="test2")
    #r = Relationship(node1,"wifi",node2)
    #neo.create(r)
    global neo
    # node
    # data = neo.run("MATCH (n) RETURN n LIMIT 25").to_table()
    # relationship
    data = neo.run("MATCH ()-[r]->() RETURN r LIMIT 20").data()
    print(data)

# 遍历节点, 获取病症信息
def getDisser(input):
    global neo
    data = neo.run("MATCH (n:disser {name:\""+input+"\"})-[r*..4]->(m) return n,r,m LIMIT 100").data()
    print(data)
    
#create nodes.json
def processJson():
    with open('./static/medical.json','r') as f:
        testList = []
        try:
            for i in f.readlines():
                txt = json.loads(i)
                txt = txt['category']
                if txt == []:
                    continue
                if len(txt) == 1:
                    testList.append(txt[0])
                    continue
                elif len(txt) == 2:
                    testList.append(str(txt[1]))
                    continue
                testList.append(str(txt[1])+":"+str(txt[2]))
            testList = np.unique(testList)
            print(testList)
        except:
            print(i)

        nodes = {"疾病百科":[]}
        for i in testList:
            txt = i.split(":")
            if len(txt) == 1:
                nodes["疾病百科"].append({i:[]})
            else:
                nodes["疾病百科"].append({txt[0]:txt[1]})
        
        print(nodes)
        nodes = json.dumps(nodes,ensure_ascii=False)
        with open('./static/node.json','w') as f:
            f.write(nodes)

#add node dor neo4j
def addNode1(nodeList,relationList,rootNode,nodes,nodeName,method="-"):
    if nodeName not in nodes:
        return nodeList,relationList
    nodeSym = Node(nodeName,name=nodeName)
    for j in nodes[nodeName]:
        node = Node(nodeName[:4],name=j)
        relationList.append(Relationship(nodeSym,method,node))
        nodeList.append(node)
    nodeList.append(nodeSym)
    relationList.append(Relationship(rootNode,nodeName,nodeSym))
    return nodeList,relationList

def addNode2(nodeList,relationList,rootNode,nodes,nodeName,method="-"):
    if nodeName not in nodes:
        return nodeList,relationList
    node = [Node(nodeName,name=j) for j in nodes[nodeName]]
    for j in node:
        nodeList.append(j)
    for j in range(1,len(node)):
        relationList.append(Relationship(node[j-1],method,node[j]))
    relationList.append(Relationship(rootNode,nodeName,node[0]))
    return nodeList,relationList

def processNodes():
    with open("./static/medical.json",'r') as f:
        global neo
        nodes = f.read()
        #print(nodes)
        nodes = json.loads(nodes)
        #neo.create(nodeRoot)
        try:
            for i in nodes:
                createNode = []
                createRelation = []
                nodeDisser = Node("disser",name=i['name'])
                nodeLabelList = ["yibao_status",'get_prob','get_way','cure_lasttime','cured_prob','desc']
                for j in nodeLabelList:
                    if j in i:
                        nodeDisser.add_label(j)
                createNode.append(nodeDisser)

                nodePrevent = Node("preventNode",name="preventNode")
                for j in i['prevent'].split('\n'):
                    node = Node('prevent',method=j)
                    createRelation.append(Relationship(nodePrevent,"method",node))
                    createNode.append(node)
                createNode.append(nodePrevent)
                createRelation.append(Relationship(nodeDisser,"prevent",nodePrevent))

                createNode,createRelation = addNode2(createNode,createRelation,nodeDisser,i,'category')
                createNode,createRelation = addNode2(createNode,createRelation,nodeDisser,i,'cure_department')

                createNode,createRelation = addNode1(createNode,createRelation,nodeDisser,i,'symptom')
                createNode,createRelation = addNode1(createNode,createRelation,nodeDisser,i,'acompany')
                createNode,createRelation = addNode1(createNode,createRelation,nodeDisser,i,'check')
                createNode,createRelation = addNode1(createNode,createRelation,nodeDisser,i,'cure_way','method')
                createNode,createRelation = addNode1(createNode,createRelation,nodeDisser,i,'do_eat')
                createNode,createRelation = addNode1(createNode,createRelation,nodeDisser,i,'not_eat')
                createNode,createRelation = addNode1(createNode,createRelation,nodeDisser,i,'recommand_eat')
                createNode,createRelation = addNode1(createNode,createRelation,nodeDisser,i,'recommand_drug')
                createNode,createRelation = addNode1(createNode,createRelation,nodeDisser,i,'drug_detail')
            
                sub = Subgraph(createNode,createRelation)
                t = neo.begin()
                t.create(sub)
                neo.commit(t)
        except Exception as e:
            print(e)
            print(i)

def initNeo():
    with open("./static/sql.json","r") as f:
        try:
            data = json.load(f)
            global neo
            # new version of py2neo
            neo = Graph("http://localhost:7474", auth=(
                        data["neo4j"]['user'],
                        data["neo4j"]['password']))
        except Exception as e:
            print(e.with_traceback())
'''



class MedicalGraph:
    def __init__(self):
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        self.data_path = os.path.join(cur_dir, 'data/medical.json')
        with open("./static/sql.json","r") as f:
            try:
                data = json.load(f)
                global neo
                # new version of py2neo
                self.g = Graph("http://localhost:7474", auth=(
                            data["neo4j"]['user'],
                            data["neo4j"]['password']))
            except Exception as e:
                print(e.with_traceback())
        '''
        self.g = Graph(
            host="127.0.0.1",  # neo4j 搭载服务器的ip地址，ifconfig可获取到
            http_port=7474,  # neo4j 服务器监听的端口号
            user="neo4j",  # 数据库user name，如果没有更改过，应该是neo4j
            password="123456")
        '''

    '''读取文件'''
    def read_nodes(self):
        # 共７类节点
        drugs = [] # 药品
        foods = [] #　食物
        checks = [] # 检查
        departments = [] #科室
        producers = [] #药品大类
        diseases = [] #疾病
        symptoms = []#症状

        disease_infos = []#疾病信息

        # 构建节点实体关系
        rels_department = [] #　科室－科室关系
        rels_noteat = [] # 疾病－忌吃食物关系
        rels_doeat = [] # 疾病－宜吃食物关系
        rels_recommandeat = [] # 疾病－推荐吃食物关系
        rels_commonddrug = [] # 疾病－通用药品关系
        rels_recommanddrug = [] # 疾病－热门药品关系
        rels_check = [] # 疾病－检查关系
        rels_drug_producer = [] # 厂商－药物关系

        rels_symptom = [] #疾病症状关系
        rels_acompany = [] # 疾病并发关系
        rels_category = [] #　疾病与科室之间的关系


        count = 0
        for data in open(self.data_path):
            disease_dict = {}
            count += 1
            print(count)
            data_json = json.loads(data)
            disease = data_json['name']
            disease_dict['name'] = disease
            diseases.append(disease)
            disease_dict['desc'] = ''
            disease_dict['prevent'] = ''
            disease_dict['cause'] = ''
            disease_dict['easy_get'] = ''
            disease_dict['cure_department'] = ''
            disease_dict['cure_way'] = ''
            disease_dict['cure_lasttime'] = ''
            disease_dict['symptom'] = ''
            disease_dict['cured_prob'] = ''

            if 'symptom' in data_json:
                symptoms += data_json['symptom']
                for symptom in data_json['symptom']:
                    rels_symptom.append([disease, symptom])

            if 'acompany' in data_json:
                for acompany in data_json['acompany']:
                    rels_acompany.append([disease, acompany])

            if 'desc' in data_json:
                disease_dict['desc'] = data_json['desc']

            if 'prevent' in data_json:
                disease_dict['prevent'] = data_json['prevent']

            if 'cause' in data_json:
                disease_dict['cause'] = data_json['cause']

            if 'get_prob' in data_json:
                disease_dict['get_prob'] = data_json['get_prob']

            if 'easy_get' in data_json:
                disease_dict['easy_get'] = data_json['easy_get']

            if 'cure_department' in data_json:
                cure_department = data_json['cure_department']
                if len(cure_department) == 1:
                     rels_category.append([disease, cure_department[0]])
                if len(cure_department) == 2:
                    big = cure_department[0]
                    small = cure_department[1]
                    rels_department.append([small, big])
                    rels_category.append([disease, small])

                disease_dict['cure_department'] = cure_department
                departments += cure_department

            if 'cure_way' in data_json:
                disease_dict['cure_way'] = data_json['cure_way']

            if  'cure_lasttime' in data_json:
                disease_dict['cure_lasttime'] = data_json['cure_lasttime']

            if 'cured_prob' in data_json:
                disease_dict['cured_prob'] = data_json['cured_prob']

            if 'common_drug' in data_json:
                common_drug = data_json['common_drug']
                for drug in common_drug:
                    rels_commonddrug.append([disease, drug])
                drugs += common_drug

            if 'recommand_drug' in data_json:
                recommand_drug = data_json['recommand_drug']
                drugs += recommand_drug
                for drug in recommand_drug:
                    rels_recommanddrug.append([disease, drug])

            if 'not_eat' in data_json:
                not_eat = data_json['not_eat']
                for _not in not_eat:
                    rels_noteat.append([disease, _not])

                foods += not_eat
                do_eat = data_json['do_eat']
                for _do in do_eat:
                    rels_doeat.append([disease, _do])

                foods += do_eat
                recommand_eat = data_json['recommand_eat']

                for _recommand in recommand_eat:
                    rels_recommandeat.append([disease, _recommand])
                foods += recommand_eat

            if 'check' in data_json:
                check = data_json['check']
                for _check in check:
                    rels_check.append([disease, _check])
                checks += check
            if 'drug_detail' in data_json:
                drug_detail = data_json['drug_detail']
                producer = [i.split('(')[0] for i in drug_detail]
                rels_drug_producer += [[i.split('(')[0], i.split('(')[-1].replace(')', '')] for i in drug_detail]
                producers += producer
            disease_infos.append(disease_dict)
        return set(drugs), set(foods), set(checks), set(departments), set(producers), set(symptoms), set(diseases), disease_infos,\
               rels_check, rels_recommandeat, rels_noteat, rels_doeat, rels_department, rels_commonddrug, rels_drug_producer, rels_recommanddrug,\
               rels_symptom, rels_acompany, rels_category

    '''建立节点'''
    def create_node(self, label, nodes):
        count = 0
        for node_name in nodes:
            node = Node(label, name=node_name)
            self.g.create(node)
            count += 1
            print(count, len(nodes))
        return

    '''创建知识图谱中心疾病的节点'''
    def create_diseases_nodes(self, disease_infos):
        count = 0
        for disease_dict in disease_infos:
            node = Node("Disease", name=disease_dict['name'], desc=disease_dict['desc'],
                        prevent=disease_dict['prevent'] ,cause=disease_dict['cause'],
                        easy_get=disease_dict['easy_get'],cure_lasttime=disease_dict['cure_lasttime'],
                        cure_department=disease_dict['cure_department']
                        ,cure_way=disease_dict['cure_way'] , cured_prob=disease_dict['cured_prob'])
            self.g.create(node)
            count += 1
            print(count)
        return

    '''创建知识图谱实体节点类型schema'''
    def create_graphnodes(self):
        Drugs, Foods, Checks, Departments, Producers, Symptoms, Diseases, disease_infos,rels_check, rels_recommandeat, rels_noteat, rels_doeat, rels_department, rels_commonddrug, rels_drug_producer, rels_recommanddrug,rels_symptom, rels_acompany, rels_category = self.read_nodes()
        self.create_diseases_nodes(disease_infos)
        self.create_node('Drug', Drugs)
        print(len(Drugs))
        self.create_node('Food', Foods)
        print(len(Foods))
        self.create_node('Check', Checks)
        print(len(Checks))
        self.create_node('Department', Departments)
        print(len(Departments))
        self.create_node('Producer', Producers)
        print(len(Producers))
        self.create_node('Symptom', Symptoms)
        return


    '''创建实体关系边'''
    def create_graphrels(self):
        Drugs, Foods, Checks, Departments, Producers, Symptoms, Diseases, disease_infos, rels_check, rels_recommandeat, rels_noteat, rels_doeat, rels_department, rels_commonddrug, rels_drug_producer, rels_recommanddrug,rels_symptom, rels_acompany, rels_category = self.read_nodes()
        self.create_relationship('Disease', 'Food', rels_recommandeat, 'recommand_eat', '推荐食谱')
        self.create_relationship('Disease', 'Food', rels_noteat, 'no_eat', '忌吃')
        self.create_relationship('Disease', 'Food', rels_doeat, 'do_eat', '宜吃')
        self.create_relationship('Department', 'Department', rels_department, 'belongs_to', '属于')
        self.create_relationship('Disease', 'Drug', rels_commonddrug, 'common_drug', '常用药品')
        self.create_relationship('Producer', 'Drug', rels_drug_producer, 'drugs_of', '生产药品')
        self.create_relationship('Disease', 'Drug', rels_recommanddrug, 'recommand_drug', '好评药品')
        self.create_relationship('Disease', 'Check', rels_check, 'need_check', '诊断检查')
        self.create_relationship('Disease', 'Symptom', rels_symptom, 'has_symptom', '症状')
        self.create_relationship('Disease', 'Disease', rels_acompany, 'acompany_with', '并发症')
        self.create_relationship('Disease', 'Department', rels_category, 'belongs_to', '所属科室')

    '''创建实体关联边'''
    def create_relationship(self, start_node, end_node, edges, rel_type, rel_name):
        count = 0
        # 去重处理
        set_edges = []
        for edge in edges:
            set_edges.append('###'.join(edge))
        all = len(set(set_edges))
        for edge in set(set_edges):
            edge = edge.split('###')
            p = edge[0]
            q = edge[1]
            query = "match(p:%s),(q:%s) where p.name='%s'and q.name='%s' create (p)-[rel:%s{name:'%s'}]->(q)" % (
                start_node, end_node, p, q, rel_type, rel_name)
            try:
                self.g.run(query)
                count += 1
                print(rel_type, count, all)
            except Exception as e:
                print(e)
        return

    '''导出数据'''
    def export_data(self):
        Drugs, Foods, Checks, Departments, Producers, Symptoms, Diseases, disease_infos, rels_check, rels_recommandeat, rels_noteat, rels_doeat, rels_department, rels_commonddrug, rels_drug_producer, rels_recommanddrug, rels_symptom, rels_acompany, rels_category = self.read_nodes()
        f_drug = open('drug.txt', 'w+')
        f_food = open('food.txt', 'w+')
        f_check = open('check.txt', 'w+')
        f_department = open('department.txt', 'w+')
        f_producer = open('producer.txt', 'w+')
        f_symptom = open('symptoms.txt', 'w+')
        f_disease = open('disease.txt', 'w+')

        f_drug.write('\n'.join(list(Drugs)))
        f_food.write('\n'.join(list(Foods)))
        f_check.write('\n'.join(list(Checks)))
        f_department.write('\n'.join(list(Departments)))
        f_producer.write('\n'.join(list(Producers)))
        f_symptom.write('\n'.join(list(Symptoms)))
        f_disease.write('\n'.join(list(Diseases)))

        f_drug.close()
        f_food.close()
        f_check.close()
        f_department.close()
        f_producer.close()
        f_symptom.close()
        f_disease.close()

        return



if __name__ == '__main__':
    handler = MedicalGraph()
    print("step1:导入图谱节点中")
    handler.create_graphnodes()
    print("step2:导入图谱边中")      
    handler.create_graphrels()