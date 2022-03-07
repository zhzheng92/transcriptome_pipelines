#! /usr/bin/env python
'''
Description:
	this file is used to get overlap for 2 file, and output intercouse line
'''
import argparse
import sys
import os

__author__='Zihao Zheng'
__mail__='billzhengzh@gmail.com'
def Overlap(dict1,dict2):
	out_dict={}
	for i in dict1:
		if i in dict2:
			#out_dict[i]="{0}\t{1}".format(dict1[i],dict2[i])
			out_dict[i]="{0}".format('\t'.join(dict2[i]))
	return out_dict

def store_record(id,record,args,count,line):
	tmp=line.split('\t')
	if not id in record:
		record[id]={}
	if args.col[count] == 'all':
		record[id][count] = line
	else:
		try:
			a_col = int(args.col[count])
			record[id][count] = tmp[a_col]
		except :
			print(args.col[count],'should be int')
			sys.exit()
	#return record

def main():
	parser=argparse.ArgumentParser(
			description=__doc__,
			formatter_class=argparse.RawDescriptionHelpFormatter,
			epilog='Author:\t{0}\nE-mail:\t{1}\n'.format(__author__,__mail__)
			)
	parser.add_argument('-f','--files',dest='files',help='input more than ones file',required=True,nargs='+')
	parser.add_argument('-head','--header',dest='header',help='header line number [0]',default=0,type=int)
	parser.add_argument('-i','--index',dest='index',help='which col is index [0] ',default=[0],type=int,nargs='*')
	parser.add_argument('-c','--col',dest='col',help='which col should be store [all] ',nargs='*',required=True)
	parser.add_argument('-n','--name',dest='name',help='names ',nargs='*',type=str,default=[])
	parser.add_argument('-s','--sep',dest='sep',help='separte symbol in id column',default='')
	args=parser.parse_args()

	if len(args.files)<2 :
		print('please input more than one files',file=sys.stderr)
		sys.exit()

	count=0
	record={}
	col_count=0
	for file in args.files:
		tag=0
		try :
			args.index[count]
		except IndexError:
			args.index.append(args.index[count-1])

		try:
			args.col[count]
		except IndexError:
			args.col.append(args.col[count-1])

		try :
			args.name[count]
		except IndexError:
			bb = os.path.basename(file).split(r'.')
			args.name.append(bb[0])

		with open(file,'r') as f_file:
			for line in f_file:
				tag+=1
				tt = 0
				if args.header >= tag :continue
				for i in ['no_feature','ambiguous','too_low_aQual','not_aligned','alignment_not_unique']:
					if line.startswith(i) : tt =1
				if tt == 1 :continue
				line=line.rstrip()
				if line.startswith('__'):continue
				tmp=line.split('\t')
				if not col_count : col_count =len(line)
				ids=tmp[args.index[count]]
				if args.sep:
					ids = ids.split(args.sep)
					for id in ids:
						store_record(id,record,args,count,line)
				else:
					store_record(ids,record,args,count,line)
		count+=1

	print("name\t"+"\t".join(args.name))
	if 'name' in record:
		output='name\t'
		for file_num in range(len(args.files)):
			if file_num in record['name']:
				output+=record['name'][file_num]+'\t'
			else:
				output+='miss\t'
		output=output.rstrip()
		print(output)

	for id in record:
		if id == 'name' : continue
		output=id+'\t'
		for file_num in range(len(args.files)):
			if file_num in record[id]:
				output+=record[id][file_num]+'\t'
			else:
				output+='miss\t'
		output=output.rstrip()
		#output_value = [int(i) for i in output.split('\t')[1:]]
		#if sum(output_value) == 0:continue
		print(output)

if __name__=='__main__':
	main()
