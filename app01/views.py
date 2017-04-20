#coding:utf-8
from django.http import HttpResponse
from django.shortcuts import render,render_to_response
from django import forms
from app01.models import File,Transaction
import xlrd
import app01.sample as sample
import app01.mining_adv as mining_adv
import app01.mining as mining
import app01.creatrules as creatrules

class FileForm(forms.Form):
	file = forms.FileField()

def index(request):
	if request.method == "POST":
		uf = FileForm(request.POST,request.FILES)
		if uf.is_valid():
		    #获取表单信息
			file = uf.cleaned_data['file']
			#写入数据库
			f = File()
			f.filename = file
			f.file = file
			f.save()
			#载入事务数据
			#import2sqlite(file)
			#获取数据源信息
			t_num,t_len,i_num = getFileInfo()
			result = minning(file)
			info_dict = {'filename':file,'t_num':t_num,'t_len':t_len,'i_num':i_num,'result':result}
			return render_to_response('home.html', {'info_dict': info_dict,'uf':uf})
	else:
		uf = FileForm()
	return render_to_response('home.html', {'uf':uf})

def import2sqlite(filename):
	fpath = './app01/static/upload/'+str(filename)
	file = xlrd.open_workbook(fpath)
	data = file.sheet_by_index(0)
	for i in range(1,data.nrows-1):
		t = Transaction();
		t.t_id = data.cell(i,0).value
		t.herb = data.cell(i,1).value
		t.weight = data.cell(i,2).value
		t.save()
		print("已导入:"+i+"条数据")
	return True

def getFileInfo():
	total = Transaction.objects.all().count()
	t_num = Transaction.objects.values('t_id').distinct().count()
	i_num = Transaction.objects.values('herb').distinct().count()
	return t_num,total/t_num,i_num
	
def minning(filename):
	s=sample.sample('./app01/static/upload/'+str(filename),u'Python')
	sup=90
	result="===============挖掘结果===============\n"
	fsetdict={}
	fItems=mining_adv.findFItem(s.recipeTrans, s.weights, sup)
	result+=" 频繁1项集："+str(len(fItems))+"个；\n\n"
	f2set=mining_adv.findFSet(s.recipeTrans, fItems.keys(), s.weights, 2, sup)
	fsetdict.update(f2set)
	result+=" 频繁2项集："+str(len(f2set))+"个；\n\n"
	f3set=mining_adv.findFSet(s.recipeTrans, mining.getItemInSet(f2set.keys()), s.weights, 3, sup)
	fsetdict.update(f3set)
	result+=" 频繁3项集："+str(len(f3set))+"个；\n\n"
	f4set=mining_adv.findFSet(s.recipeTrans, mining.getItemInSet(f3set.keys()), s.weights, 4, sup)
	fsetdict.update(f4set)
	result+=" 频繁4项集："+str(len(f4set))+"个；\n\n"
	r=creatrules.rulesbuilder(sample=s,fset=fsetdict,itemcount=fItems,conf=0.7)
	r.export2excel('./app01/static/upload/'+'result_y0.xls')
	result+=" 有效规则 ："+str(len(r.rulesdict1))+"条。\n\n"
	result+="===具体挖掘结果请参见生成的excel文件==="
	return result