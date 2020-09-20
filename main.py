from gensim import corpora, models
from gensim.similarities import SparseMatrixSimilarity
import jieba
import re
import numpy


def remove_punctuation(line):
    rule = re.compile(u"[^a-zA-Z0-9\u4e00-\u9fa5]")
    line = rule.sub('', line)
    return line


def main():
    save_path = 'C:/Users/john.keats/Desktop/out.txt'
    orig_path = 'C:/Users/john.keats/Desktop/orig.txt'
    orig_file = open(orig_path, 'r', encoding="utf-8")
    txt = orig_file.read()
    txt = remove_punctuation(txt)
    text = list(txt)
    orig_file.close()

    add_path = 'C:/Users/john.keats/Desktop/add.txt'
    add_file = open(add_path, 'r', encoding="utf-8")
    add_text = add_file.read()
    add_file.close()
    add_text = remove_punctuation(add_text)

    texts = []
    for line in text:
        words = ' '.join(jieba.lcut(line)).split(' ')
        texts.append(words)
    for line in texts:
        print(line)
    dictionary = corpora.Dictionary(texts)
    num_features = len(dictionary.token2id)
    print(dictionary)

    new_vec = dictionary.doc2bow(jieba.lcut(add_text))
    print(new_vec)
    corpus = [dictionary.doc2bow(text) for text in texts]
    tfidf = models.TfidfModel(corpus)
    print(tfidf)
    # 相似度计算
    tf_texts = tfidf[corpus]
    for i in tfidf[corpus]:
        print(i)
    tf_add = tfidf[new_vec]
    print(tf_add)
    sparse_matrix = SparseMatrixSimilarity(tf_texts, num_features)
    similarities = sparse_matrix.get_similarities(tf_add)
    print('\nTF-IDF模型的keyword稀疏向量：')
    print(tfidf[new_vec])
    print('\n相似度计算：')
    print('%.2f' % (numpy.max(similarities)))
    f = open(save_path, 'w', encoding="utf-8")
    f.write("相似的计算结果：%.2f" % (numpy.max(similarities)))


if __name__ == '__main__':
    main()
