from django.core import serializers
from django.db import models
from django.http.response import JsonResponse
from django.db import models
from django.db import connection
import json,datetime



class commonList:
    '''
    --公用方法
    --getModelData--获取数据库数据
    --dictfetchall--将游标返回的结果保存到一个字典对象中
    --getDateTime--将时间转换成字符串
    --getTimeTulpue--返回时间数组为开始时间到结束时间
    '''
    def __init__(self):
        pass
    def getDateTime(self,time):
        '''将时间转换成字符串'''
        startTime1=time.split("-")
        startTimeList=[]
        for i in startTime1:
            startTimeList.append(int(i))
        print('startTimeList',startTimeList)
        return startTimeList
    def getTimeTulpue(self,startTime,endTime):
        '''返回时间数组为开始时间到结束时间'''
        dataStart=self.getDateTime(startTime)
        dataEnd=self.getDateTime(endTime)
        datatimelist=[]
        dataStartTime=datetime.datetime.strptime(startTime,"%Y-%m-%d")#字符串转成datetime
        days=(datetime.datetime(dataEnd[0],dataEnd[1],dataEnd[2])-datetime.datetime(dataStart[0],dataStart[1],dataStart[2])).days
        for i in range(days+2):
            dataTime=dataStartTime+ datetime.timedelta(days=i)
            dataTimeToString=dataTime.strftime("%Y-%m-%d")
            datatimelist.append(dataTimeToString)
        return datatimelist
    def getModelData(self,varr):
        '''获取数据库数据'''
        cursor = connection.cursor()
        cursor.execute(varr)
        data=self.dictfetchall(cursor)
        return data
    def getSignModeldata(self,cursor,varr):
        '''获取指定数据库数据'''
        print("==getSignModeldata==获取到的数据",varr)
        cursor.execute(varr)
        data = self.dictfetchall(cursor)
        return data
    def dictParams(self,varr):
        '''序列化Json数据'''
        for i in varr:
            data=json.loads(i)

    def dictfetchall(self,varr):
        "将游标返回的结果保存到一个字典对象中"
        desc = varr.description
        return [dict(zip([col[0] for col in desc], row))for row in varr.fetchall()]
    # def dataRequest():
    def randomPhoneBase(self):
        "随机生成11位手机号"
        import  random
        preList=["130", "131", "132", "133", "134", "135", "136", "137", "138", "139",
             "147", "150", "151", "152", "153", "155", "156", "157", "158", "159",
             "186", "187", "188", "189"]
        return  random.choice(preList)+"".join(random.choice("0123456789") for i in range(8))
    def randomNameBase(self):
        "随机生成3位姓名"
        import random  as r
        xing='赵钱孙李周吴郑王冯陈褚卫蒋沈韩杨朱秦尤许何吕施张孔曹严华金魏陶姜戚谢邹喻柏水窦章云苏潘葛' \
           '奚范彭郎鲁韦昌马苗凤花方俞任袁柳酆鲍史唐费廉岑薛雷贺倪汤滕殷罗毕郝邬安常乐于时傅皮卞齐康' \
           '伍余元卜顾孟平黄和穆萧尹姚邵湛汪祁毛禹狄米贝明臧计伏成戴谈宋茅庞熊纪舒屈项祝董梁杜阮蓝闵' \
           '席季麻强贾路娄危江童颜郭梅盛林刁钟徐邱骆高夏蔡田樊胡凌霍虞万支柯昝管卢莫经房裘缪干解应宗' \
           '丁宣贲邓郁单杭洪包诸左石崔吉钮龚程嵇邢滑裴陆荣翁荀羊於惠甄曲家封芮羿储靳汲邴糜松井段富巫' \
           '乌焦巴弓牧隗山谷车侯宓蓬全郗班仰秋仲伊宫宁仇栾暴甘钭厉戎祖武符刘景詹束龙叶幸司韶郜黎蓟薄' \
           '印宿白怀蒲邰从鄂索咸籍赖卓蔺屠蒙池乔阴鬱胥能苍双闻莘党翟谭贡劳逄姬申扶堵冉宰郦雍卻璩桑桂' \
           '濮牛寿通边扈燕冀郏浦尚农温别庄晏柴瞿阎充慕连茹习宦艾鱼容向古易慎戈廖庾终暨居衡步都耿满弘' \
           '匡国文寇广禄阙东欧殳沃利蔚越夔隆师巩厍聂晁勾敖融冷訾辛阚那简饶空曾毋沙乜养鞠须丰巢关蒯相' \
           '查后荆红游竺权逯盖益桓公万俟司马上官欧阳夏侯诸葛闻人东方赫连皇甫尉迟公羊澹台公冶宗政濮阳' \
           '淳于单于太叔申屠公孙仲孙轩辕令狐钟离宇文长孙慕容鲜于闾丘司徒司空丌官司寇仉督子车颛孙端木' \
           '巫马公西漆雕乐正壤驷公良拓跋夹谷宰父谷梁晋楚闫法汝鄢涂钦段干百里东郭南门呼延归海羊舌微生' \
           '岳帅缑亢况郈有琴梁丘左丘东门西门商牟佘佴伯赏南宫墨哈谯笪年爱阳佟第五言福'
        ming = '伟刚勇毅俊峰强军平保东文辉力明永健世广志义兴良海山仁波宁贵福生龙元全国胜学祥才发武新利清' \
               '飞彬富顺信子杰涛昌成康星光天达安岩中茂进林有坚和彪博诚先敬震振壮会思群豪心邦承乐绍功松善' \
               '厚庆磊民友裕河哲江超浩亮政谦亨奇固之轮翰朗伯宏言若鸣朋斌梁栋维启克伦翔旭鹏泽晨辰士以建家' \
               '致树炎德行时泰盛秀娟英华慧巧美娜静淑惠珠翠雅芝玉萍红娥玲芬芳燕彩春菊兰凤洁梅琳素云莲真环' \
               '雪荣爱妹霞香月莺媛艳瑞凡佳嘉琼勤珍贞莉桂娣叶璧璐娅琦晶妍茜秋珊莎锦黛青倩婷姣婉娴瑾颖露瑶' \
               '怡婵雁蓓纨仪荷丹蓉眉君琴蕊薇菁梦岚苑筠柔竹霭凝晓欢霄枫芸菲寒欣滢伊亚宜可姬舒影荔枝思丽秀' \
               '飘育馥琦晶妍茜秋珊莎锦黛青倩婷宁蓓纨苑婕馨瑗琰韵融园艺咏卿聪澜纯毓悦昭冰爽琬茗羽希'
        name=r.choice(xing)+"".join(r.choice(ming) for i in range(2))
        return  name
if __name__=="__main__":
    # commonList().createPhone()
    commonList().randomName()

