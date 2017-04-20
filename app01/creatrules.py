__author__ = 'wyw'
# coding=utf-8
import itertools
import xlrd,xlwt
from xlutils.copy import copy

class rulesbuilder:
    #fset:频繁项集；itemcount：频次表；conf：置信度阈值
    def __init__(self,sample,fset,itemcount,conf):
        self.sample=sample.recipeTrans
        self.w4herblist=sample.weights
        self.fset=fset
        self.itemcount=itemcount
        self.conf=conf
        self.herbs=self.getherbname()
        self.creatrule()

    def creatrule(self):
        self.rulesdict={}
        self.rulesdict1={}
        self.f2set={}
        self.f3set={}
        self.f4set={}
        for fs in self.fset:
            fset = []
            for herb in fs:
                fset.append(self.herbs[herb])
            if fs.__len__()==2:
                self.f2set[str(fset)]=self.fset[fs]
            if fs.__len__()==3:
                self.f3set[str(fset)]=self.fset[fs]
            if fs.__len__()==4:
                self.f4set[str(fset)]=self.fset[fs]
            bef=self.splitfset(fs)
            for i in range(0,len(bef)):
                w_befcount, w_afcount, w_rcount, w_rconf, lift, IR, Kulc, befcount, afcount, rcount, rconf=self.rIndicators(fs,bef[i])
                if w_rconf>=self.conf:
                    befset=[]
                    for herb in bef[i]:
                        befset.append(self.herbs[herb])
                    rule=str(set(befset))+str(w_befcount)+'=>'+str(set(fset) - set(befset))+str(w_afcount)
                    rule_draw=str(set(bef[i]))+'=>'+str(set(fs) - set(bef[i]))
                    rulerecord={"sup":w_rcount,"conf":w_rconf,"lift":lift,"IR":IR,"Kulc":Kulc}
                    self.rulesdict.setdefault(rule_draw,rulerecord)
                    self.rulesdict1.setdefault(rule, rulerecord)

    def splitfset(self,fs):
        bef=[]
        for i in range(1,len(fs)):
            bef.extend(list(itertools.combinations(fs, i)))
        return bef

    def rIndicators(self,fs,bef):
        rcount = self.countset(fs)
        w_rcount = self.countset_w(fs)
        befcount = self.countset(bef)
        w_befcount = self.countset_w(bef)
        afset = set(fs) - set(bef)
        afcount = self.countset(list(afset))
        w_afcount = self.countset_w(list(afset))
        rconf = rcount / befcount
        w_rconf = w_rcount / w_befcount
        lift = (rcount * len(self.sample)) / (befcount * afcount)#lift取0到正无穷大，lift小于1表示规则前项出现抑制后项出现，lift大于1表示促进（一般大于3视为有效）
        Kulc = (1 / befcount + 1 / afcount) * (rcount / 2)#Kulc取0-1，Kulc越大规则两侧的联系越紧密
        IR = abs(befcount - afcount) / (befcount + afcount - rcount)#IR为0时规则两个方向的蕴含相同，ir越大越不平衡
        # Kulc = self.rIndicator_herb(fs, bef)
        return w_befcount, w_afcount, w_rcount, w_rconf, lift, IR, Kulc, befcount, afcount, rcount, rconf

    def countset(self,fset):
        if len(fset)==1:
            return self.itemcount[fset[0]]
        else:
            count=0
            for trans in self.sample:
                #判断trans是否为fset的超集
                if(set(trans)>=set(fset)):
                    count += 1
            return count

    def countset_w(self,fset):
        count=0
        flag=True
        for i in range(0,len(self.sample)):
            recipe=self.sample[i]
            if set(fset)<=(set(recipe)):
                w4herb=self.w4herblist[i]
                for item in fset:
                    if int(w4herb[recipe.index(item)]) == 1:
                        count += 1
                        flag=False
                        break
                if flag:
                    count += 2
            flag=True
        return count

    def export2excel(self, path):
        self.exportfset(path)
        self.exportrules(path)

    def exportfset(self, path):
        wb = xlwt.Workbook()
        fsetsheet = wb.add_sheet(u'fset', cell_overwrite_ok=True)
        title=['f1set','sup','f2set','sup','f3set','sup','f4set','sup']
        for i in range(0, len(title)):
            fsetsheet.write(0, i, title[i], self.set_style('Times New Roman', 220, True))
        i=1
        rankkeys = sorted(self.itemcount.keys(), key=lambda k: self.itemcount[k], reverse=True)
        for key in rankkeys:
            fsetsheet.write(i, 0, self.herbs[key])
            fsetsheet.write(i, 1, self.itemcount[key])
            i+=1
        i=1
        rankkeys = sorted(self.f2set.keys(), key=lambda k: self.f2set[k], reverse=True)
        for key in rankkeys:
            fsetsheet.write(i, 2, str(key))
            fsetsheet.write(i, 3, self.f2set[key])
            i+=1
        i=1
        rankkeys = sorted(self.f3set.keys(), key=lambda k: self.f3set[k], reverse=True)
        for key in rankkeys:
            fsetsheet.write(i, 4, str(key))
            fsetsheet.write(i, 5, self.f3set[key])
            i+=1
        i=1
        rankkeys = sorted(self.f4set.keys(), key=lambda k: self.f4set[k], reverse=True)
        for key in rankkeys:
            fsetsheet.write(i, 6, str(key))
            fsetsheet.write(i, 7, self.f4set[key])
            i+=1
        wb.save(path)

    def exportrules(self, path):
        wbold = xlrd.open_workbook(path)
        wbnew = copy(wbold)
        sheet = wbnew.add_sheet(u'rules', cell_overwrite_ok=True)
        title=['rule','sup','conf','lift','IR','Kulc']
        for i in range(0, len(title)):
            sheet.write(0, i, title[i], self.set_style('Times New Roman', 220, True))
        i=1
        for key in self.rulesdict1.keys():
            sheet.write(i, 0, key)
            sheet.write(i, 1, self.rulesdict1[key]['sup'])
            sheet.write(i, 2, self.rulesdict1[key]['conf'])
            sheet.write(i, 3, self.rulesdict1[key]['lift'])
            sheet.write(i, 4, self.rulesdict1[key]['IR'])
            sheet.write(i, 5, self.rulesdict1[key]['Kulc'])
            i+=1
        wbnew.save(path)

    def set_style(self,name, height, bold=False):
        style = xlwt.XFStyle()  # 初始化样式
        font = xlwt.Font()  # 为样式创建字体
        font.name = name  # 'Times New Roman'
        font.bold = bold
        font.color_index = 4
        font.height = height
        style.font = font
        return style

    def getherbname(self):
        return {"aa":"白术","ab":"茯苓","ac":"甘草","ad":"茵陈蒿","ae":"丹参","af":"泽泻","ag":"猪苓",
               "ah":"陈皮","ai":"枳壳","aj":"郁金","ak":"半夏","al":"车前子","am":"神曲","an":"大腹皮",
               "ao":"鸡内金","ap":"太子参","aq":"鳖甲","ar":"大黄","as":"黄芪","at":"黄芩","au":"半枝莲",
               "av":"黄连","aw":"党参","ax":"茯苓皮","ay":"薏苡仁","az":"连翘","ba":"白芍","bb":"当归",
               "bc":"谷芽","bd":"厚朴","be":"柴胡","bf":"赤芍","bg":"白茅根","bh":"地黄","bi":"白花蛇舌草",
               "bj":"麦芽","bk":"泽兰","bl":"砂仁","bm":"知母","bn":"桂枝","bo":"瓜蒌","bp":"蒲公英",
               "bq":"山楂","br":"金钱草","bs":"香附","bt":"枸杞子","bu":"山药","bv":"乌贼骨","bw":"生姜",
               "bx":"败酱草","by":"牡丹皮","bz":"白芨","ca":"牡蛎","cb":"酸枣仁","cc":"栀子","cd":"姜黄",
               "ce":"玄参","cf":"苦杏仁","cg":"麦门冬","ch":"木香","ci":"延胡索","cj":"沙参","ck":"莪术",
               "cl":"葶苈子","cm":"葛根","cn":"夏枯草","co":"石菖莆","cp":"桑白皮","cq":"藿香","cr":"桔梗",
               "cs":"槟榔","ct":"浙贝母","cu":"通草","cv":"路路通","cw":"牛膝","cx":"葫芦壳","cy":"金银花",
               "cz":"海藻","da":"黄精","db":"滑石","dc":"山茱萸","dd":"川芎","de":"豆蔻","df":"佛手",
               "dg":"桃仁","dh":"阿胶","di":"旋覆花","dj":"防风","dk":"火麻仁","dl":"白英","dm":"瞿麦",
               "dn":"石斛","do":"龙胆草","dp":"忍冬藤","dq":"夜交藤","dr":"诸实子","ds":"紫花地丁","dt":"苏子",
               "du":"荆芥","dv":"附子","dw":"木瓜","dx":"茜草","dy":"青蒿","dz":"莱菔子","ea":"龙葵",
               "eb":"苦参","ec":"川楝子","ed":"女贞子","ee":"赤小豆","ef":"熟地黄","eg":"大枣","eh":"远志",
               "ei":"前胡","ej":"白薇","ek":"黄柏","el":"仙鹤草","em":"益母草","en":"菊花","eo":"防己",
               "ep":"灵芝","eq":"虎杖","er":"苍术","es":"射干","et":"杜仲","eu":"蒲黄","ev":"何首乌",
               "ew":"珍珠母","ex":"乳香","ey":"没药","ez":"五味子","fa":"佩兰","fb":"牛蒡子","fc":"鸡血藤",
               "fd":"竹茹","fe":"薄荷","ff":"决明子","fg":"菟丝子","fh":"天花粉","fi":"升麻","fj":"芦根",
               "fk":"百部","fl":"龙骨","fm":"橘络","fn":"七叶一枝花","fo":"三棱","fp":"红花","fq":"苘麻子",
               "fr":"芒硝","fs":"淫羊藿","ft":"马勃","fu":"牵牛子","fv":"侧柏叶","fw":"川贝母","fx":"蝉蜕",
               "fy":"海金沙","fz":"冬葵子","ga":"寄生","gb":"马齿苋","gc":"皂荚","gd":"五灵脂","ge":"徐长卿",
               "gf":"柏子仁","gg":"薤白","gh":"瓦楞子","gi":"三七","gj":"淡竹叶","gk":"银柴胡","gl":"石膏",
               "gm":"板蓝根","gn":"扁蓄","go":"王不留行","gp":"朱云苓","gq":"红藤","gr":"云芝","gs":"青皮",
               "gt":"浮小麦","gu":"扁豆","gv":"紫菀","gw":"肉苁蓉","gx":"血余炭","gy":"乌梅","gz":"地骨皮",
               "ha":"花椒","hb":"藕节炭","hc":"紫草","hd":"白藓皮","he":"地龙","hf":"伸筋草","hg":"天门冬",
               "hh":"独活","hi":"赤石脂","hj":"合欢花","hk":"胡芦巴","hl":"麻黄","hm":"芡实","hn":"续断",
               "ho":"狗脊","hp":"百合","hq":"沉香","hr":"鱼腥草","hs":"天麻","ht":"鹿角","hu":"郁李仁",
               "hv":"威灵仙","hw":"墨旱莲","hx":"地肤子","hy":"地丁","hz":"肉桂","ia":"白附子","ib":"斑蟊",
               "ic":"土茯苓","id":"蜈蚣","ie":"玫瑰花","if":"乌药","ig":"地枫皮","ih":"生晒参","ii":"土贝母",
               "ij":"甘松","ik":"龙齿","il":"白芥子","im":"辛夷","in":"苍耳子","io":"桑椹子","ip":"山慈菇",
               "iq":"枇杷叶","ir":"蜇虫","is":"穿山甲","it":"木蝴蝶","iu":"大青叶","iv":"桑叶","iw":"紫苏",
               "ix":"羌活","iy":"马鞭草","iz":"木通","ja":"萹蓄","jb":"乌稍蛇","jc":"茺蔚子","jd":"地榆",
               "je":"五加皮","jf":"萆薢","jg":"糯稻根","jh":"萆邂","ji":"六一散","jj":"钩藤","jk":"款冬花",
               "jl":"骨碎补","jm":"荷叶","jn":"冬瓜皮","jo":"玉米须","jp":"诃子","jq":"肉豆蔻","jr":"吴茱萸",
               "js":"益智","jt":"巴戟天","ju":"苏木","jv":"胆南星","jw":"胡黄连"}
