# coding=utf-8
import xlrd

class sample:
    #样本数据类
    def __init__(self,xls,sheet):
        self.xls=xls
        self.sheet=sheet
        self.recipeTrans,self.weights=self.creatDataset()

    '''20161002：读取excel'''
    def getExcel(self):
        file = xlrd.open_workbook(self.xls)
        table = file.sheet_by_name(self.sheet)
        return table

    '''20161002：建立分析用数据集'''
    def creatDataset(self):
        recipe = list()
        recipelist = list()
        w_dose = list()
        w_doselist = list()
        data = self.getExcel()
        for i in range(1,data.nrows-1):
            recipe.append(data.cell(i,1).value)
            w_dose.append(data.cell(i,4).value)
            if data.cell(i,0).value!=data.cell(i+1,0).value or i==data.nrows-2:
                if i==data.nrows-2:
                    recipe.append(data.cell(i+1,1).value)
                    w_dose.append(data.cell(i+1,4).value)
                recipelist.append(recipe)
                w_doselist.append(w_dose)
                recipe = list()
                w_dose = list()
        return recipelist,w_doselist
