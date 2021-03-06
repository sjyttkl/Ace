#encoding=utf-8

import jieba
jieba.load_userdict("userdict.txt")
jieba.enable_parallel(2) # 开启并行分词模式，参数为并行进程数
import re
import sys
import codecs
import cPickle

debug=False
_DEBUG_TIME_=True

if _DEBUG_TIME_:
    import time

class CATEGORY:
    class INWORD:
        def __init__(self):
            self.incount=0
            self.weight=0.0
    def __init__(self):
        self.inwords={}
        self.count_sample=0
class INWORD:
    def __init__(self):
        self.incount=0
        self.weight=0.0

class WORD:
    def __init__(self):
        self.incategorys={}
        self.count=0

f_parameter_words=open('parameter_words.dat','rb')
f_parameter_categorys=open('parameter_categorys.dat','rb')
f_test=codecs.open('test.data','r')
f_testanswer=codecs.open('testanswer.data','w',"utf-8")

print "读取参数配置文件..."
words=cPickle.load(f_parameter_words)
categorys=cPickle.load(f_parameter_categorys)

dr="【|】|[|]|（|）|\(|\)|-|\+|/|\\\|~|\*".decode("utf-8")
print "读取停止词..."
stopwords={line.strip().decode("utf-8") for line in open('stopwords.txt').readlines()}  #读取停止词文件并保存到列表stopwords

if __name__=='__main__':
    #if debug:
        #for w in words:
         #   for c in words[w].incategorys:
          #      print w,c,categorys[c].inwords[w].incount,words[w].count,categorys[c].inwords[w].weight
    print "正在生成测试文件..."
    count_read=0
    total_time=0.0
    for s in f_test:
        count_read+=1
        ''''
        if debug:
            print "测试样本数 ："+"%d"%count_read
        '''
        if _DEBUG_TIME_:
            temp_time=time.clock()
        ss=re.split(dr,s)
        scores={}
        for sss in ss:
            #result=jieba.cut(sss, cut_all=True)
            result=jieba.cut(sss)
            for r in result :
                if r not in stopwords and r!=" " and r!='\n' and r!="" and words.has_key(r):
                    for c in words[r].incategorys:
                        #if 1.0*categorys[c].inwords[r].incount/categorys[c].count_sample > 0.02:
                            if not scores.has_key(c):
                                scores[c]=0.0
                            scores[c]+=categorys[c].inwords[r].weight
                            if debug:
                                if count_read==1:
                                    if c=="381" or c=="869":
                                        print r,c,categorys[c].inwords[r].weight,1.0*categorys[c].inwords[r].incount/categorys[c].count_sample
                
        
        if debug:
            if count_read==1:
                print s,": "
                for c in scores:
                    if c=="381" or c=="869":
                        print "\t"+c+" "+'%f'%scores[c]
                    #print c+" "+'%f'%scores[c]+" \\",
                #print ""
        
        score_max=max(scores.values())
        for c in scores:
            if scores[c]==score_max:
                category=c
                break
        if _DEBUG_TIME_:
            total_time+=time.clock()-temp_time
            #print str(total_time)
        #d=dict([(k,v) for k,v in scores.items() if v==max(scores.values())])
        #print category
        f_testanswer.write(category+"\n")
    print "测试文件testanswer.data生成完毕"
    print "平均每个测试用例耗时 ："+"%f"%(total_time/count_read*1000)+"ms"

f_parameter_words.close()
f_parameter_categorys.close()
f_test.close()
f_testanswer.close()