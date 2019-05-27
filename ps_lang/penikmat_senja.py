import ps_lexer
import ps_parser


class BasicExecute:

    def __init__(self, tree, env):
        self.env = env
        result = self.walkTree(tree)
        if result is not None and isinstance(result, int):
            print(result)
        if isinstance(result, str) and result[0] == '"':
            print(result)

    def walkTree(self, node):

        if isinstance(node, int):
            return node
        if isinstance(node, str):
            return node

        if node is None:
            return None

        if node[0] == 'program':
            if node[1] == None:
                self.walkTree(node[2])
            else:
                self.walkTree(node[1])
                self.walkTree(node[2])

        if node[0] == 'angka':
            return node[1]

        if node[0] == 'str':
            return node[1]

        if node[0] == 'IF_sajak':
            result = self.walkTree(node[1])
            if result:
                return self.walkTree(node[2][1])
            return self.walkTree(node[2][2])

        if node[0] == 'EQEQ_kondisi':
            return self.walkTree(node[1]) == self.walkTree(node[2])

        if node[0] == 'coba_def':
            self.env[node[1]] = node[2]

        if node[0] == 'coba_call':
            try:
                return self.walkTree(self.env[node[1]])
            except LookupError:
                print("Percayalah engkau merupakan fungsi yang tak terdefinisi '%s'" % node[1])
                return 0

        if node[0] == 'tambah':
            return self.walkTree(node[1]) + self.walkTree(node[2])
        elif node[0] == 'kurang':
            return self.walkTree(node[1]) - self.walkTree(node[2])
        elif node[0] == 'kali':
            return self.walkTree(node[1]) * self.walkTree(node[2])
        elif node[0] == 'bagi':
            return self.walkTree(node[1]) / self.walkTree(node[2])

        if node[0] == 'penetapan_variabel':
            self.env[node[1]] = self.walkTree(node[2])
            return node[1]

        if node[0] == 'variabel':
            try:
                return self.env[node[1]]
            except LookupError:
                print("Wahai variabel '" + node[1] +"' yang tak terdefinisi kenapa engkau disini")
                return 0

        if node[0] == 'for_loop':
            if node[1][0] == 'for_loop_setup':
                loop_setup = self.walkTree(node[1])

                loop_count = self.env[loop_setup[0]]
                loop_limit = loop_setup[1]

                for i in range(loop_count+1, loop_limit+1):
                    res = self.walkTree(node[2])
                    if res is not None:
                        print(res)
                    self.env[loop_setup[0]] = i
                del self.env[loop_setup[0]]

        if node[0] == 'for_loop_setup':
            return (self.walkTree(node[1]), self.walkTree(node[2]))


if __name__ == '__main__':

    print("--------------------------------------- PENIKMAT SENJA PROGRAMMING LANGUAGE ------------------------------------------")
    env = {}
    
    while True:
        try:
            text = input('penikmat_senja ~ ')
        except EOFError:
            break
        if text:
            lexer = ps_lexer.BasicLexer()
            parser = ps_parser.BasicParser()
            tree = parser.parse (lexer.tokenize(text))
            BasicExecute(tree, env)
