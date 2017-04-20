#coding:utf-8
from django.http import HttpResponse
from django.shortcuts import render
import sample
import mining
import mining_adv
import drawrule
import creatrules
  
def minning(request):
	sample=sample.sample('F:/2016Graduate/20160922.xlsx',u'Python')
	sup=118
	fsetdict={}
	# fItems=mining.findFItem(sample.recipeTrans, sup)
	# f2set=mining.findFSet(sample.recipeTrans, fItems.keys(), 2, sup)
	# fsetdict.update(f2set)
	# f3set=mining.findFSet(sample.recipeTrans, mining.getItemInSet(f2set.keys()), 3, sup)
	# fsetdict.update(f3set)
	# f4set=mining.findFSet(sample.recipeTrans, mining.getItemInSet(f3set.keys()), 4, sup)
	# fsetdict.update(f4set)
	# r=creatrules.rulesbuilder(sample=sample,fset=fsetdict,itemcount=fItems,conf=0.7)
	# r.export2excel('F:/2016Graduate/python_result02.xls')
	# dr=drawrule.drawrule(r.rulesdict)
	# dr.drawscatter(fn='scatter02.png')
	# dr.drawbubble(fn='bubble02.png')
	# dr.drawnetwork(fn='network02.png')
	fItems=mining_adv.findFItem(sample.recipeTrans, sample.weights, sup)
	f2set=mining_adv.findFSet(sample.recipeTrans, fItems.keys(), sample.weights, 2, sup)
	fsetdict.update(f2set)
	f3set=mining_adv.findFSet(sample.recipeTrans, mining.getItemInSet(f2set.keys()), sample.weights, 3, sup)
	fsetdict.update(f3set)
	f4set=mining_adv.findFSet(sample.recipeTrans, mining.getItemInSet(f3set.keys()), sample.weights, 4, sup)
	fsetdict.update(f4set)
	r=creatrules.rulesbuilder(sample=sample,fset=fsetdict,itemcount=fItems,conf=0.7)
	r.export2excel('F:/2016Graduate/python_result_y0.xls')
	# dr=drawrule.drawrule(r.rulesdict)
	# dr.drawscatter(fn='scatter13.png')
	# dr.drawbubble(fn='bubble13.png')
	# dr.drawnetwork(fn='network13.png')
    return render(request, 'home.html')