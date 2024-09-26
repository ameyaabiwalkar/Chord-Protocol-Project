import math
from bisect import bisect_left
from itertools import product
#from operator import itemgetter
from operator import attrgetter
class Fingertable:

    def __init__(self, n):
        self.n = n
        self.FT = [n for _ in range(8)]

    def set_successor(self, pos, successor):
        self.FT[pos] = successor

    def get_successor(self, pos):
        return self.FT[pos]
    
    """Printing the Finger Table """
    def print_finger_tables(self):
        print(f"-----------------Node id: {self.n.id}------------------")
        #print("\n")
        print(f"Successor: {self.n.successor.id}  \t Predecessor: {self.n.predecessor.id}")
        print("FingerTables:")
        lines = [f"|k = {k + 1} [{(self.n.id + 2**k) % 256}, {(self.n.id + 2**(k + 1)) % 256}) \t \t succ. = {self.FT[k].id if self.FT[k] else -1} |" 
                 for k in range(8)]
        for line in lines:
            print(line)
        horizontal_line = "-" * 40
        vertical_space = "\n"
        asterisk_line = "*" * 41

        print(horizontal_line)
        print(vertical_space)
        print(asterisk_line)

"""Creating a class for the node functionalities"""

class DHTNode:
    
    def __init__(self, identifier, finger_table=None, successor=None, predecessor=None, key_values=None):
        self.id = identifier
        self.FT = finger_table or Fingertable(self)
        self.successor = successor or self
        self.predecessor = predecessor or self
        self.key_values = key_values or {}  

    """Printing of the keys"""
    def print_keys(self):
        print(f"----------------------Node id: {self.id}--------------------\n{self.key_values}\n")

    def find_all(self, ref, check_predecessor_equality=False):
        if (e := self.validate_special_case(ref, check_predecessor_equality)): return e
        dis = (ref - self.id) % 256
        exp = int(math.log2(dis + 1))
        next_val = self.FT.get_successor(exp)
        node_val = next_val.validate_special_case(ref, check_predecessor_equality)
        return node_val if node_val else next_val.predecessor if next_val.predecessor.id > ref and next_val.predecessor == self else next_val.find_all(ref, check_predecessor_equality)


    def validate_special_case(self, ref, check_predecessor_equality):
        if ref == self.id or (check_predecessor_equality and self.predecessor == self == self.successor):
            return self
        if self.predecessor.id < self.id:
            if self.predecessor.id < ref < self.id:
                return self
        elif ref > self.predecessor.id or (ref < self.predecessor.id and ref < self.id):
            return self
        elif self.predecessor.id > self.id and self.predecessor.id < ref < self.id:
            return self
    
    """Join method for a node in the given network"""
    def join(self, n):
        if n:
            self.successor = n.find_all(self.id)
            self.predecessor = self.successor.predecessor
            self.successor.predecessor = self
            self.predecessor.successor = self
            self.pft()
            self.keys_migrated(self.successor)
            
            
    def insert(self, ref, val):
        val = int(val) if val else None
        self.find_all(ref, True).key_values[ref] = val

    """Migration of the keys"""
    def keys_migrated(self, successor):
        removal = [ref for ref in successor.key_values.keys() if
                        (ref <= self.id < self.successor.id) or
                        (self.id > self.successor.id and ref > self.successor.id and ref < self.id) or
                        (self.id < self.successor.id and ref > self.successor.id)]
        migrated_keys = [(k, v) for k, v in successor.key_values.items() if k in removal]
        for k, v in migrated_keys:
            print(f"Migrate key {k} from node {successor.id} to node {self.id}")
            self.key_values[k] = v
        [successor.remove(k2) for k2 in removal] and print('\n')


    def remove(self, ref): self.key_values.pop(ref, None)

    def delete_key(self, ref):
        resp = self.find_all(ref, True)
        #print(resp)
        key_values = resp.key_values
        print(f"Not Found {ref} \n") if ref not in key_values else (print(f"Key deleted {ref} with value {key_values[ref]}\n"), resp.remove(ref))


    """Look up methods for the keys"""

    def lookup(self, z, pointer):
        print(f"---------------------------- node {self.id} -----------------------\n") if pointer == 0 else None

        if z == self and pointer >=1: return
        list_traversed = [z.id, self.id] if z != self else [z.id]
        
        for k, v in self.key_values.items():
            print(f"Look-up result of key {k} from node {z.id} with path {list_traversed} value is {v}")
        self.successor.lookup(z, pointer+1)
    
    def find(self, ref):
        val = self.find_all(ref, True).key_values.get(ref, None)
        print(f"Found {ref} with {val}\n") if val is not None else print(f" {ref} not found\n")


    def pft(self):
        def helper(dht_nodes, ref):
            ids = [l.id for l in dht_nodes]
            ref = ref % 256
            index = bisect_left(ids, ref)
            return dht_nodes[0] if not dht_nodes else dht_nodes[index % len(dht_nodes)]

        dht_nodes = sorted(self.retrieve_nodes([], self, 0), key=attrgetter('id'))

        for j, k in product(dht_nodes, range(8)):
            j.FT.set_successor(k, helper(dht_nodes, j.id + 2**k))

    
    def retrieve_nodes(self, dht_nodes, z, pointer):
        if pointer < 1 or z != self:
            dht_nodes.append(self)
            self.successor.retrieve_nodes(dht_nodes, z, pointer + 1)
        return dht_nodes


    
#f=Fingertable()
#h=Helper()