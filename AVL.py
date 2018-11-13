# coding=utf-8
#import random, math

outputdebug = False 

# Para debuggear.
def debug(msg):
    if outputdebug:
        print msg

# El nodo.
class Node():
    def __init__(self,point,dimension=0):
        self.left = None 
        self.right = None
        # Adaptación del Duis.
        # Árbol asociado a ese nodo T(v).
        self.T_assoc = None
        # El punto asociado a ese nodo.
        self.point = point
        # La dimensión de nuestro nodo 0,1 o 2 (x,y o z)
        self.dimension = dimension

    # Determina si tiene hijo derecho.
    def hasRightChild(self):
        return self.right.node != None

    # Determina si tiene hijo izquierdo.
    def hasLeftChild(self):
        return self.left.node != None

    # Regresa el valor del nodo.
    def getValue(self):
        return self.point[self.dimension]

    def getPoint(self):
        return self.point

    # Asgina un nuevo valor al nodo.
    def setValue(self,value):
        self.point[self.dimension] = value


# El Árbol AVL, tuneado para árboles de rangos, by el Duis.
class AVLTree():
    def __init__(self,dimension = 0):
        self.node = None 
        self.height = -1  
        self.balance = 0
        # Adaptación del Duis 
        self.isPoint = False
        self.dimension = dimension
        
                
    def height(self):
        if self.node: 
            return self.node.height 
        else: 
            return 0 
    
    def is_leaf(self):
        return (self.height == 0) 
        
    def rebalance(self):
        ''' 
        Rebalance a particular (sub)tree
        ''' 
        # value inserted. Let's check if we're balanced
        self.update_heights(False)
        self.update_balances(False)
        while self.balance < -1 or self.balance > 1: 
            if self.balance > 1:
                if self.node.left.balance < 0:  
                    self.node.left.lrotate() # we're in case II
                    self.update_heights()
                    self.update_balances()
                self.rrotate()
                self.update_heights()
                self.update_balances()
                
            if self.balance < -1:
                if self.node.right.balance > 0:  
                    self.node.right.rrotate() # we're in case III
                    self.update_heights()
                    self.update_balances()
                self.lrotate()
                self.update_heights()
                self.update_balances()


            
    def rrotate(self):
        # Rotate left pivoting on self
        debug ('Rotating ' + str(self.node.getValue()) + ' right') 
        A = self.node 
        B = self.node.left.node 
        T = B.right.node 
        
        self.node = B 
        B.right.node = A 
        A.left.node = T 

    
    def lrotate(self):
        # Rotate left pivoting on self
        debug ('Rotating ' + str(self.node.getValue()) + ' left') 
        A = self.node 
        B = self.node.right.node 
        T = B.left.node 
        
        self.node = B 
        B.left.node = A 
        A.right.node = T 
        
            
    def update_heights(self, recurse=True):
        if not self.node == None: 
            if recurse: 
                if self.node.left != None: 
                    self.node.left.update_heights()
                if self.node.right != None:
                    self.node.right.update_heights()
            
            self.height = max(self.node.left.height,
                              self.node.right.height) + 1 
        else: 
            self.height = -1 
            
    def update_balances(self, recurse=True):
        if not self.node == None: 
            if recurse: 
                if self.node.left != None: 
                    self.node.left.update_balances()
                if self.node.right != None:
                    self.node.right.update_balances()

            self.balance = self.node.left.height - self.node.right.height 
        else: 
            self.balance = 0 

    def delete(self, value):
        # debug("Trying to delete at node: " + str(self.node.getValue()))
        if self.node != None: 
            if self.node.getValue() == value: 
                debug("Deleting ... " + str(value))  
                if self.node.left.node == None and self.node.right.node == None:
                    self.node = None # leaves can be killed at will 
                # if only one subtree, take that 
                elif self.node.left.node == None: 
                    self.node = self.node.right.node
                elif self.node.right.node == None: 
                    self.node = self.node.left.node
                
                # worst-case: both children present. Find logical successor
                else:  
                    replacement = self.logical_successor(self.node)
                    if replacement != None: # sanity check 
                        debug("Found replacement for " + str(value) + " -> " + str(replacement.value))  
                        self.node.setValue(replacement.value) 
                        
                        # replaced. Now delete the value from right child 
                        self.node.right.delete(replacement.value)
                    
                self.rebalance()
                return  
            elif value < self.node.getValue(): 
                self.node.left.delete(value)  
            elif value > self.node.getValue(): 
                self.node.right.delete(value)
                        
            self.rebalance()
        else: 
            return 

    def logical_predecessor(self, node):
        ''' 
        Find the biggest valued node in LEFT child
        ''' 
        node = node.left.node 
        if node != None: 
            while node.right != None:
                if node.right.node == None: 
                    return node 
                else: 
                    node = node.right.node  
        return node 
    
    def logical_successor(self, node):
        ''' 
        Find the smallese valued node in RIGHT child
        ''' 
        node = node.right.node  
        if node != None: # just a sanity check  
            
            while node.left != None:
                debug("LS: traversing: " + str(node.value))
                if node.left.node == None: 
                    return node 
                else: 
                    node = node.left.node  
        return node 

    def check_balanced(self):
        if self == None or self.node == None: 
            return True
        
        # We always need to make sure we are balanced 
        self.update_heights()
        self.update_balances()
        return ((abs(self.balance) < 2) and self.node.left.check_balanced() and self.node.right.check_balanced())  
        
    def inorder_traverse(self):
        if self.node == None:
            return [] 
        
        inlist = [] 
        l = self.node.left.inorder_traverse()
        for i in l: 
            inlist.append(i) 

        inlist.append(self.node.getValue())

        l = self.node.right.inorder_traverse()
        for i in l: 
            inlist.append(i) 
    
        return inlist 

    def display(self, level=0, pref=''):
        '''
        Display the whole tree. Uses recursive def.
        TODO: create a better display using breadth-first search
        '''        
        self.update_heights()  # Must update heights before balances 
        self.update_balances()
        if(self.node != None): 
            print '-' * level * 2, pref, self.node.getValue()    
            if self.node.left != None: 
                self.node.left.display(level + 1, '<')
            if self.node.left != None:
                self.node.right.display(level + 1, '>')

    # Inserta en el árbol
    def insert(self, point, dimension = 0):
        tree = self.node

        newNode = Node(point,dimension)
        
        if tree == None:
            self.node = newNode 
            self.node.left = AVLTree() 
            self.node.right = AVLTree()
        
        elif newNode.getValue() < tree.getValue(): 
            self.node.left.insert(point,dimension)
            
        elif newNode.getValue() > tree.getValue(): 
            self.node.right.insert(point,dimension)
            
        self.rebalance() 

    # Para llenar las hojas del árbol, que serán los puntos.
    def insertaPuntos(self,dimension=0):
        if self.node == None or self.isPoint:
            return
        # El hijo izquierdo
        sub_izq = self.node.left.node
        # Si no tiene hijo izquierdo, ahí insertamos el punto.
        if sub_izq == None:
            self.node.left.node = Node(self.node.point,dimension)
            self.node.left.node.left = AVLTree()
            self.node.left.node.right = AVLTree()
            self.node.left.isPoint = True
            return
        # Si si tiene hijo izquierdo.
        else: 
            self.node.left.insertaDerecho(self.node.point,dimension)

        if self.node.left != None:
            self.node.left.insertaPuntos(dimension)
        if self.node.left != None:
            self.node.right.insertaPuntos(dimension)

    # Función auxiliar para insertaPuntos.
    def insertaDerecho (self,value,dimension):
        if self.node == None:
            self.node = Node(value,dimension)
            self.node.left = AVLTree()
            self.node.right = AVLTree()
            self.isPoint = True
        else: 
            self.node.right.insertaDerecho(value,dimension)

    # Dada una raíz, regresa todas sus hojas (puntos).
    def getHojas(self):
        # Si es una hoja. 
        if not self.node.hasLeftChild() and not self.node.hasRightChild():
            return [self.node.getPoint()]
        lista = []
        # Si tiene hijo izquierdo.
        if self.node.hasLeftChild():
            leftChild = self.node.left
            lista = lista + leftChild.getHojas()
        # Si tiene hijo derecho.
        if self.node.hasRightChild():
            rightChild = self.node.right
            lista = lista + rightChild.getHojas()

        return lista


    # Dada una raíz, regresa V_split. (El nodo donde se divide la búsqueda).
    def getVSplit (self,v1,v2):
        if self.node == None:
            return
        # Esto solo pasa si v1 = v2.
        elif self.node.getValue() == v1 and self.node.getValue() == v2:
            print("El nodo split es: ", self.node.getValue(),self.node.point)
            print(self.node.left.getHojas())
        # Si es el nodo que buscamos
        elif self.node.getValue() >= v1 and self.node.getValue() < v2:
            print("El nodo split es: ", self.node.getValue(),self.node.point)
            print(self.getHojas())
        elif (self.node.getValue() > v1 and self.node.getValue() >= v2):
            self.node.left.getVSplit(v1,v2)
        else:
            self.node.right.getVSplit(v1,v2)

    # Construye recursivamente los árboles asocidados a cada nodo de nuestro árbol principal.
    def fillAssocTrees (self):
        # Si es una hoja.
        if self.isPoint:
            return
        # T(v)
        puntos = self.getHojas()
        print("Para: ", self.node.getPoint())
        # El uno, es temporal, debería ser más genérico.
        dimension = 1
        # Creamos el árbol asociado a este nodo
        self.node.T_assoc = AVLTree(dimension)
        map(lambda punto: self.node.T_assoc.insert(punto,dimension), puntos)
        # Llenamos las hojas.
        self.node.T_assoc.insertaPuntos(dimension)
        print("Su árbol")
        self.node.T_assoc.display()
        if self.node.hasLeftChild():
            self.node.left.fillAssocTrees()
        if self.node.hasRightChild():
            self.node.right.fillAssocTrees()


        
# Usage example
if __name__ == "__main__":
    # Cosas del Duis 
    # Los puntos  
    lista_puntos = [(2,2),(3,4),(5,3),(6,7),(8,5),(9,8),(11,10),(13,6),(12,1),(15,9)]
    # Árbol ordenado respecto al eje x.
    x_tree = AVLTree()
    # Agregamos los puntos al AVL con respecto a su coordenada x.
    map(lambda punto: x_tree.insert(punto), lista_puntos)
    x_tree.insertaPuntos()
    print("El árbol: ")
    x_tree.display()
    # Primer prueba de V Split
    # x_tree.getVSplit(3,4)
    # Primer prueba de Assoc
    x_tree.fillAssocTrees()
    # Fin de Cosas del Duis
    # TO DO
    # En lugar de que el nodo guarde un punto, guardar una lista de puntos.
    # Ver qué onda con los repetidos