#! /usr/bin/env python3
import argparse
import sys
import os
import re

__author__='Zihao Zheng'
__mail__= 'billzhengzh@gmail.com'

pat1=re.compile('^\s+$')

def read_sample(f_file):
	r_dict = {}
	r_list = []
	for line in f_file:
		if line.startswith('#') or re.search(pat1,line):continue
		tmp=line.rstrip().split('\t')
		name,group = tmp[0],tmp[3]
		if not name in r_list :
			r_list.append(name)
		if not group in r_dict:
			r_dict[group] = []
		if not name in r_dict[group]:
			r_dict[group].append(name)
	return r_dict,r_list

def read_report(f_file):
	cmp = []
	gene = []
	for count,line in enumerate(f_file):
		if line.startswith('#') or re.search(pat1,line):continue
		tmp=line.rstrip().split('\t')
		if count == 0 :
			for i in tmp :
				if i.endswith('_normalize'):
					group = i.replace('_normalize','')
					if not group in cmp:
						cmp.append(group)
				elif i.endswith('_rpkm'):
					group = i.replace('_rpkm','')
					if not group in cmp:
						cmp.append(group)
				else:
					pass
		else:
			if tmp[-1] == 'yes':
				gene.append(tmp[0])
	return gene,cmp

def get_samples(cmp,in_dict):
	r_list = []
	for i in cmp:
		r_list.extend(in_dict[i])
	return r_list

def output_heatmap(f_out,f_file,samples,genes):
	cols = []
	for count,line in enumerate(f_file):
		tmp=line.rstrip().split('\t')
		output = ''
		if count == 0 :
			for i in tmp[1:]:
				if i in samples:
					cols.append(tmp.index(i))
			output = 'gene\t{0}\n'.format('\t'.join(samples))
		else:
			if not tmp[0] in genes: continue
			rpkms = [tmp[i] for i in cols]
			output = '{0}\t{1}\n'.format(tmp[0],"\t".join(rpkms))
		f_out.write(output)

def main():
	parser=argparse.ArgumentParser(description=__doc__,
			formatter_class=argparse.RawDescriptionHelpFormatter,
			epilog='author:\t{0}\nmail:\t{1}'.format(__author__,__mail__))
	parser.add_argument('-i','--input',help='input file',dest='input',type=open,required=True)
	parser.add_argument('-s','--sample',help='sample list file',dest='sample',type=open,required=True)
	parser.add_argument('-r','--rpkm',help='rpkm file',dest='rpkm',type=open,required=True)
	parser.add_argument('-c','--cmp',help='compare group',dest='cmp',nargs="+")
	parser.add_argument('-o','--output',help='output file',dest='output',type=argparse.FileType('w'),required=True)
	args=parser.parse_args()

	sample_dict,sample_list = read_sample(args.sample)

	gene_list, compare = read_report(args.input)

	if not args.cmp == None:
		compare = args.cmp

	print(sample_dict)
	print(compare)
	samples = get_samples(compare, sample_dict)

	output_heatmap(args.output, args.rpkm, samples, gene_list)


if __name__ == '__main__':
	main()
