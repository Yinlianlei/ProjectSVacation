import gensim
import os

class word_vector:
    h5 = ""

    def __init__(self) -> None:
        if os.path.exists("./model/model.h5"):
            self.h5 = gensim.models.Word2Vec.load("./model/model.h5")
            print("exist")
            return
        symptom = []
        with open("./dict/symptom.txt") as f:
            a = f.readlines()
            for i in a:
                symptom.append([str(i).split('\n')[0]])
        self.h5 = gensim.models.Word2Vec(symptom, min_count=1, window=5,sg=1)
        self.h5.save("./model/model.h5")
        self.h5.wv.save_word2vec_format('./model/model.vector')

    # calculate the word vector of input
    def calculate(self,input):
        result = self.h5.wv.most_similar(input,topn=1)
        print(result)
        #result = self.h5.wv.similarity(input,input)
        #print(result)

if __name__ == "__main__":
    v = word_vector()
    v.calculate(["低烧","持续低烧"])
