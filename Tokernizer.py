from enum import Enum

PUNCTION = ['(', ')', ';', ',']


class Token():
    def __init__(self, type, value):
        self.type = type
        self.value = value


RESERVED_KEYWORDS = ['where', 'let', 'aug', 'within' ,'in' ,'rec' ,'eq']


# token type e
# num
class TokenType(Enum):
    RESERVED_KEYWORD = 'RESERVED_KEYWORD'

    ID = 'ID'
    COMMENT = 'COMMENT'
    INT = 'INT'
    PLUS = 'PLUS'  # +
    MINUS = 'MINUS'  # -
    MUL = 'MUL'  # *
    DIV = 'DIV'  # /
    GREATER_THAN = 'GREATER_THAN'  # >
    LESSER_THAN = 'LESSER_THAN'  # <
    AMPERSAND_OPERATOR = 'AMPERSAND_OPERATOR'  # &
    DOT_OPERATOR = 'DOT_OPERATOR'  # .
    AT_OPERATOR = 'AT_OPERATOR'  # @
    SEMICOLON = 'SEMICOLON'  # ;
    EQUAL = 'EQUAL'  # =
    CURL = 'CURL'  # ~
    SQUARE_OPEN_BRACKET = 'SQUARE_OPEN_BRACKET'  # [
    SQUARE_CLOSE_BRACKET = 'SQUARE_CLOSE_BRACKET'  # ]
    DOLLAR = 'DOLLAR'  # $
    EXCLAMATION_MARK = 'EXCLAMATION_MARK'
    HASH_TAG = 'HASH_TAG'
    MODULUS = 'MODULUS'
    CARROT = 'CARROT'
    CURLY_OPEN_BRACKET = 'CURLY_OPEN_BRACKET'
    CURLY_CLOSE_BRACKET = 'CURLY_CLOSE_BRACKET'
    BACK_TICK = 'BACK_TICK'
    DOUBLE_QUOTE = 'DOUBLE_QUOTE'
    QUESTION_MARK = 'QUESTION_MARK'
    PUNCTION = 'PUNCTION'
    OR_OPERATOR = 'OR_OPERATOR'
    STRING = 'STRING'
    TERNARY_OPERATOR = 'TERNARY_OPERATOR'

    EOF = 'EOF'


class LEX_STATE:
    def __init__(self):
        self.line_number = 0
        self.current_char = None
        self.column_number = None


class Tokenizer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.state = LEX_STATE()

        self.state.current_char = self.text[self.pos]
        self.state.line_number = 1
        self.state.column_number = 1

    def error(self):
        raise Exception('Error parsing input')

    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.state.current_char = None  # Indicates end of input
        else:
            self.state.current_char = self.text[self.pos]
            self.state.column_number += 1

    def skip_whitespace(self):
        while self.state.current_char is not None and self.state.current_char.isspace():
            if self.state.current_char == '\n':
                self.state.line_number += 1
                self.state.column_number = 0
            self.advance()

    def integer(self):
        result = ''
        while self.state.current_char is not None and self.state.current_char.isdigit():
            result += self.state.current_char
            self.advance()
        return int(result)

    def identifier(self):
        result = ''
        while self.state.current_char is not None and (
                self.state.current_char.isalpha() or self.state.current_char.isdigit() or self.state.current_char == '_'):
            result += self.state.current_char
            self.advance()
        return result

    def comment(self):
        result = ''
        while self.state.current_char is not None and self.state.current_char != '\n':
            result += self.state.current_char
            self.advance()
        return result

    def isCommnet(self):
        if self.state.current_char is not None and self.state.current_char == '/':
            return True
        else:
            return False

    def string(self):
        result = ''
        while self.state.current_char is not None and self.state.current_char != "'":
            result += self.state.current_char
            self.advance()
        return result

    def get_next_token(self):
        while self.state.current_char is not None:

            if self.state.current_char.isspace():
                self.skip_whitespace()
                continue

            # tokenize digits
            elif self.state.current_char.isdigit():
                return Token(TokenType.INT, self.integer())

            ## tokenize identifier
            elif self.state.current_char.isalpha():
                return Token(TokenType.ID, self.identifier())


            # read comment or punctuation

            # elif self.state.current_char == "/":
            #
            #
            #     self.advance()
            #
            #     # punctuation
            #     if self.state.current_char == '/':
            #         self.advance()
            #         return  Token (TokenType.COMMENT,self.comment())
            #     else :
            #         return Token(TokenType.DIV, '/')

            # tokenoze string starting with '''
            elif self.state.current_char == "'":
                self.advance()
                return Token(TokenType.STRING, self.string())


            # tokenize punctuation
            elif self.state.current_char in PUNCTION:
                token = Token(TokenType.PUNCTION, self.state.current_char)
                self.advance()
                return token








            elif self.state.current_char == '+':
                self.advance()
                return Token(TokenType.PLUS, '+')

            elif self.state.current_char == '-':
                self.advance()
                return Token(TokenType.MINUS, '-')

            elif self.state.current_char == '*':
                self.advance()
                return Token(TokenType.MUL, '*')

            elif self.state.current_char == '<':
                self.advance()
                return Token(TokenType.GREATER_THAN, '<')

            elif self.state.current_char == '>':
                self.advance()
                return Token(TokenType.LESSER_THAN, '>')

            elif self.state.current_char == '&':
                self.advance()
                return Token(TokenType.AMPERSAND_OPERATOR, '&')

            elif self.state.current_char == '.':
                self.advance()
                return Token(TokenType.DOT_OPERATOR, '.')

            elif self.state.current_char == '@':
                self.advance()
                return Token(TokenType.AT_OPERATOR, '@')

            elif self.state.current_char == ';':
                self.advance()
                return Token(TokenType.SEMICOLON, ';')

            elif self.state.current_char == '=':
                self.advance()
                return Token(TokenType.EQUAL, '=')

            elif self.state.current_char == '~':
                self.advance()
                return Token(TokenType.CURL, '~')

            elif self.state.current_char == '[':
                self.advance()
                return Token(TokenType.SQUARE_OPEN_BRACKET, '[')

            elif self.state.current_char == ']':
                self.advance()
                return Token(TokenType.SQUARE_CLOSE_BRACKET, ']')

            elif self.state.current_char == '$':
                self.advance()
                return Token(TokenType.DOLLAR, '$')

            elif self.state.current_char == '!':
                self.advance()
                return Token(TokenType.EXCLAMATION_MARK, '!')

            elif self.state.current_char == '#':
                self.advance()
                return Token(TokenType.HASH_TAG, '#')

            elif self.state.current_char == '%':
                self.advance()
                return Token(TokenType.MODULUS, '%')

            elif self.state.current_char == '^':
                self.advance()
                return Token(TokenType.CARROT, '^')

            elif self.state.current_char == '{':
                self.advance()
                return Token(TokenType.CURLY_OPEN_BRACKET, '{')

            elif self.state.current_char == '}':
                self.advance()
                return Token(TokenType.CURLY_CLOSE_BRACKET, '}')

            elif self.state.current_char == '`':
                self.advance()
                return Token(TokenType.BACK_TICK, '`')

            elif self.state.current_char == '\"':
                self.advance()
                return Token(TokenType.DOUBLE_QUOTE, '\"')

            elif self.state.current_char == '?':
                self.advance()
                return Token(TokenType.QUESTION_MARK, '?')

            elif self.state.current_char == '|':
                self.advance()
                return Token(TokenType.OR_OPERATOR, '|')

            self.error()

        return Token(TokenType.EOF, None)


# read input
# text = input('calc> ')




class Screener:
    def __init__(self,tokens):
        self.text = None
        self.tokens=tokens

    def merge_tokens(self ):
        tokens=self.tokens
        for i in range(len(tokens)):
            if i < len(tokens) and tokens[i].type == TokenType.MINUS and tokens[i + 1].type == TokenType.LESSER_THAN:
                tokens[i].value = '->'
                tokens[i].type = TokenType.TERNARY_OPERATOR
                tokens.pop(i + 1)
        self.tokens=tokens



    def screen(self):
        self.merge_tokens()
        return self.tokens


with open("test") as file:
    program = file.read();
    print(program)

# tokenize input
tokenizer = Tokenizer(program)
token = tokenizer.get_next_token()
tokens = []

tokens.append(token)
while token.type != TokenType.EOF:
    print(token.type, token.value)

    token = tokenizer.get_next_token()
    tokens.append(token)

screener = Screener(tokens)
tokens = screener.screen()

for token in tokens:
    print(token.type, token.value)
