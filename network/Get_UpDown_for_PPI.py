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
def ReadReport(report_file):
	gene_dict = {}
	for index,line in enumerate(report_file):
		if line.endswith('yes\n'):
			lines = line.rstrip('\n').split('\t')
			if not lines[0] in gene_dict:
				gene_dict[lines[0]] = lines[-2]
	return gene_dict

def main():
	parser=argparse.ArgumentParser(description=__doc__,
		formatter_class=argparse.RawDescriptionHelpFormatter)
	parser.add_argument('-r','--report',help='de report file',type=open,required=True)
	parser.add_argument('-p','--pro',help='reference pro file',type=open,required=True)
	parser.add_argument('-c','--cmp',help='input compare name',required=True)
	parser.add_argument('-o','--outdir',help='outdir',required=True)
	args = parser.parse_args()

	node_file = open('{0}/{1}.ppi.node.txt'.format(args.outdir,args.cmp),'w')
	edge_file = open('{0}/{1}.ppi.edge.txt'.format(args.outdir,args.cmp),'w')

	de_dict = ReadReport(args.report)
	de_ppi = {}
	for index,line in enumerate(args.pro):
		if line.startswith('#') or re.search(pat1,line):continue
		pro_1, pro_2 = line.rstrip('\n').split('\t')
		if pro_1 in de_dict and pro_2 in de_dict:
			output = '\t'.join(sorted([pro_1,pro_2]))
			edge_file.write(output+'\n')
			de_ppi[pro_1] = de_dict[pro_1]
			de_ppi[pro_2] = de_dict[pro_2]

	for gene in de_ppi:
		node_file.write(gene+'\t'+de_ppi[gene]+'\n')

if __name__ == '__main__':
	main()
