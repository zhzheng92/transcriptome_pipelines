#! /usr/bin/env python3
import argparse
import time
import sys
import re
import os
import logging
bindir = os.path.abspath(os.path.dirname(__file__))

__author__ = 'Zihao Zheng'
__mail__ = 'billzhengzh@gmail.com'
__doc__ = 'the description of program'

'''
import node file and find the edge file by  matching suffix.
'''

pat1=re.compile('^s+$')

def Read_edge(edge_file,max):
	edge_dict = {}
	select_dict = {}

	in_edge =open(edge_file,'r')
	for index,line in enumerate(in_edge):
		node_1 = line.rstrip('\n').split('\t')[0]
		edge_dict.setdefault(node_1,[]).append(line.rstrip('\n'))
	in_edge.close()

	for index,node in enumerate(edge_dict):
		if index == int(max):
			break
		select_dict[node] = edge_dict[node][0:5]

	return select_dict

def main():
	parser=argparse.ArgumentParser(description=__doc__,
		formatter_class=argparse.RawDescriptionHelpFormatter)
	parser.add_argument('-n','--node',help='node file',dest='node',required=True)
	#parser.add_argument('-e','--edge',help='edge file',dest='edge',required=True)
	parser.add_argument('-o','--outdir',help='output dir',dest='outdir',required=True)
	parser.add_argument('-t','--type',help='network type',default='network')
	parser.add_argument('-m','--max',help='max node to choose',type=int,default=100)
	args=parser.parse_args()

	edge_file = os.path.abspath(args.node).replace('node.txt','edge.txt')
	if not os.path.exists(edge_file):
	#if not os.path.basename(args.node).split('.')[0] == os.path.basename(args.edge).split('.')[0]:
		print('Node file does not have a matched Edge file!\n{0}\n '.format(args.node))
		exit

	out_node = open('{0}.{1}.node.txt'.format(args.outdir,args.type),'w')
	out_edge = open('{0}.{1}.edge.txt'.format(args.outdir,args.type),'w')

	edge_dict = Read_edge(edge_file,args.max)
	node_list = []

	for source in edge_dict:
		for info in edge_dict[source]:
			out_edge.write('{0}\n'.format(info))
			target = info.split('\t')[1]
			node_list.append(source)
			node_list.append(target)

	node_list = list(set(node_list))
	print(len(node_list))
	in_node = open(args.node,'r')
	for index,line in enumerate(in_node):
		if line.startswith('#') or re.search(pat1,line):continue
		node,*info = line.rstrip('\n').split('\t')
		if node in node_list:
			out_node.write(line)

	in_node.close()
	out_node.close()
	out_edge.close()

if __name__ == '__main__':
	main()
