from pyecharts.charts import Graph as Graph2
from pyecharts import options as opts
from py2neo import Graph
import json

neo = None


def initNeo():
    try:
        global neo
        # new version of py2neo
        neo = Graph("http://localhost:7474", auth=("neo4j","123456"))
    except Exception as e:
        print(e)

initNeo()

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


    #nodesCategory = [{"name":i,"symbolSize": 30,"category":1} for i in category[2:]]

    #links = [{"source": root, "target": i,"value":"1"} for i in category[2:]]

    #nodes =  nodesCategory

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
            label_opts=opts.LabelOpts(position="bottom"),
            edge_label=opts.LabelOpts(
                is_show=True, position="middle", formatter="{c}"
            )
            
        )
        .set_global_opts(title_opts=opts.TitleOpts(title=root+"-知识图谱"),
        legend_opts=opts.LegendOpts(orient="horizontal", pos_left="center", pos_top="5%"))
    )
    c.width = "800px"
    c.height = "600px"
    return c.render_embed()

def selectDisease(input):
    data = getInfoOfDisease(input)
    re = process4echarts(input,data)
    return re