# import queue

import ASTNode


class Tau:
    def __init__(self, n):
        self.n = n
class Beta:
    def __init__(self):
        pass

class CtrlStruct:
    def __init__(self, idx, delta):
        self.idx = idx
        self.delta = delta
class LambdaExpression:
    def __init__(self, envIdx, lambdaIdx, tok):
        self.envIdx = envIdx
        self.lambdaIdx = lambdaIdx
        self.item = tok

    def print_lambda_expression(self):
        if isinstance(self.item, ASTNode.ASTNode):
            pass

            # System.out.#print("[lambda closure: " + ((Token)item).name + ": " + idx + "]");
            # print("lambda~" + self.env_id + "~" + self.item.name + "~" + str(self.idx))
        elif isinstance(self.item, list):
            # System.out.println("Lambda's item is a list");
            lam_vars = ""
            for it in self.item:
                # System.out.println("it: " + ((Token)it).name);
                lam_vars += it.name + ','
            #print("lambda~" + self.env_id + "~" + lam_vars + "~" + str(self.idx))


class ControlStructureGenerator:
    def __init__(self):
        self.curIdxDelta = 0
        self.queue = []
        self.map_ctrl_structs = {}
        self.current_delta=[]

    # def print_ctrl_structs(self):
    #     #print("Starting printCtrlStructs:\n\n\n")
    #     for key, ctrl_struct in self.map_ctrl_structs.items():
    #         #print("key: " + str(key))
    #         for obj in ctrl_struct:
    #             # if isinstance(obj, ASTNode.ASTNode):
    #             #     # if obj.value is not None:
    #             #     #     print("value: " +  obj.type + str(obj.value))
    #             #     # else:
    #             #     #     print("value: " +  obj.type )
    #
    #             elif isinstance(obj, LambdaExpression):
    #                 pass
    #                 #print("value: ", " envIdx: ", obj.envIdx, " lambdaIdx: ", obj.lambdaIdx)
    #             elif isinstance(obj, list):
    #                 #print("I am a list")
    #                 for item in obj:
    #                     if isinstance(item, ASTNode):
    #                         pass
    #                         # print("Token item: " + item.type)
    #                     else:
    #                         pass
    #                         # print("item: " + str(item))
    #             else:
    #                 print("I was not Token or LambdaExpression, value: " + str(obj))
    #         #print("next obj\n\n")

    def generate_control_structures(self, root):
        delta = []
        self.current_delta = []
        self.pre_order_traversal(root, delta)
        # #print cureent delta here

        # for items in self.current_delta:
        #     if isinstance(items, ASTNode.ASTNode):
        #         #print("current delta: " + items.type)
        #     elif isinstance(items, LambdaExpression):
        #         #print("current delta: commented for now")
        #         items.print_lambda_expression()
        #     elif isinstance(items, list):
        #         #print("I am a list")
        #         for item in items:
        #             if isinstance(item, ASTNode):
        #                 #print("Token item: " + item.type)
        #             else:
        #                 #print("item: " + str(item))
        #     else:
        #         #print("I was not Token or LambdaExpression, current delta: " + str(items))
        #print("queue: " + str(self.queue))
        ctrl_delta = CtrlStruct(self.curIdxDelta, delta)
        self.map_ctrl_structs[0] = self.current_delta.copy()
        # #print("queue: " + str(self.queue))
        # for items in self.queue:
            #print("items in queue: " + str(items[1].type) + str(items[1].child.type))

        while len(self.queue)>0:
            #print("while lloopp")
            self.current_delta = []


            idx, node, delta_queue = self.queue[0]
            #print("idx: " + str(idx) + " node: " + str(node.type) + " delta_queue: " + str(delta_queue))
            self.pre_order_traversal(node, delta_queue)
            #print("lenght")
            #print(len(self.current_delta))
            ctrl_delta = CtrlStruct(idx, delta_queue)
            self.map_ctrl_structs[idx] = self.current_delta.copy()

            # #print(self.map_ctrl_structs)
            self.queue.pop(0)
            # for items in self.queue:
            #     if items[1].child is not None:
            #         print("items in queue: " + str(items[1].type) + str(items[1].child.type))

        return self.map_ctrl_structs



    def pre_order_traversal(self, root ,delta):

        # if root is None:
        #     return
        #
        # self.pre_order_traversal(root.child ,delta)
        #
        # if root.sibling != None:
        #     self.pre_order_traversal(root.sibling ,delta)



        #print("root type: " + root.type)
        match root.type :
            case "lambda":
                #print("lambdhs "+str(root.child.type))
                self.curIdxDelta += 1
                # currently all environment Indices of each lambda are set to 0, they will be
                # set to proper values when the lambda gets moved to stack.
                lambda_exp = None
                if root.child.type ==',':
                    # rule 11
                    #print("rule 11")
                    tau_list = []
                    child = root.child.child
                    while child is not None:
                        tau_list.append(child)
                        child = child.sibling
                    lambda_exp = LambdaExpression(0, self.curIdxDelta, tau_list)
                else:
                    lambda_exp = LambdaExpression(0, self.curIdxDelta, root.child)

                #print("addingrrrr lambda with id: " + str(self.curIdxDelta)+str(root.child.sibling.type))
                self.current_delta.append(lambda_exp)
                delta_lambda = []

                self.queue.append((self.curIdxDelta, root.child.sibling, delta_lambda))
                #print("103", self.queue[-1][1].child.type)
                # if root.child.sibling is not None:
                #     sibling_delta = []
                #     saved_idx_delta = curIdxDelta
                #     pre_order_traversal(root.child.sibling, sibling_delta)
                #     ctrl_delta = CtrlStruct(saved_idx_delta, sibling_delta)
                #     map_ctrl_structs[saved_idx_delta] = ctrl_delta

                # if root.sibling is not None:
                #     #print("############ 123 ")
                #
                #     self.pre_order_traversal(root.sibling, delta)
                return
            case "->":
                delta2 = []
                # savedcurIdxDelta = curIdxDelta
                savedcurIdxDelta2 = self.curIdxDelta + 1
                savedcurIdxDelta3 = self.curIdxDelta + 2
                self.curIdxDelta += 2

                node2 = root.child.sibling
                # print("135",root.child.sibling.sibling.type ,root.type)

                node3 = root.child.sibling.sibling

                node2.sibling = None  # to avoid re-traversal
                """
                preOrderTraversal(node2, delta2)
                ctrlDelta2 = CtrlStruct(savedcurIdxDelta2, delta2)
                mapCtrlStructs[savedcurIdxDelta2] = ctrlDelta2
                """
                self.queue.append((savedcurIdxDelta2, node2, delta2))

                # node3.sibling = None

                delta3 = []
                """
                preOrderTraversal(node3, delta3)
                ctrlDelta3 = CtrlStruct(savedcurIdxDelta3, delta3)
                mapCtrlStructs[savedcurIdxDelta3] = ctrlDelta3
                """
                self.queue.append((savedcurIdxDelta3, node3, delta3))
                self.current_delta.append( CtrlStruct ( savedcurIdxDelta2 , delta2))
                self.current_delta.append(CtrlStruct ( savedcurIdxDelta3 , delta3))
                # print("adding beta \n\n\n")
                beta = Beta()
                self.current_delta.append(beta)  # TODO: may create a problem: be careful!!!!!!!!!!!!!!!!
                # this is imp so that you don't traverse the sibling of the 1st child again
                # as you already did it above.
                root.child.sibling = None
                # print("now calling preOrder for root.child: " + root.child.type)
                self.pre_order_traversal(root.child, delta)
                #
                # if root.child.sibling is not None:
                #     self.pre_order_traversal(root.child.sibling, delta)
                return
            case "gamma":
                # print("adding gamma")
                self.current_delta.append(root)
                self.pre_order_traversal(root.child, delta)
                if root.child.sibling is not None:
                    self.pre_order_traversal(root.child.sibling, delta)
                return

            case "tau":
                initial_length=len(self.current_delta)
                node = root.child
                next_node = node.sibling
                deltas_tau = []
                counter = 0
                while node is not None:
                    node.sibling = None
                    self.pre_order_traversal(node, deltas_tau)
                    node = next_node
                    if node is not None:
                        next_node = node.sibling
                    counter += 1

                tau = Tau(counter)
                temp=[]
                final_length=len(self.current_delta)
                # print("adding tau" )
                counter=final_length-initial_length
                for i in range(counter):
                    temp.append(self.current_delta.pop())

                self.current_delta.append(tau)
                for i in range(counter):
                    self.current_delta.append(temp.pop())
                # delta.extend(deltas_tau)

                if root.sibling is not None:
                    self.pre_order_traversal(root.sibling, delta)
                return

            # case "**":
            #     # print("adding **")
            #     delta.append(root.type)
            #     self.pre_order_traversal(root.child, delta)
            #     if root.sibling is not None:
            #         self.pre_order_traversal(root.sibling, delta)
            #     return
            #
            #
            # case "*":
            #     self.current_delta.append(root);
            #     self.pre_order_traversal(root.child, delta);
            #     if (root.child.sibling is not None):
            #         self.pre_order_traversal(root.child.sibling, delta);

            case _ :
                self.current_delta.append(root);
                if (root.child is not None):
                    self.pre_order_traversal(root.child, delta);
                    if (root.child.sibling is not None):
                        self.pre_order_traversal(root.child.sibling, delta);
                # print("default " + root.type)
                return
            








