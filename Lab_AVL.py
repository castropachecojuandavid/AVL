import sys


class Node:
    def __init__(self, value):
        self.value  = value
        self.left   = None
        self.right  = None
        self.height = 1


# Funciones auxiliares

def getHeight(node):
    """Retorna la altura del nodo"""
    if not node:
        return 0
    return node.height

def getBalance(node):
    """Factor de balance alturas izq-der"""
    if not node:
        return 0
    return getHeight(node.left) - getHeight(node.right)

def updateHeight(node):
    """Recalcular h del nodo"""
    if node:
        node.height = 1 + max(getHeight(node.left), getHeight(node.right))


# Rotaciones

def rotate_right(y):
    """Rotación a la derecha, sobre el nodo y."""
    x  = y.left
    T2 = x.right

    x.right = y
    y.left  = T2

    updateHeight(y)
    updateHeight(x)

    return x   #x es la nueva raíz del subárbol

def rotate_left(x):
    """Rotación a la izquierda sobre el nodo x."""
    y  = x.right
    T2 = y.left

    y.left  = x
    x.right = T2

    updateHeight(x)
    updateHeight(y)

    return y   #y es la nueva raíz del subárbol


# Clase AVLTree

class AVLTree:
    def __init__(self):
        self.root = None

    # Inserción
    def insert(self, value):
        self.root = self._insert_recursive(self.root, value)

    def _insert_recursive(self, node, value):
        #1. Inserción BST normal
        if not node:
            return Node(value)

        if value < node.value:
            node.left  = self._insert_recursive(node.left,  value)
        elif value > node.value:
            node.right = self._insert_recursive(node.right, value)
        else:
            return node   #así valores duplicados no se insertan

        #2. Actualizar altura
        updateHeight(node)

        #3.Verificar balance y aplicar rotaciones necesarias
        balance = getBalance(node)

        #Caso Left-Left
        if balance > 1 and getBalance(node.left) >= 0:
            return rotate_right(node)

        #Caso Left-Right
        if balance > 1 and getBalance(node.left) < 0:
            node.left = rotate_left(node.left)
            return rotate_right(node)

        #Caso Right-Right
        if balance < -1 and getBalance(node.right) <= 0:
            return rotate_left(node)

        #Caso Right-Left
        if balance < -1 and getBalance(node.right) > 0:
            node.right = rotate_right(node.right)
            return rotate_left(node)

        return node

    #Eliminación
    def delete(self, value):
        self.root = self._delete_recursive(self.root, value)

    def _delete_recursive(self, node, value):
        #1. Eliminación BST normal
        if not node:
            return node

        if value < node.value:
            node.left  = self._delete_recursive(node.left,  value)
        elif value > node.value:
            node.right = self._delete_recursive(node.right, value)
        else:
            #Nodo encontrado
            if not node.left:
                return node.right
            elif not node.right:
                return node.left

            #Nodo con dos hijos: sucesor in-order
            successor      = self._get_min_node(node.right)
            node.value     = successor.value
            node.right     = self._delete_recursive(node.right, successor.value)

        #2. Actualizar altura
        updateHeight(node)

        #3. Rebalancear
        balance = getBalance(node)

        #Left-Left
        if balance > 1 and getBalance(node.left) >= 0:
            return rotate_right(node)

        #Left-Right
        if balance > 1 and getBalance(node.left) < 0:
            node.left = rotate_left(node.left)
            return rotate_right(node)

        #Right-Right
        if balance < -1 and getBalance(node.right) <= 0:
            return rotate_left(node)

        #Right-Left
        if balance < -1 and getBalance(node.right) > 0:
            node.right = rotate_right(node.right)
            return rotate_left(node)

        return node

    def _get_min_node(self, node):
        """Retorna el nodo con el valor mínimo de un subárbol"""
        while node.left:
            node = node.left
        return node

    #Recorrido In-Order
    def inorder(self):
        """Retorna los elementos en orden ascendente."""
        result = []
        self._inorder_recursive(self.root, result)
        return result

    def _inorder_recursive(self, node, result):
        if node:
            self._inorder_recursive(node.left,  result)
            result.append(node.value)
            self._inorder_recursive(node.right, result)

    #Visualización
    def visualize(self):
        """Imprime el árbol, su valor, altura y factor de balance"""
        if not self.root:
            print("(árbol vacío)")
            return
        self._visualize_recursive(self.root, prefix="", is_left=None)

    def _visualize_recursive(self, node, prefix, is_left):
        if not node:
            return

        #Subárbol derecho primero (arriba)
        right_prefix = prefix + ("│   " if is_left is True  else "    ")
        self._visualize_recursive(node.right, right_prefix, False)

        #Nodo actual
        connector = ""
        if is_left is True:
            connector = "└── "
        elif is_left is False:
            connector = "┌── "

        balance = getBalance(node)
        print(f"{prefix}{connector}[{node.value}] h={node.height} b={balance}")

        #Subárbol izquierdo
        left_prefix = prefix + ("    " if is_left is False else "│   ")
        self._visualize_recursive(node.left, left_prefix, True)


#Para visualización

def run_tests():

    #Prueba 1: rotación simple Right-Right
    print("=" * 55)
    print("Prueba 1: Rotación Right-Right (insertar 10, 20, 30)")
    print("=" * 55)
    t1 = AVLTree()
    for v in [10, 20, 30]:
        t1.insert(v)
    t1.visualize()
    print("In-order:", t1.inorder())

    #Prueba 2: Secuencia del enunciado + rotación Left-Right
    print("\n" + "=" * 55)
    print("Prueba 2: Secuencia mixta [10,20,30,40,50,25]")
    print("=" * 55)
    t2 = AVLTree()
    for v in [10, 20, 30, 40, 50, 25]:
        t2.insert(v)
    t2.visualize()
    print("In-order:", t2.inorder())

    #Prueba 3: Rotación Left-Left
    print("\n" + "=" * 55)
    print("Prueba 3: Rotación Left-Left (insertar 30, 20, 10)")
    print("=" * 55)
    t3 = AVLTree()
    for v in [30, 20, 10]:
        t3.insert(v)
    t3.visualize()
    print("In-order:", t3.inorder())

    #Prueba 4: Rotación Right-Left
    print("\n" + "=" * 55)
    print("Prueba 4: Rotación Right-Left (insertar 10, 30, 20)")
    print("=" * 55)
    t4 = AVLTree()
    for v in [10, 30, 20]:
        t4.insert(v)
    t4.visualize()
    print("In-order:", t4.inorder())

    #Prueba 5: Eliminar y rebalanceo
    print("\n" + "=" * 55)
    print("Prueba 5: Eliminación con rebalanceo")
    print("=" * 55)
    t5 = AVLTree()
    for v in [10, 20, 30, 40, 50, 25]:
        t5.insert(v)
    print("Antes de eliminar 40:")
    t5.visualize()
    t5.delete(40)
    print("\nDespués de eliminar 40:")
    t5.visualize()
    print("In-order:", t5.inorder())

    #Prueba 6: Eliminar un nodo con dos hijos
    print("\n" + "=" * 55)
    print("Prueba 6: Eliminar raíz con dos hijos")
    print("=" * 55)
    t6 = AVLTree()
    for v in [20, 10, 30, 5, 15, 25, 35]:
        t6.insert(v)
    print("Árbol inicial:")
    t6.visualize()
    t6.delete(20)
    print("\nDespués de eliminar 20 (raíz):")
    t6.visualize()
    print("In-order:", t6.inorder())


if __name__ == "__main__":
    run_tests()
