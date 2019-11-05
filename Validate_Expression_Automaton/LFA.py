import re
import sys


def check_expression(exp):

    beforeEqual = ''
    afterEqual = ''
    result = ''
    equal = ''
    igual = ''

    # transforma a expressão algébrica em uma lista de caracteres
    for ex, pos in enumerate(exp):
        aux = list(pos)
        # verifica o primeiro caractere do identificador
        if re.search(r"[a-z]", aux[0]):
            # valida o identificador até encontrar o sinal de igual ('=')
            for carac in aux:
                if re.search(r"[^0-9A-Z]?[a-z0-9_]+[^A-Z]?", carac):
                    beforeEqual += carac
                elif re.search(r"=", carac):
                    # armazena a posição do valor de igual
                    equal = aux.index(carac)
                    igual = carac
                    break
                else:
                    print('Identificador com valor inválido!')
                    break
            # armazena o identificador e o valor de igual
            result += beforeEqual + igual

        # laço para verificar a expressão após o valor de igual
        for k in aux[equal+1:]:  # equal recebe +1 para pegar o que vem depois do valor de igual
            validate = ''
            afterEqual += k
            # verifica a expressão quando encontra operadores e valida
            if re.search(r'[\+\-\*\/\;]', afterEqual):
                validate += afterEqual[:-1]
                # verifica o primeiro caractere do identificador
                if re.search(r'[a-z]', validate[0]):
                    for l in validate:
                        if re.search(r'[^0-9A-Z]?[a-z0-9_]+[^A-Z]?', l):
                            result += l
                        else:
                            print('Identificador com valor inválido!')
                            sys.exit(0)
                elif re.search(r'[0-9]', validate[0]):
                    for m in validate:
                        if re.search(r'[0-9]+', m):
                            result += m
                        elif re.search(r'[.]', m):
                            result += m
                        elif re.search(r'[a-zA-Z]', m):  # caso houver letra depois do início com número
                            print('Identificador com valor numérico!')
                            sys.exit(0)

                # adicionar os operadores
                result += afterEqual[-1]
                afterEqual = ''

            # o que vem após ';', ignora
            if re.search(r';', k):
                print('Fim da expressão!')
                break
        else:
            print('Identificador com valor inicial incorreto!')
            break

    return result


def calc(expression, vars):

    account = expression.split('=')[1]
    numbers = ''
    aux = ''

    for v in vars:
        iden = v.split('=')[0].strip()
        value = v.split('=')[1].strip()
        for ac in account:
            aux += ac
            if re.search(r'[\+\-\*\/\;]', aux):
                # caso houver identificador, realiza a troca pelo seu valor
                if aux[:-1] == iden:
                    account = account.replace(aux[:-1], value)
                    numbers = account
                # se não, pega o valor do número
                else:
                    numbers = account

                aux = ''

    print('------------------')
    print(f'Expressão -> {numbers}')
    print('------------------')

    # -1 para não pegar ;
    result = eval(numbers[:-1])
    print(f'Resultado = {result}')


if __name__ == '__main__':

    var = []
    varFormatted = []
    expression = []

    # leitura do arquivo
    with open('arq.txt', 'r') as fp:
        leitura = fp.readlines()
        for i in leitura:
            if len(i.strip()) != 0:
                # valores das variáveis são adicionados na lista var
                var.append(i)
            else:
                break
        # última linha referente a expressão é adicionada na lista expression
        expression.append(leitura[-1])

    for j in var:
        varFormatted.append(j.replace('\n', ''))

    validatedExpression = check_expression(expression)

    calc(validatedExpression, varFormatted)
