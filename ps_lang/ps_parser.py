from sly import Parser
import ps_lexer

class BasicParser(Parser):
    tokens = ps_lexer.BasicLexer.tokens
    
    precedence = (
        ('left', '+', '-'),
        ('left', '*', '/'),
        ('right', 'UMINUS'),
    )

    def __init__(self):
        self.env = {}

    @_('')
    def statement(self, p):
        pass

    @_('FOR penetapan_variabel TO expr THEN statement')
    def statement(self, p):
        return ('for_loop', ('for_loop_setup', p.penetapan_variabel, p.expr), p.statement)

    @_('IF kondisi THEN statement ELSE statement')
    def statement(self, p):
        return ('IF_sajak', p.kondisi, ('cabang', p.statement0, p.statement1))

    @_('TRY NAME "(" ")" ARROW statement')
    def statement(self, p):
        return ('coba_def', p.NAME, p.statement)

    @_('NAME "(" ")"')
    def statement(self, p):
        return ('coba_call', p.NAME)

    @_('expr EQEQ expr')
    def kondisi(self, p):
        return ('EQEQ_kondisi', p.expr0, p.expr1)

    @_('penetapan_variabel')
    def statement(self, p):
        return p.penetapan_variabel

    @_('NAME "=" expr')
    def penetapan_variabel(self, p):
        return ('penetapan_variabel', p.NAME, p.expr)

    @_('NAME "=" STRING')
    def penetapan_variabel(self, p):
        return ('penetapan_variabel', p.NAME, p.STRING)

    @_('expr')
    def statement(self, p):
        return (p.expr)

    @_('expr "+" expr')
    def expr(self, p):
        return ('tambah', p.expr0, p.expr1)

    @_('expr "-" expr')
    def expr(self, p):
        return ('kurang', p.expr0, p.expr1)

    @_('expr "*" expr')
    def expr(self, p):
        return ('kali', p.expr0, p.expr1)

    @_('expr "/" expr')
    def expr(self, p):
        return ('bagi', p.expr0, p.expr1)

    @_('"-" expr %prec UMINUS')
    def expr(self, p):
        return p.expr

    @_('NAME')
    def expr(self, p):
        return ('variabel', p.NAME)

    @_('NUMBER')
    def expr(self, p):
        return ('angka', p.NUMBER)


if __name__ == '__main__':
   
    print("--------------------------------------------- PENIKMAT SENJA PARSING ------------------------------------------------")
   
    lexer = ps_lexer.BasicLexer()
    parser = BasicParser()
    env = {}
   
    while True:
        try:
            text = input('penikmat_senja ~ ')
        except EOFError:
            break
        if text:
            tree = parser.parse(lexer.tokenize(text))
            print(tree)
