count = 0

class node_rst:
	def __init__(self,start,end,dis_type,content):
		self.start = start
		self.end = end
		self.dis_type = dis_type
		self.child_rel = None
		self.content = content
		self.left = None
		self.right = None

class line_rst:
	def __init__(self):
		self.dis_type = None
		self.start = 0
		self.end = 0
		self.node_type = None
		self.rel2par = None
		self.text = None

class node_graph_from_tree:
	def __init__(self, tree_node):
		self.id = tree_node.start
		self.string = tree_node.content
		self.neighbour_relations = []
		self.predecessor = None

def get_line_attributes(line):
	line_object = line_rst()
	line_split = line.split('(')
	if(len(line_split)>1):
		line_object.dis_type = line_split[1].strip()
		attr_split = line_split[2].split(' ')
		line_object.node_type = attr_split[0]
		if(line_object.node_type == 'leaf'):
			line_object.start = line_object.end = int( attr_split[1].strip(')') )
			line_object.text = line_split[4].strip(')')
		else:
		 	line_object.start = int( attr_split[1] )
		 	line_object.end = int( attr_split[2].strip(')') )
		if(line_object.dis_type != 'Root'):	
			attr_split = line_split[3].split(' ')
			line_object.rel2par = attr_split[1].strip(')')
	return line_object	

def add_nodes(line_objects, T):
	if(T==None):
		return
	left_flag = 0
	right_flag = 0
	for line_object in line_objects:	
		if(line_object.start==T.start and line_object.end<T.end and left_flag==0):
			node = node_rst(line_object.start,line_object.end,line_object.dis_type,line_object.text)
			T.left = node
			if node.dis_type=='Satellite':
				T.child_rel = line_object.rel2par
			elif node.dis_type=='Nucleus' and line_object.rel2par!='span':
				T.child_rel = line_object.rel2par
			left_flag = 1
		if(line_object.start>T.start and line_object.end==T.end and right_flag==0):
			node = node_rst(line_object.start,line_object.end,line_object.dis_type,line_object.text)
			T.right = node
			if node.dis_type=='Satellite':
				T.child_rel = line_object.rel2par
			right_flag = 1
	T.left = add_nodes(line_objects, T.left)
	T.right = add_nodes(line_objects, T.right)
	return T	

def print_pre_order_traversal(T):
	if(T == None):
		return
	print T.start, T.end, T.child_rel, T.content
	print_pre_order_traversal(T.left)
	print_pre_order_traversal(T.right)

def make_tree(line_objects):
	root_node = node_rst(line_objects[0].start,line_objects[0].end,line_objects[0].dis_type,line_objects[0].text)
	T = root_node
	T = add_nodes(line_objects, T)
	# print_pre_order_traversal(root_node)
	return T

def find_most_nuclear_node(T):
	if(T.left==None and T.right==None):
		return T
	if(T.left.dis_type=='Nucleus'):
		return find_most_nuclear_node(T.left)
	elif(T.right.dis_type=='Nucleus'):
		return find_most_nuclear_node(T.right)

def find_node_with_id(id, graph_nodes):
	flag = 0
	for graph_node in graph_nodes:
		if(graph_node.id == id):	
			return graph_node				

def make_graph_from_tree(T, graph_nodes, graph_node_ids): 							# TODO: multi-nuclear relations
	global count
	if(T.left==None and T.right==None):
		return graph_nodes
	node1 = find_most_nuclear_node(T.left)
	node2 = find_most_nuclear_node(T.right)
	rel = T.child_rel

	if node1.start in graph_node_ids:
		graph_node_1 = find_node_with_id(node1.start, graph_nodes)
	else:
		graph_node_1 = node_graph_from_tree(node1)	
	if node2.start in graph_node_ids:
		graph_node_2 = find_node_with_id(node2.start, graph_nodes)
	else:
		graph_node_2 = node_graph_from_tree(node2)

	if(T.left.dis_type=='Nucleus' and T.right.dis_type=='Satellite'):			
		graph_node_1.neighbour_relations.append( (graph_node_2,rel) )
		count+=1 					
	elif(T.left.dis_type=='Satellite' and T.right.dis_type=='Nucleus'):
		graph_node_2.neighbour_relations.append( (graph_node_1,rel) )
		count+=1
	graph_node_ids.add(graph_node_1.id)
	graph_node_ids.add(graph_node_2.id)
	graph_nodes.add(graph_node_1)
	graph_nodes.add(graph_node_2)

	graph_nodes = make_graph_from_tree(T.left, graph_nodes, graph_node_ids)
	graph_nodes = make_graph_from_tree(T.right, graph_nodes, graph_node_ids)
	return graph_nodes

def find_path(G, node1, node2):
	nodes_queue = [node1]
	flag = 0
	while len(nodes_queue)>0:
		current_node = nodes_queue[0]
		for neighbour_relation in current_node.neighbour_relations:
			neighbour_relation[0].predecessor = current_node
			if(neighbour_relation[0].id == node2.id):
				flag = 1
				break
			nodes_queue.append(neighbour_relation[0])	
		if(flag==1):
			break
		nodes_queue.pop(0)
	if(flag==0):
		print "There is no path from node1 to node2"
		return None
	else:
		relations_list = []
		print "There is a path"
		current_node = node2
		while current_node.id != node1.id:
			prev_node = current_node.predecessor
			print "Prev node id: ",prev_node.id
			for neighbour_relation in prev_node.neighbour_relations:
				if neighbour_relation[0].id == current_node.id:
					relations_list.append(neighbour_relation[1])
					break							
			current_node = prev_node
		relations_list.reverse()	
		return relations_list				 

def main():
	filename = 'lec26.pdf.xmln1.dis'
	graph_nodes = set([])
	graph_node_ids = set([])
	with open(filename) as f:
		text = f.read()
	lines = text.split('\n')[:-1]
	line_objects = []
	for line in lines:
		line_objects.append( get_line_attributes(line) )		
	T = make_tree(line_objects)
	G = make_graph_from_tree(T, graph_nodes, graph_node_ids)
	
#	edge_count = 0
#	for item in G:
#		if(item.id==1):
#			for x in item.neighbour_relations:
#				print x[0].id, x[1]
#		edge_count += len(item.neighbour_relations)

	str1 = raw_input("Enter first string: ")
	str2 = raw_input("Enter second string: ")
	for item in G:
		if item.string.find(str1) != -1:
			node1 = item
		if item.string.find(str2) != -1:
			node2 = item
	print node1.id
	print node2.id

	relations_list = find_path(G,node1,node2)
	print relations_list
				
main()		