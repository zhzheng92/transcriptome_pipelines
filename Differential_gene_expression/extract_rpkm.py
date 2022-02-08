#! /usr/bin/env python3
import argparse
import sys
import os
import re
import math
bindir = os.path.abspath(os.path.dirname(__file__))

__author__='Zihao Zheng'
__mail__= 'billzhengzh@gmail.com'
__doc__='the decription of program'

pat1=re.compile('^\s+$')

def getRpkmGene(rpkm_file):
	gene_dic = {}
	filein = open(rpkm_file)
	for index,line in enumerate(filein):
		lines = line.rstrip().split('\t')
		if index==0:
			gene_dic[lines[0]] = lines[1:]
			continue
		if lines[0] not in gene_dic:
			#print(lines)
			gene_dic[lines[0]] = [str(math.log(float(i)+0.0001,2)) for i in lines[1:]]
	return(gene_dic)


def main():
	parser=argparse.ArgumentParser(description=__doc__,
			formatter_class=argparse.RawDescriptionHelpFormatter,
			epilog='author:\t{0}\nmail:\t{1}'.format(__author__,__mail__))
	parser.add_argument('-i','--in',help='input file',dest='input',nargs='+',required=True)
	parser.add_argument('-r','--rpkm',help='input rpkm file',required=True)
	parser.add_argument('-o','--output',help='output file',dest='output',type=argparse.FileType('w'),required=True)
	args=parser.parse_args()
	gene_dic = getRpkmGene(args.rpkm)
	gene_list = []
	for file in args.input:
		print(file)
		filein = open(file)
		for index,line in enumerate(filein):
			lines = line.rstrip().split('\t')
			if index == 0:
				[sig_index] = [index for index,item in enumerate(lines) if item.capitalize() == 'Significant']
				print('Significant colnm',sig_index)
				continue
			#print(lines[8])
			if lines[sig_index] != 'yes' and lines[sig_index] != 'no':
				print ('Wrong info in Significnat colnm, please check your input file! (cut -f {0})\n'.format(sig_index+1))
				sys.exit(1)
			elif lines[sig_index] == 'yes':
				if lines[0] in gene_dic:
					gene_list.append(lines[0])
	args.output.write('name'+'\t'+'\t'.join(gene_dic['name'])+'\n')
	gene_list = list(set(gene_list))
	for g in gene_list:
		if g in gene_dic:
			args.output.write(g+'\t'+'\t'.join(gene_dic[g])+'\n')
		else:
			print('{0} not in rpkm file'.format(g))

if __name__ == '__main__':
	main()
