import jieba.analyse
import difflib

# 输入模块
question = '乳腺癌的症状有哪些？'
keywords_list = jieba.analyse.extract_tags(question)
print("input:"+question)
print("keywords:")
print(keywords_list)
print()

# 关键词类型
# types = "unknown"

# 输出列表
# questions = []

# 1.生成各类关键词列表
# disease
f = open("disease.txt", "r", encoding="utf-8")  # 打开文件
disease = []
line = f.readline()
line = line[:-1]
while line:
    disease.append(line)
    line = f.readline()  # 读取一行文件，包括换行符
    line = line[:-1]  # 去掉换行符，也可以不去
f.close()  # 关闭文件
# drug
f = open("drug.txt", "r", encoding="utf-8")
drug = []
line = f.readline()
line = line[:-1]
while line:
    drug.append(line)
    line = f.readline()
    line = line[:-1]
f.close()
# symptom
f = open("symptom.txt", "r", encoding="utf-8")
symptom = []
line = f.readline()
line = line[:-1]
while line:
    symptom.append(line)
    line = f.readline()
    line = line[:-1]
f.close()
# food
f = open("food.txt", "r", encoding="utf-8")
food = []
line = f.readline()
line = line[:-1]
while line:
    food.append(line)
    line = f.readline()
    line = line[:-1]
f.close()
# check
f = open("check.txt", "r", encoding="utf-8")
check = []
line = f.readline()
line = line[:-1]
while line:
    check.append(line)
    line = f.readline()
    line = line[:-1]
f.close()


def question_ask_help(keyword):
    types = "unknown"
    questions = []
    # 2.判断搜索关键词类型,进行文本匹配
    # disease
    disease_list = difflib.get_close_matches(keyword, disease, n=1, cutoff=0.6)  # 相近词匹配
    if len(disease_list) != 0:
        keyword = disease_list[0]
        types = 'disease'

    # drug
    drug_list = difflib.get_close_matches(keyword, drug, n=1, cutoff=0.6)
    if len(drug_list) != 0:
        keyword = drug_list[0]
        types = 'drug'

    # symptom
    symptom_list = difflib.get_close_matches(keyword, symptom, n=1, cutoff=0.9)
    if len(symptom_list) != 0:
        keyword = symptom_list[0]
        types = 'symptom'

    # food
    food_list = difflib.get_close_matches(keyword, food, n=1, cutoff=0.6)
    if len(food_list) != 0:
        keyword = food_list[0]
        types = 'food'

    # check
    check_list = difflib.get_close_matches(keyword, check, n=1, cutoff=0.6)
    if len(check_list) != 0:
        keyword = check_list[0]
        types = 'check'

    # 3.根据关键词类型生成问题
    if types == "disease":
        # disease_desc
        q = keyword
        questions.append(q)
        # disease_symptom
        q = keyword + '的症状有哪些？'
        questions.append(q)
        # disease_cause
        q = '为什么有的人会得' + keyword + '?'
        questions.append(q)
        # disease_acompany
        q = keyword + '有哪些并发症？'
        questions.append(q)
        # disease_not_food
        q = keyword + '的人不要吃啥?'
        questions.append(q)
        # disease_do_food
        q = keyword + '的人吃点啥？'
        questions.append(q)
        # disease_drug
        q = keyword + '要吃啥药？'
        questions.append(q)
        # disease_check
        q = keyword + '怎么才能查出来？'
        questions.append(q)
        # disease_prevent
        q = '怎样才能预防？' + keyword + '?'
        questions.append(q)
        # disease_lasttime
        q = keyword + '要多久才能好？'
        questions.append(q)
        # disease_cureway
        q = keyword + '要怎么治？'
        questions.append(q)
        # disease_cureprob
        q = keyword + '能治好吗？'
        questions.append(q)
        # disease_easyget
        q = '什么人容易得' + keyword + '?'
        questions.append(q)

    if types == "drug":
        # drug_desc
        q = keyword
        questions.append(q)
        # drug_disease
        q = keyword + '能治啥病？'
        questions.append(q)

    if types == "symptom":
        # symptom_desc
        q = keyword
        questions.append(q)
        # symptom_disease
        q = keyword + '该怎么办？'
        questions.append(q)

    if types == "food":
        # food_desc
        q = keyword
        questions.append(q)
        # food_not_disease
        q = '哪些人最好不吃' + keyword + '？'
        questions.append(q)
        # food_do_disease
        q = keyword + '有什么好处？'
        questions.append(q)

    if types == "check":
        # check_desc
        q = keyword
        questions.append(q)
        # check_disease
        q = keyword + '能查出什么病？'
        questions.append(q)

    print("type:"+types)
    print("questions:")
    print(questions)


for i in keywords_list:
    print("keyword:"+i)
    question_ask_help(i)
    print()
