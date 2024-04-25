
import ASTNode
class StandarizedNode:
    def standarize(self, root):


        if root ==None:
            return None

        root.child= self.standarize(root.child)

        if root.sibling != None:
            root.sibling = self.standarize(root.sibling)

        prevSibling = root.previous
        nextSibling = root.sibling

        match root.type :
            case "let":
                equal = root.child
                P = equal.sibling
                X = equal.child
                E = X.sibling
                lambdaNode = ASTNode.ASTNode("lambda")
                gammaNode = ASTNode.ASTNode("gamma")

                lambdaNode.child = X
                lambdaNode.sibling = E
                gammaNode.child = lambdaNode
                gammaNode.sibling = P
                P.previous = gammaNode
                return gammaNode

            case "where":
                P = root.child
                equal = P.sibling
                X = equal.child
                E = X.sibling
                lambdaNode = ASTNode.ASTNode("lambda")
                gammaNode = ASTNode.ASTNode("gamma")

                lambdaNode.child = X
                lambdaNode.sibling = E
                gammaNode.child = lambdaNode
                gammaNode.sibling = P
                P.previous = gammaNode
                return gammaNode

            case "function_form":
                P = root.child
                V = P.sibling
                Vs = V.sibling


                newRoot = ASTNode.ASTNode("=")
                newRoot.child = P

                lambdaNode = ASTNode.ASTNode("lambda")
                P.sibling = lambdaNode
                lambdaNode.previous = P




                while Vs.sibling != None:
                    lambdaNode.child = V
                    lambdaNode = ASTNode.ASTNode("lambda")
                    V.sibling = lambdaNode
                    lambdaNode.previous = V
                    V = Vs
                    Vs = Vs.sibling

                lambdaNode.child = V
                V.sibling = Vs
                Vs.previous = V

                return newRoot

            # case "tau":
            #     E= root.child
            #     tempE =E
            #     newRoot = None
            #     aug =None
            #     tempESibling =None
            #
            #     gamma = ASTNode.ASTNode("gamma")
            #     gammaL = ASTNode.ASTNode("gamma")
            #
            #     gamma.sibling = gammaL
            #     gammaL.sibling = E
            #     tempESibling=E.sibling
            #     E.sibling = None
            #     aug= ASTNode.ASTNode("aug")
            #     gammaL.child = aug


                while E !=None:
                    gamma = ASTNode.ASTNode("gamma")
                    gammaL= ASTNode.ASTNode("gamma")
                    aug.sibling = gamma
                    gamma.child = gammaL
                    gammaL.sibling  =E
                    tempESibling = E.sibling
                    E.sibling = None
                    aug = ASTNode.ASTNode("aug")
                    gammaL.child = aug
                    E = tempESibling

                aug.sibling = ASTNode.ASTNode('nil')
                tempE.sibling = None
                return newRoot

            case "within":
                eq1= root.child
                eq2 = eq1.sibling
                X1 = eq1.child
                X2 = eq2.child
                E1 = X1.sibling
                E2 = X2.sibling

                newRoot = ASTNode.ASTNode("=")
                newRoot.child = X2
                gamma = ASTNode.ASTNode("gamma")
                lambdaNode = ASTNode.ASTNode("lambda")

                X2.sibling = lambdaNode
                gamma.previous = X2
                gamma.child = lambdaNode
                lambdaNode.sibling = E1
                E1.previous = lambdaNode
                lambdaNode.child = X1
                X1.sibling = E2
                E2.previous = X1
                E1.sibling = None

                return newRoot

            case "and":
                eq= root.child

                newRoot = ASTNode.ASTNode("=")
                comma = ASTNode.ASTNode("comma")
                tau = ASTNode.ASTNode("tau")

                newRoot.child = comma
                comma.sibling = tau
                tau.previous= comma

                X = eq.child
                E = X.sibling

                comma.child = X
                tau.child = E

                eq= eq.sibling
                while eq != None :
                    X.sibling = eq.child
                    eq.child.previous = X
                    E.sibling = eq.child.sibling
                    eq = eq.sibling
                    X = X.sibling
                    E = E.sibling

                X.sibling = None
                E.sibling = None
    
                return newRoot

            case "rec":
                eq = root.first
                X = eq.first
                E = X.sibling

                new_root = ASTNode.ASTNode("=")
                new_root.first = X

                copy_X = X.create_copy()
                gamma = ASTNode.ASTNode("gamma")
                X.sibling = gamma
                gamma.previous = X

                # TODO: may need to remove <> later !!!!
                y_star = ASTNode.ASTNode("Y*")
                gamma.first = y_star
                lambda_ = ASTNode.ASTNode("lambda")
                y_star.sibling = lambda_
                lambda_.previous = y_star

                lambda_.first = copy_X
                copy_X.sibling = E
                E.previous = copy_X

                return new_root

            case "@":
                E1 = root.first
                N = E1.sibling
                E2 = N.sibling

                new_root = ASTNode.ASTNode("gamma")
                gamma_l = ASTNode.ASTNode("gamma")

                new_root.first = gamma_l
                gamma_l.sibling = E2
                E2.previous = gamma_l
                gamma_l.first = N
                N.sibling = E1
                E1.previous = N
                E1.sibling = None
                new_root.sibling = nextSibling

                return new_root



                    























    #     / *
    #     *LET
    #     *
    #
    #
    # let = > gamma
    # /  \ / \
    #     =    P
    # lambda E
    # /  \ / \
    #     X
    # E
    # X
    # P
    #
    # * /




