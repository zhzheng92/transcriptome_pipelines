#! /usr/bin/env python3
import argparse
import time
import sys
import re
import os
bindir = os.path.abspath(os.path.dirname(__file__))

__author__ = 'Zihao Zheng'
__mail__ = 'billzhengzh@gmail.com'
__doc__ = 'the description of program'

pat1=re.compile('^s+$')

def get_tf(tf_file):
	dict = {}
	for index,line in enumerate(tf_file):
		if index ==0 :
			header = line.rstrip()
		else:
			tmp = line.rstrip().split('\t')
			dict[tmp[0]]=line.rstrip()
	return dict,header

def main():
	parser=argparse.ArgumentParser(description=__doc__,
		formatter_class=argparse.RawDescriptionHelpFormatter)
	parser.add_argument('-t','--tf',help='tf file',dest='tf',type=open,required=True)
	parser.add_argument('-g','--group',help='group list',dest='group',type=open,required=True)
	parser.add_argument('-o','--output',help='output dir',dest='output',required=True)
	parser.add_argument('-i','--input',help='input file',dest='input',required=True,nargs='+')
	args=parser.parse_args()

	tf_dict,title = get_tf(args.tf)
	print(len(tf_dict.keys()))
	group_dict = {}
	for line in args.group:
		key = line.rstrip()
		group_dict[key] = 1

	for file in args.input:
		name = file.split('/')[-1].split('.')[0]
		if not name in group_dict:continue

		out_file = '{0}/{1}.TF.xls'.format(args.output,name)
		outfile = open(out_file,'w')
		outfile.write(title+'\tUP/Down\n')

		with open(file,'r') as f:
			for index,line in enumerate (f):
				if line.startswith('#') or re.search(pat1,line):continue
				if index ==0 :continue
				else:
					tmp = line.rstrip().split('\t')
					gene,de,sig = tmp[0],tmp[-2],tmp[-1]
					if gene in tf_dict and sig == 'yes':
						outfile.write(tf_dict[gene]+'\t'+sig+'\n')
			f.close()
			outfile.close()

if __name__ == '__main__':
	main()
