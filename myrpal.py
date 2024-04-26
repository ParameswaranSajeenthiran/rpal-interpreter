import Tokernizer
from Tokernizer import Screener
import controlStructure
from cseMachine import CSEMachine
import os
from ASTNode import ASTNode

BLACK = '\033[30m'
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m' # orange on some systems
BLUE = '\033[34m'
MAGENTA = '\033[35m'
CYAN = '\033[36m'
LIGHT_GRAY = '\033[37m'
DARK_GRAY = '\033[90m'
BRIGHT_RED = '\033[91m'
BRIGHT_GREEN = '\033[92m'
BRIGHT_YELLOW = '\033[93m'
BRIGHT_BLUE = '\033[94m'
BRIGHT_MAGENTA = '\033[95m'
BRIGHT_CYAN = '\033[96m'
WHITE = '\033[97m'

RESET = '\033[0m' # called to return to standard terminal text color

BLACK = '\033[30m'
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m' # orange on some systems




class ASTParsser:

    def __int__(self, tokens1):
        self.tokens = tokens1
        self.current_token = None
        self.index = 0

    def read(self):

        if self.current_token.type in [Tokernizer.TokenType.ID, Tokernizer.TokenType.INT,
                                       Tokernizer.TokenType.STRING] :

            terminalNode = ASTNode( str(self.current_token.type))
            terminalNode.value= self.current_token.value
            stack.append(terminalNode)
            # #print stack
            # #print("stack content after reading")
            # for node in stack:
            #     #print(node.data)
        if self.current_token.value in  ['true', 'false', 'nil', 'dummy']:
            # stack.append(ASTNode(self.current_token.value))
            terminalNode = ASTNode(str(self.current_token.type))
            terminalNode.value = self.current_token.value
            stack.append(terminalNode)

        #print("reading : " + str(self.current_token.value))
        self.index += 1

        if (self.index < len(self.tokens)):
            self.current_token = self.tokens[self.index]
        # elif self.index  >=len(self.tokens):



    def buildTree(self, token, ariness):
        global stack

        #print("stack content before ")
        # for node in stack:
        #     node.print_tree_to_cmd()




        # #print("building tree")

        node = ASTNode(token)

        node.value = None
        node.sourceLineNumber = -1
        node.child = None
        node.sibling = None
        node.previous = None

        while ariness > 0:
            # #print("error in while loop")
            child = stack[-1]
            stack.pop()
            # Assuming pop() is a function that returns an ASTNode
            if node.child is not None:
                child.sibling = node.child
                node.child.previous = child
                # node.previous = child
            node.child = child

            node.sourceLineNumber = child.sourceLineNumber
            ariness -= 1
        # node.print_tree()

        stack.append(node)  # Assuming push() is a function that pushes a node onto a stack
        # #print("stack content after")
        for node in stack:
            pass
            # #print(node.type)

    def procE(self):
        #print('procE')


        match self.current_token.value:

            case 'let':
                self.read()
                self.procD()

                if self.current_token.value != 'in':
                    # #print("Error: in is expected")
                    return

                self.read()
                #print("E->let D in E #####")
                self.procE()
                #print("E->let D in E #")

                # #print('E->let D in E')
                self.buildTree("let", 2)

            case 'fn':

                n = 0

                self.read()

                while self.current_token.type == Tokernizer.TokenType.ID or self.current_token.value == '(':
                    self.procVb()
                    n += 1

                if n == 0:
                    #print("E: at least one 'Vb' expected\n")
                    return

                if self.current_token.value != '.':
                    #print("Error: . is expected")
                    return

                self.read()
                self.procE()
                # #print('E->fn Vb . E')
                self.buildTree("lambda", n+1)

            case _:
                self.procEw()
                # #print('E->Ew')

    def procEw(self):
        #print('procEw')
        self.procT()
        # #print('Ew->T')
        if self.current_token.value == 'where':
            self.read()
            self.procDr()
            # #print('Ew->T where Dr')
            self.buildTree("where", 2)

    def procT(self):
        # print('procT')
        self.procTa()
        # print('T->Ta')

        n = 0
        while self.current_token.value == ',':
            self.read()
            self.procTa()
            n += 1
            # print('T->Ta , Ta')
        if n > 0:
            self.buildTree("tau", n + 1)
        else:
            pass
            # print('T->Ta')

    def procTa(self):
        # print('procTa')
        self.procTc()
        # print('Ta->Tc')
        while self.current_token.value == 'aug':
            self.read()
            self.procTc()
            # print('Ta->Tc aug Tc')

            self.buildTree("aug", 2)

    def procTc(self):
        # print('procTc')

        self.procB()
        # print('Tc->B')
        if self.current_token.type == Tokernizer.TokenType.TERNARY_OPERATOR:
            self.read()
            self.procTc()

            if self.current_token.value != '|':
                print("Error: | is expected")
                return
            self.read()
            self.procTc()
            # print('Tc->B -> Tc | Tc')
            self.buildTree("->", 3)

    def procB(self):
        # print('procB')

        self.procBt()
        # print('B->Bt')
        while self.current_token.value == 'or':
            self.read()
            self.procBt()
            # print('B->B or B')
            self.buildTree("or", 2)

    def procBt(self):
        # print('procBt')

        self.procBs()
        # print('Bt->Bs')
        while self.current_token.value == '&':
            self.read()
            self.procBs()
            # print('Bt->Bs & Bs')
            self.buildTree("&", 2)

    def procBs(self):
        # print('procBs')

        if self.current_token.value == 'not':
            self.read()
            self.procBp()
            # print('Bs->not Bp')
            self.buildTree("not", 1)
        else:
            self.procBp()
            # print('Bs->Bp')

    def procBp(self):
        # print('procBp')

        self.procA()
        # print('Bp->A')
        # print(self.current_token.value+"######")

        ##  Bp -> A ( 'gr' | '>') A
        match self.current_token.value:
            case '>':
                self.read()
                self.procA()
                # print('Bp->A gr A')
                self.buildTree("gr", 2)
            case 'gr':
                self.read()
                self.procA()
                # print('Bp->A gr A')
                self.buildTree("gr", 2)

            case 'ge':
                self.read()
                self.procA()
                # print('Bp->A ge A')
                self.buildTree("ge", 2)

            case '>=':
                self.read()
                self.procA()
                # print('Bp->A ge A')
                self.buildTree("ge", 2)



            case '<':
                self.read()
                self.procA()
                # print('Bp->A ls A')
                self.buildTree("ls", 2)

            case 'ls':
                self.read()
                self.procA()
                # print('Bp->A ls A')
                self.buildTree("ls", 2)

            case '<=':
                self.read()
                self.procA()
                # print('Bp->A le A')
                self.buildTree("le", 2)

            case 'le':
                self.read()
                self.procA()
                # print('Bp->A le A')
                self.buildTree("le", 2)

            case 'eq':
                self.read()
                self.procA()
                # print('Bp->A eq A')
                self.buildTree("eq", 2)

            case 'ne':
                self.read()
                self.procA()
                # print('Bp->A ne A')
                self.buildTree("ne", 2)

            case _:
                return

    def procA(self):
        # print('procA')

        if self.current_token.value == '+':
            self.read()
            self.procAt()
            # print('A->+ At')
            # self.buildTree("+", 1)

        elif self.current_token.value == '-':
            self.read()
            self.procAt()
            # print('A->- At')
            self.buildTree("neg", 1)


        else:
            self.procAt()
            # print('A->At')
        plus = '+'
        while self.current_token.value == '+' or self.current_token.value == '-':

            if self.current_token.value=='-':
                plus='-'

            self.read()
            self.procAt()
            # print('A->A + / -At')
            # print(self.current_token.value)
            self.buildTree(plus, 2)


    def procAt(self):
        # print('procAt')

        self.procAf()
        # print('At->Af')
        while self.current_token.value == '*' or self.current_token.value == '/':
            self.read()
            self.procAf()
            # print('At->Af * Af')
            # print("current token value " + self.current_token.value)
            self.buildTree("*", 2)

    def procAf(self):
        # print('procAf')

        self.procAp()
        # print('Af->Ap')
        while self.current_token.value == '**':
            self.read()
            self.procAf()
            # print('Af->Ap ** Af')
            self.buildTree("**", 2)

    def procAp(self):
        # print('procAp')

        self.procR()
        # print('Ap->R')
        while self.current_token.value == '@':
            self.read()
            self.procR()
            # print('Ap->R @ R')
            self.buildTree("@", 2)

    def procR(self):
        # print('procR')

        self.procRn()
        # print('R->Rn')
        # self.read()

        while (self.current_token.type in [Tokernizer.TokenType.ID, Tokernizer.TokenType.INT,
                                           Tokernizer.TokenType.STRING] or self.current_token.value in ['true', 'false',
                                                                                                        'nil', 'dummy',
                                                                                                        "("]):
            if self.index >= len(self.tokens):
                break
            self.procRn()
            # print('R->R Rn')
            self.buildTree("gamma", 2)

            # self.read()

    def procRn(self):
        # print("procRn")

        if self.current_token.type in [Tokernizer.TokenType.ID, Tokernizer.TokenType.INT,
                                       Tokernizer.TokenType.STRING]:

            # print('Rn->' + str(self.current_token.value))

            self.read()

            # self.read()
            # self.buildTree("id", 0)
        elif self.current_token.value in ['true', 'false', 'nil', 'dummy']:
            # print('Rn->' + self.current_token.value)
            self.read()
            # print("self.current_token.value" , self.current_token.value)
            # self.buildTree(self.current_token.value, 0)
        elif self.current_token.value == '(':
            self.read()
            self.procE()
            if self.current_token.value != ')':
                # print("Error: ) is expected")
                return
            self.read()
            # print('Rn->( E )')
            # self.buildTree("()", 1)

    def procD(self):
        # print('procD')

        self.procDa()
        # print('D->Da')
        while self.current_token.value == 'within':
            self.read()
            self.procD()
            # print('D->Da within D')
            self.buildTree("within", 2)

    def procDa(self):
        # print('procDa')

        self.procDr()
        # print('Da->Dr')
        n = 0
        while self.current_token.value == 'and':
            n += 1
            self.read()
            self.procDa()
            # print('Da->and Dr')
        # if n == 0:
        #     print("Error")
        #     return
        if n > 0:
            self.buildTree("and", n + 1)

    def procDr(self):
        # print('procDr')

        if self.current_token.value == 'rec':
            self.read()
            self.procDb()
            # print('Dr->rec Db')
            self.buildTree("rec", 1)

        self.procDb()
        # print('Dr->Db')

    def procDb(self):
        # print('procDb')

        if self.current_token.value == '(':
            self.read()
            self.procD()
            if self.current_token.value != ')':
                # print("Error: ) is expected")
                return
            self.read()
            # print('Db->( D )')
            self.buildTree("()", 1)

        elif self.current_token.type == Tokernizer.TokenType.ID:
            self.read()

            if self.current_token.type == Tokernizer.TokenType.COMMA:
                # Db -> Vl '=' E => '='
                self.read()
                self.procVb()

                if self.current_token.value != '=':
                    print("Error: = is expected")
                    return
                self.buildTree(",", 2)
                self.read()
                self.procE()
                self.buildTree("=", 2)
            else :
                if self.current_token.value == '=':
                    self.read()
                    self.procE()
                    # print('Db->id = E')
                    self.buildTree("=", 2)

                else :

                    n = 0
                    while self.current_token.type == Tokernizer.TokenType.ID or self.current_token.value == '(':
                        self.procVb()
                        n += 1

                    if n == 0:
                        print("Error: ID or ( is expected")
                        return

                    if self.current_token.value != '=':
                        print("Error: = is expected")
                        return
                    self.read()
                    self.procE()
                    # print('Db->identifier Vb+ = E')
                    self.buildTree("function_form", n + 2)

        # else:
        #     self.procVL()
        #     print(self.current_token.value)
        #     if self.current_token.value != '=':
        #         print("Error: = is expected")
        #         return
        #     self.read()
        #     self.procE()
        #     print('Db->Vl = E')
        #     self.buildTree("=", 2)

    def procVb(self):
        # print('procVb')
        if self.current_token.type == Tokernizer.TokenType.ID:
            self.read()
            # print('Vb->id')
            # self.buildTree("id", 1)

        elif self.current_token.value == '(':
            self.read()
            # print(self.current_token.value)
            if self.current_token.type == ')':
                # print('Vb->( )')
                self.buildTree("()", 0)
                self.read()
            else:
                self.procVL()
                # print('Vb->( Vl )')
                if self.current_token.value != ')':
                    print("Error: ) is expected")
                    return
            self.read()

            # self.buildTree("()", 1)

        else:
            print("Error: ID or ( is expected")
            return

    def procVL(self):
        # print("procVL")
        # print("559 "+str(self.current_token.value))

        if self.current_token.type != Tokernizer.TokenType.ID:
            pass
            # print("562 VL: Identifier expected")  # Replace with appropriate error handling
        else:
            pass
            # print('VL->' + self.current_token.value)

            self.read()
            trees_to_pop = 0
            while self.current_token.value == ',':
                # Vl -> '<IDENTIFIER>' list ',' => ','?;
                self.read()
                if self.current_token.type != Tokernizer.TokenType.ID:
                    print(" 572 VL: Identifier expected")  # Replace with appropriate error handling
                self.read()
                # print('VL->id , ?')

                trees_to_pop += 1
            # print('498')
            if trees_to_pop > 0:
                self.buildTree(',', trees_to_pop +1)  # +1 for the child identifier





import sys


if len(sys.argv) > 1:
    argv_idx = 1  # Index of file name in argv
    ast_flag = 0  # Flag to check if AST or ST is to be printed

    if len(sys.argv) == 3:  # Check if AST or ST flag is present
        argv_idx = 2
        if sys.argv[2] == "-ast":  # Check if AST flag is present
            print("AST flag is set")
            ast_flag = 1

        input_path = sys.argv[1]
    else:
        # print("Error: CSE machine not yet built . try -ast switch as second argument")
        # sys.exit(1)
        input_path = sys.argv[1]

    # filepath = sys.argv[argv_idx]  # Read file name from command line

# input_path=sys.argv[2]
numeric_result_file=["test_cases/standarizer","test_cases/sum"]
test_results=[]
test_id=0
# input_files=os.listdir("test_cases")

# for input_path in input_files:
with open(input_path) as file:
    program = file.read();

stack = []
tokens = []


# tokenize input
tokenizer = Tokernizer.Tokenizer(program)
token = tokenizer.get_next_token()
while token.type != Tokernizer.TokenType.EOF:
    tokens.append(token)
    token = tokenizer.get_next_token()

#sreen tokens
screener = Screener(tokens)
tokens = screener.screen()

# parse input
# print(" after screening ")
# for token in tokens:
#     print(token.type, token.value)
    # print(token.type, token.value)
parser = ASTParsser()
parser.tokens = tokens
parser.current_token = tokens[0]
parser.index = 0

parser.procE()
# print(len(stack))
root = stack[0]
# root.print_tree()

with open( "output_files/"+input_path.split("\\")[-1], "w") as file:
    root.indentation = 0
    root.print_tree_to_file(file)
    if ast_flag == 1: root.print_tree_to_cmd()
    # root.print_tree_to_cmd()

if ast_flag == 0:
    ASTStandarizer = ASTNode("ASTStandarizer")
    root= ASTStandarizer.standarize(root)
    # print("###### Standarized tree ######")
    # root.print_tree_to_cmd()
    with open(input_path+"__standarized_output", "w") as file:
        root.indentation = 0
        root.print_tree_to_file(file)

    ctrlStructGen = controlStructure.ControlStructureGenerator()
    ctr_structures=ctrlStructGen.generate_control_structures(root)
    # ctrlStructGen.print_ctrl_structs()

    cseMachine= CSEMachine(ctr_structures ,input_path)
    result=cseMachine.execute()



    # if input_path in numeric_result_file :
    #
    #     if int(result) == r:
    #         test_results.append( (input_path ,"test passed"))
    #     else:
    #         test_results.append( (input_path ,"test failed"))
    #
    # else :
    #
    #     if (result) == r:
    #         test_results.append( (input_path ,"test passed"))
    #     else:
    #         test_results.append( (input_path ,"test failed"))
    # (  result)

    for t in test_results:
        id+=1

        # if t[1] == "test passed":
        #     print( t[0]+": "+  GREEN + t[1] + RESET)
        # else :
        #     print(t[0]+": "+  RED + t[1] + RESET)


    # print(CSEMachine.results)