from question_classifier import *
from question_parser import *
from answer_search import *

import time

'''问答类'''
class ChatBotGraph:
    def __init__(self):
        self.classifier = QuestionClassifier()
        self.parser = QuestionPaser()
        self.searcher = AnswerSearcher()

    def chat_main(self, sent):
        answer = '您好，我是小泽司机医药智能助理，目前暂无此方面数据，希望未来可以帮到您。'
        res_classify = self.classifier.classify(sent)
        if not res_classify:
            return answer
        res_sql = self.parser.parser_main(res_classify)
        final_answers = self.searcher.search_main(res_sql)
        if not final_answers:
            return answer
        else:
            return '\n'.join(final_answers)

def response(input):
    sendTime = time.strftime("%H:%M", time.localtime()) 
    txt = ""
    respnseHtml = '<div class="chat_right_item_1 clearfix">用户</div>'+\
        '<div class="chat_right_item_2">'+\
        '<div class="chat_right_time clearfix">'+sendTime+'</div>'+\
        '<div class="chat_right_content clearfix">'+txt+'</div>'+'</div>'

    return respnseHtml