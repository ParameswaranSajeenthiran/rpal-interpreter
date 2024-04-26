
class ASTNode:


    def standarize(self, root):

        if root == None:
            return None


        root.child = self.standarize(root.child)

        if root.sibling != None:
            root.sibling = self.standarize(root.sibling)

        nextSibling = root.sibling;

        # prevSibling = root.previous
        # nextSibling = root.sibling

        match root.type:
            case "let":
                #print("let")
                #print( "type : " , root.child.type)
                if root.child.type == "=":
                    #print("equal")
                    equal = root.child
                    P = equal.sibling
                    X = equal.child
                    E = X.sibling
                    lambdaNode = ASTNode("lambda")
                    gammaNode = ASTNode("gamma")
                    gammaNode.child = lambdaNode
                    lambdaNode.sibling = E
                    #print("stantdarizing let #######")
                    X.sibling = P
                    lambdaNode.child = X







                    # P.previous = X
                    gammaNode.sibling = nextSibling


                    return gammaNode
                else:
                    root.sibling = nextSibling

                    return root

            case "where":
                if root.child.sibling.type== "=":
                    P = root.child
                    equal = P.sibling
                    X = equal.child
                    E = X.sibling
                    lambdaNode = ASTNode("lambda")
                    gammaNode = ASTNode("gamma")

                    gammaNode.child = lambdaNode
                    lambdaNode.sibling = E
                    lambdaNode.child = X

                    X.sibling = P
                    # P.previous = gammaNode
                    P.sibling = None

                    gammaNode.sibling = nextSibling


                    return gammaNode
                else:
                    root.sibling = nextSibling

                    return root

            case "function_form":
                P = root.child
                V = P.sibling
                Vs = V.sibling

                newRoot = ASTNode("=")
                newRoot.child = P

                lambdaNode = ASTNode("lambda")
                P.sibling = lambdaNode
                lambdaNode.previous = P

                while Vs.sibling != None:
                    lambdaNode.child = V
                    lambdaNode = ASTNode("lambda")
                    V.sibling = lambdaNode
                    lambdaNode.previous = V
                    V = Vs
                    Vs = Vs.sibling

                lambdaNode.child = V
                V.sibling = Vs
                Vs.previous = V

                newRoot.sibling = nextSibling

                return newRoot

            # case "tau":
            #     E = root.child
            #     tempE = E
            #     newRoot = None
            #     aug = None
            #     tempESibling = None
            #
            #     gamma = ASTNode("gamma")
            #     gammaL = ASTNode("gamma")
            #
            #     gamma.sibling = gammaL
            #     gammaL.sibling = E
            #     tempESibling = E.sibling
            #     E.sibling = None
            #     aug = ASTNode("aug")
            #     gammaL.child = aug
            #
            #     while E != None:
            #         gamma = ASTNode("gamma")
            #         gammaL = ASTNode("gamma")
            #         aug.sibling = gamma
            #         gamma.child = gammaL
            #         gammaL.sibling = E
            #         tempESibling = E.sibling
            #         E.sibling = None
            #         aug = ASTNode("aug")
            #         gammaL.child = aug
            #         E = tempESibling
            #
            #     aug.sibling = ASTNode('nil')
            #     tempE.sibling = None
            #     newRoot.sibling = nextSibling
            #
            #     return newRoot

            case "within":
                if root.child.type =="=" and root.child.sibling.type == "=":
                    eq1 = root.child
                    eq2 = eq1.sibling
                    X1 = eq1.child
                    E1 = X1.sibling
                    X2 = eq2.child
                    E2 = X2.sibling

                    newRoot = ASTNode("=")
                    newRoot.child = X2
                    gamma = ASTNode("gamma")
                    lambdaNode = ASTNode("lambda")

                    X2.sibling = gamma
                    gamma.previous = X2
                    gamma.child = lambdaNode
                    lambdaNode.sibling = E1
                    E1.previous = lambdaNode
                    lambdaNode.child = X1
                    X1.sibling = E2
                    E2.previous = X1
                    E1.sibling = None
                    newRoot.sibling = nextSibling

                    return newRoot
                else :
                    root.sibling = nextSibling

                    return root

            case "and":
                eq = root.child

                newRoot = ASTNode("=")
                comma = ASTNode(",")
                tau = ASTNode("tau")

                newRoot.child = comma
                comma.sibling = tau
                tau.previous = comma

                X = eq.child
                E = X.sibling

                comma.child = X
                tau.child = E

                eq = eq.sibling
                while eq != None:
                    X.sibling = eq.child
                    eq.child.previous = X
                    E.sibling = eq.child.sibling
                    eq = eq.sibling
                    X = X.sibling
                    E = E.sibling

                X.sibling = None
                E.sibling = None
                newRoot.sibling = nextSibling


                return newRoot

            case "rec":
                eq = root.child
                X = eq.child
                E = X.sibling

                new_root = ASTNode("=")
                new_root.child = X

                copy_X = X.createCopy()
                gamma = ASTNode("gamma")
                X.sibling = gamma
                gamma.previous = X

                # TODO: may need to remove <> later !!!!
                y_star = ASTNode("Y*")
                gamma.child = y_star
                lambda_ = ASTNode("lambda")
                y_star.sibling = lambda_
                lambda_.previous = y_star

                lambda_.child = copy_X
                copy_X.sibling = E
                E.previous = copy_X
                new_root.sibling = nextSibling


                return new_root

            case "@":
                E1 = root.child
                N = E1.sibling
                E2 = N.sibling

                new_root = ASTNode("gamma")
                gamma_l = ASTNode("gamma")

                new_root.child = gamma_l
                gamma_l.sibling = E2
                # E2.previous = gamma_l
                gamma_l.child = N
                N.sibling = E1
                # E1.previous = N
                E1.sibling = None
                new_root.sibling=nextSibling

                return new_root

            case _:
                return root

        # #print("root" , root.type)
        # root.previous = prevSibling
        # root.sibling = nextSibling
        return root

    def __init__(self, type):
        self.type = type
        self.value = None
        self.sourceLineNumber = -1
        self.child = None
        self.sibling = None
        self.previous = None
        self.indentation = 0

    def print_tree(self):
        # #print(self.type)

        if self.child:
            # #print(" child of " + str(self.type) + " is ",end=" ")
            self.child.print_tree()
        if self.sibling:
            # #print(" sibling of " + str(self.type) + " is " ,end=" ")

            self.sibling.print_tree()

    def print_tree_to_cmd(self):

        for i in range(self.indentation):
            print(".", end="")
        if self.value is not None:
            print("<"+str(self.type.split(".")[1]) +":" + str(self.value)+">")
        else:print(str(self.type))
        # print(self.type, end=" ")
        # if self.child:
        #     #print("child of " + str(self.type) + " is ", self.child.type)
        # if self.sibling:
        #     #print("sibling of " + str(self.type) + " is ", self.sibling.type)
        #

        if self.child:
            self.child.indentation = self.indentation + 1
            self.child.print_tree_to_cmd()
        if self.sibling:
            self.sibling.indentation = self.indentation
            self.sibling.print_tree_to_cmd()

    # output to the file
    def print_tree_to_file(self, file):

        for i in range(self.indentation):
            file.write(".")
        # if(self.type ==)
        if self.value is not None:

            file.write("<"+str(self.type.split(".")[1])+":"+str(self.value)+">" + "\n")
        else :
            file.write(str(self.type) + "\n")

        if self.child:

            self.child.indentation = self.indentation + 1
            self.child.print_tree_to_file(file)
        if self.sibling:
            self.sibling.indentation = self.indentation
            self.sibling.print_tree_to_file(file)

    def createCopy (self):
        node = ASTNode(self.type)
        node.value = self.value
        node.sourceLineNumber = self.sourceLineNumber
        node.child = self.child
        node.sibling = self.sibling
        node.previous = self.previous
        return node

