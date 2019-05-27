from sly import Lexer


class BasicLexer(Lexer):
    tokens = {NAME, NUMBER, STRING, IF, THEN, ELSE, FOR, TRY, TO, ARROW, EQEQ}
    ignore = '\t '

    literals = {'=', '+', '-', '/', '*', '(', ')', ',', ';'}

    # Menetapkan tokens
    IF = r'Jika_sajak'
    THEN = r'Maka_angan'
    ELSE = r'Lainnya_sendu'
    FOR = r'Untuk_nuansa'
    TRY = r'Coba_bangkit'
    TO = r'Sampai_redup'
    ARROW = r'->'
    NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
    STRING = r'\".*?\"'

    EQEQ = r'=='

    @_(r'\d+')
    def NUMBER(self, t):
        t.value = int(t.value)
        return t

    @_(r'#.*')
    def COMMENT(self, t):
        pass

    @_(r'\n+')
    def newline(self, t):
        self.lineno = t.value.count('\n')


if __name__ == '__main__':
    
    print("--------------------------------------------- PENIKMAT SENJA LEXING ------------------------------------------------")
    
    lexer = BasicLexer()
    env = {}
    
    while True:
        try:
            text = input('penikmatsenja ~ ')
        except EOFError:
            break
        if text:
            lex = lexer.tokenize(text)
            for token in lex:
                print(token)
