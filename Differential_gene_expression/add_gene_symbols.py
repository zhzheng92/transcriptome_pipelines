#! /usr/bin/env python3
import argparse
import sys
import os
import re
bindir = os.path.abspath(os.path.dirname(__file__))

__author__='ZZ'
__mail__= 'billzhengzh@gmail.com

pat1=re.compile('^\s+$')

def read_anno(f_file):
	record={}
	for line in f_file:
		if line.startswith('#') or re.search(pat1,line):continue
		tmp=line.rstrip().split('\t')
		name,symbols = tmp[0],tmp[7]
		if not name in record:
			record[name] = symbols
		else:
			print('{0} is repeat'.format(name))
	return record


def main():
	parser=argparse.ArgumentParser(description=__doc__,
			formatter_class=argparse.RawDescriptionHelpFormatter,
			epilog='author:\t{0}\nmail:\t{1}'.format(__author__,__mail__))
	parser.add_argument('-i','--input',help='input file',dest='input',type=open,required=True)
	parser.add_argument('-a','--anno',help='annotation file',dest='anno',type=open,required=True)
	parser.add_argument('-o','--output',help='output file',dest='output',type=argparse.FileType('w'),required=True)
	args=parser.parse_args()

	record = read_anno(args.anno)


	for line in args.input:
		if line.startswith('#') or re.search(pat1,line):continue
		tmp=line.rstrip().split('\t')
		names = tmp[4].split(r'|')
		symbols = "|".join([record[i] for i in names])
		args.output.write('\t'.join(tmp + [symbols]) + '\n')

if __name__ == '__main__':
	main()
