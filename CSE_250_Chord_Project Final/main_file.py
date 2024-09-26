
from dhtnode import DHTNode
import sys

nodes_list = {}

def create_node(id):
    """Creating a new node with the given ID"""
    return DHTNode(int(id))

def find_value(input_node, key):
    """Retrieving the value associated with the key"""
    input_node.find(int(key))

def join_nodes(new_node, current_node):
    """Linking the new node to the existing node"""
    new_node.join(current_node)

def print_finger_table(current_node):
    """Displaying the finger table of the node"""
    current_node.FT.print_finger_tables()

def print_key_values(current_node):
    """Displaying the key-value pairs stored in the node"""
    current_node.print_keys()

def remove_key(marked_node, key):
    """Deleting the key and its associated value from the node"""
    marked_node.delete_key(int(key))

def insert_key_value(new_node, key, val):
    """Storing the key-value pair in the node"""
    new_node.insert(int(key), val)

def lookup_search(current_node):
    """Searching for the key in the network"""
    current_node.lookup(current_node, 0)
    
""" Defining a dictionary to map commands to functions"""
action_functions = {
    "add_node": create_node,
    "find": find_value,
    "join": join_nodes,
    "print_finger": print_finger_table,
    "print_keys": print_key_values,
    "remove": remove_key,
    "insert_node": insert_key_value,
    "lookup": lookup_search
}

with open(sys.argv[-1], 'r') as f:
    inputs = f.readlines()

"""Scanning the input and separating the arguments"""
for i in inputs:
    action, *args = i.split()

    if action=="add_node" and action in action_functions.keys():
        nodes_list[args[0]] = create_node(args[1])

    elif action == "remove" and action in action_functions.keys():
        n = nodes_list[args[0]]
        remove_key(n, args[1])

    elif action == "find" and action in action_functions.keys():
        n = nodes_list[args[0]]
        find_value(n, args[1])

    elif action == "join" and action in action_functions.keys():
        if args[1] != 'None':
            n, c= nodes_list[args[0]], nodes_list[args[1]]
            join_nodes(n, c)

    elif action=="print_finger" and action in action_functions.keys():
        print_finger_table(nodes_list[args[0]])

    elif action=="print_keys" and action in action_functions.keys():
        print_key_values(nodes_list[args[0]])
    
    elif action == "insert_node" and action in action_functions.keys():
            n, k, x = nodes_list[args[0]], args[1], args[2] if len(args) == 3 else None
            insert_key_value(n, k, x)

    elif action=="lookup" and action in action_functions.keys():
        lookup_search(nodes_list[args[0]])
        
"""

def execute_command(action, *args):

    if action in action_functions:
        action_functions[action](*args)


"""