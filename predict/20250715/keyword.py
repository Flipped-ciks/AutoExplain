import jieba.analyse

question = "下列属于系统软件的是（） Windows Excel Photoshop Word"
keywords = jieba.analyse.extract_tags(question, topK=5)
print("关键词：", keywords)