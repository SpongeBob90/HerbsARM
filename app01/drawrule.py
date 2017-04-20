__author__ = 'wyw'
# coding=utf-8
from rpy2 import robjects
from rpy2.robjects.packages import importr
from IPython.core.display import Image
import re

class drawrule:
    # 将获得的规则以图形方式展示
    def __init__(self,rules):
        self.rprint = robjects.globalenv.get("print")
        self.stats = importr('stats')
        self.grdevices = importr('grDevices')
        self.base = importr('base')
        self.arules = importr('arules')
        self.arulesViz = importr('arulesViz')
        self.RColorBrewer = importr('RColorBrewer')
        self.creatruleset(rules)

    def creatruleset(self, rules):
        flag=False
        for rule in rules.keys():
            sets=str.split(rule,'=>')
            robjects.globalenv["l"]=robjects.StrVector(re.findall("[a-z]+", sets[0]))
            robjects.globalenv["r"]=robjects.StrVector(re.findall("[a-z]+", sets[1]))
            quality=rules[rule]
            # robjects.globalenv["q"]=robjects.DataFrame({'support':int(quality['sup']),'confidence':float(quality['conf']),'w_Kulc':float(quality['h_Kulc'])})
            robjects.globalenv["q"] = robjects.DataFrame(
                {'support': int(quality['sup']), 'confidence': float(quality['conf']),
                 'lift': float(quality['lift'])})
            robjects.r('''
                lm<-matrix(1,ncol=length(l))
                dimnames(lm)<-list(NULL,l)
                x<-matrix(0,ncol=length(r))
                dimnames(x)<-list(NULL,r)
                lhs<-as(cbind(lm,x),"itemMatrix")
                rm<-matrix(1,ncol=length(r))
                dimnames(rm)<-list(NULL,r)
                x<-matrix(0,ncol=length(l))
                dimnames(x)<-list(NULL,l)
                rhs<-as(cbind(x,rm),"itemMatrix")
            ''')
            if flag:
                robjects.r('''
                rule<-new("rules",lhs=lhs,rhs=rhs,quality=q)
                ruleset<-c(ruleset,rule)
                ''')
            else:
                robjects.r('ruleset<-new("rules",lhs=lhs,rhs=rhs,quality=q)')
                flag=True

    def drawscatter(self, fn = 'scatter.png',width = 1000, height = 600):
        self.grdevices.png(fn, width = width, height = height)
        robjects.r('''plot(ruleset, control=list(jitter=2,col=rev(brewer.pal(9,"Greens")[4:9])), shading = "lift")''')
        self.grdevices.dev_off()
        return Image(filename=fn)

    def drawbubble(self, fn = 'bubble.png',width = 1000, height = 1000):
        self.grdevices.png(fn, width = width, height = height)
        robjects.r('''plot(ruleset, method="grouped",control=list(col = rev(brewer.pal(9, "Greens")[4:9])),shading ="lift")''')
        self.grdevices.dev_off()
        return Image(filename=fn)

    def drawnetwork(self, fn = 'network.png',width = 800, height = 800):
        self.grdevices.png(fn, width = width, height = height)
        robjects.r('''plot(ruleset,measure="confidence",method="graph",control=list(type="items"),shading ="lift")''')
        self.grdevices.dev_off()
        return Image(filename=fn)
