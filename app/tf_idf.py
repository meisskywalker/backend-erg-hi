import pandas as pd
import math
import re


class Tf_Idf:
    def __init__(self, corpus: dict):
        self.uuids, self.corpus = corpus.keys(), list(corpus.values()) 
        self.corpus = self.clean_text()
        self.words_match = self.count_match()
        self.tfreq = self.transform_tf()
        self.idf = self.transform_idf()
        self.val_tfidf = self.transform_tfidf()


    def clean_w(self, word):
        # return re.split(" ", re.sub(r"[^\w\s]", "", word.lower()))
        return re.split(" ", re.sub(r"[^a-zA-Z\s]", "", word.lower()))

    def clean_text(self):
        return list(
            map(lambda w: self.clean_w(w), self.corpus)
        )

    def count_match(self):
        match = map(lambda w: {a: w.count(a) for a in w}, self.corpus)
        return {uuid: a for uuid, a in zip(self.uuids, match)}

    def words_in_each(self, key: str):
        return sum([key in a for a in self.corpus])

    def f_tfreq(self, val_word: int, doc_w: dict) -> float:
        return val_word / sum(doc_w.values())

    def f_idf(self, key: str) -> float:
        a = len(self.corpus)
        b = self.words_in_each(key)
        return math.log10(a / b)

    def transform_tf(self):
        _ret = {
            doc: {k: self.f_tfreq(v, doc_v) for k, v in doc_v.items()}
            for doc, doc_v in self.words_match.items()
        }
        return pd.DataFrame(_ret).fillna(0)

    def transform_idf(self):
        _ret = {
            doc: {k: self.f_idf(k) for k, _ in doc_v.items()}
            for doc, doc_v in self.words_match.items()
        }
        return pd.DataFrame(_ret).fillna(0)

    def transform_tfidf(self):
        return self.tfreq * self.idf

