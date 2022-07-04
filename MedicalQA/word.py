from py2neo import Graph
from pyecharts.charts import Graph as Graph2
from pyecharts import options as opts
import pandas as pd
import json
import numpy as np
import os
import jieba

neo = ""
# symptom
symptom = []
disease = []

def initSymptom():
    global symptom
    global disease
    with open("./dict/symptom.txt") as f:
        a = f.readlines()
        for i in a:
            symptom.append(str(i).split('\n')[0])
    symptom = np.array(symptom)
    with open("./dict/disease.txt") as f:
        a = f.readlines()
        for i in a:
            disease.append(str(i).split('\n')[0])
    disease = np.array(disease)

def initNeo():
    with open("./static/json/sql.json","r") as f:
        try:
            data = json.load(f)
            global neo
            # new version of py2neo
            neo = Graph("http://localhost:7474", auth=(
                        data["neo4j"]['user'],
                        data["neo4j"]['password']))
        except Exception as e:
            print(e)

# get info from symptom
#input: info of disease
#return: list[]
def getDiseaseFromSymptom(symptom):
    global neo
    txt = "MATCH (n:Symptom)-[r]-(m:Disease) WHERE n.name = "
    if len(symptom) == 0:
        return
    elif len(symptom) == 1:
        txt += "\"" + symptom + "\""
    else:
        txt += "\"" + symptom[0] + "\""
        for i in symptom[1:]:
            txt += " AND n.name = \"" + i + "\""

    txt += " RETURN m LIMIT 250"

    data = neo.run(txt).to_data_frame()

    dataDict = []
    if len(data) == 0:
        return dataDict

    for i in data['m']:
        dataDict.append(dict(i)['name'])

    return dataDict

# get disease
# input: symptom of disease
# return: dict(information of Dosease)
def getInfoOfDisease(Disease):
    global neo
    data = neo.run("MATCH (n)-[r]-(m:Disease{name:\""+Disease+"\"}) RETURN n,r LIMIT 250").to_data_frame()
    dataDict = {}
    #print(data)
    for i in range(len(data['n'])):
        dataDict[dict(data.iloc[i,0])['name']] = dict(data.iloc[i,1])['name']

    return dataDict

def process4echarts(root,data):
    category = ["病症"]
    for i in data:
        if data[i] not in category:
            category.append(data[i])
    rootNode = {"name":root , "symbolSize": 30,"category":0}
    nodes = [{"name":i,"symbolSize": 30,"category":category.index(data[i])} for i in data]

    category = [{"name":i} for i in category]

    nodes.insert(0,rootNode)
    links = [
        {"source": root, "target": i,"value":data[i]} for i in data
    ]

    c = (
        Graph2()
        .add("", nodes, links,category, repulsion=8000,
            #linestyle_opts=opts.LineStyleOpts(color="red"),
            label_opts=opts.LabelOpts(position="right"),
            edge_label=opts.LabelOpts(
                is_show=True, position="middle", formatter="{c}"
            )
            
        )
        .set_global_opts(title_opts=opts.TitleOpts(title=root+"-知识图谱"),
        legend_opts=opts.LegendOpts(orient="vertical", pos_left="2%", pos_top="20%"))
    )
    c.width = "600px"
    c.height = "600px"
    return c.render_embed()

# load dict for jieba
def cutLoad():
    for i,j,k in os.walk('./dict/'):
        for l in k:
            jieba.load_userdict("./dict/"+l)

# use cut
def cutString(input):
    result = jieba.lcut_for_search(input)
    return result

def AI(input):
    global symptom,disease,neo

    if len(symptom) == 0 or len(disease) == 0:
        initSymptom()
    if neo == "":
        initNeo()

    res = []
    sym = []#存储病症
    dis = []#存储病
    data = ""
    re = ""
    result = ""

    # 等待分词处理
    result = cutString(input)
    print(result)

    #print(result)
    for i in result:
        if i in symptom:
            sym.append(i)
        elif i in disease:
            dis.append(i)
    
    print(len(dis),len(sym))
    
    # Disease
    if len(dis) == 1:
        data = getInfoOfDisease(dis[0])
        re = process4echarts(dis[0],data)
    elif len(dis) > 1:
        result = dis

    # Symptom
    if len(sym) == 1:
        sym = getDiseaseFromSymptom(sym)
    elif len(sym) > 1:
        dis = getDiseaseFromSymptom(sym)
        if len(dis) == 0:
            tempList = []
            for i in sym:
                tempList.append(getDiseaseFromSymptom(i))
            dis = tempList

    
    #response = (res,result,sym,dis,re)

    response = str(sym)

    return response