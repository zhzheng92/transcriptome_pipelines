#! /usr/bin/env python3
import argparse
import sys
import os
import re
import math
bindir = os.path.abspath(os.path.dirname(__file__))

__author__='Zihao Zheng'
__mail__= 'billzhengzh@gmail.com'

pat1=re.compile('^\s+$')

def read_input(f_file,cmp,o_file,q_cutoff,log2_cutoff):
	cols = ['id', 'baseMeanA', 'baseMeanB', 'pval','padj','result']
	n_col = []
	o_file.write('Gene\t{0}_normalize\t{1}_normalize\tFoldChange\tLog2FoldChange\tpval\tpadj\tUp/Down\tSignificant\n'.format(cmp[0],cmp[1]))
	for count,line in enumerate(f_file):
		if line.startswith('#') or re.search(pat1,line):continue
		tmp=line.rstrip().split('\t')
		if count == 0:
			n_col = [tmp.index(i) for i in cols]
		else:
			[gene,ba,bb,p,q,result] = [tmp[i] for i in n_col]
			ba = float(ba)
			bb = float(bb)
			fc ,log2fc, up  = '','',''
			if bb == 0 and ba == 0 :
				fc,log2fc = 'NA','NA'
				up = '--'
			elif ba == 0:
				fc,log2fc = '-Inf','-Inf'
				up = 'down'
			elif bb == 0 :
				fc,log2fc = 'Inf','Inf'
				up = 'up'
			else:
				fc = float(ba)/float(bb)
				log2fc = math.log(fc,2)
				if log2fc > 0 :
					up='up'
				else:
					up='down'
			if log2fc == 'NA':
				result = 'no'
			elif float(q) < q_cutoff  and abs(float(log2fc)) > log2_cutoff :
				result = 'yes'
			else:
				result = 'no'
			o_file.write('{0}\n'.format("\t".join([str(i) for i in [gene,ba,bb,fc,log2fc,p,q,up,result]])))

def main():
	parser=argparse.ArgumentParser(description=__doc__,
			formatter_class=argparse.RawDescriptionHelpFormatter,
			epilog='author:\t{0}\nmail:\t{1}'.format(__author__,__mail__))
	parser.add_argument('-i','--input',help='input file',dest='input',type=open,required=True)
	parser.add_argument('-c','--compare',help='compare group, in cordance with compare group use in DEseq',dest='cmp',required=True,nargs=2)
	parser.add_argument('-q','--qvalue',help='q value cutoff',dest='q',type=float,default=0.05)
	parser.add_argument('-l','--log2ratio',help='log2 ratio abs cutoff',dest='log2',type=float,default=1)
	parser.add_argument('-o','--output',help='output file',dest='output',type=argparse.FileType('w'),required=True)
	args=parser.parse_args()

	read_input(args.input,args.cmp,args.output,args.q,args.log2)
if __name__ == '__main__':
	main()
