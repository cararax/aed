# Pedro Hasan Carara - 201811385
import re

### Nome do Produto ###
# O nome do produto deve ser composto por palavras que começam com letras maiúsculas;
# Pode ter várias palavras separadas por espaços;
# Deve conter no mínimo 3 palavras.
productName = [
    "Camiseta Polo Masculina",
    "Tênis Esportivo Masculino",
    "Bermuda Jeans Masculina",
    "Vestido Longo Estampado",
    "camiseta polo masculina",
    "Camisa Masculina",
    "Calça Jeans Slim",
    "Blusa De Frio",
    "Jaqueta Masculina Couro",
    "Boné Vermelho Casual",
    "Mochila Escolar Grande",
    "Tênis Corrida Branco"]

patterName = re.compile(r'(?P<palavra>\b[A-Z]\w+\s?){3}')
# Explicação: A partir da borda inicial, a palavra deve conter 1 letra maiuscula, deve ter uma ou mais letras e pode ter espaço  no final, esse conjunto deve estar presente 3 vezes

print(f'Nome do produto: ')
for name in productName:
    print(f'{"OK" if patterName.fullmatch(name) else "INVÁLIDO":8} | {name}')
print(f'')

### Código do produto ###
# O código do produto deve ser composto por 6 letras maiúsculas seguidas de 4 números (formato: ABCDEF1234);
# Não pode conter espaços ou caracteres especiais

productCode = [
    "ABCDEF1234",
    "ZXCVBN5678",
    "QWERTY0001",
    "LONGDR1234",
    "abcdef1234",
    "ABC1234@",
    "ABCDE1234",
    "1234567890",
    "C0D1C01234",
    "VERMEL0000",
    "MOCHIL123",
    "RUNSHO1234"]

patternCode = re.compile(r'(?P<codigo>[A-Z]{6}\d{4})')
# Explicação: a palavra deve ter 6 letras maiusculas e 4 numeros

print(f'Código do Produto: ')
for code in productCode:
    print(f'{"VÁLIDO" if patternCode.fullmatch(code) else "INVÁLIDO":8} | {code}')
print(f'')

### Preço ###
# O preço do produto deve ser um número com até 2 casas decimais;
# Deve ser um valor positivo, podendo incluir um ponto (para separação de casas decimais) ou vírgula;
# O preço não pode ter mais de duas casas decimais (exemplo: 99.99 ou 99,99).

productPrice = [
    "99.99",
    "149,90",
    "79.9",
    "120.00",
    "99.999",
    "-49,90",
    "100,999",
    "0.00",
    "abc",
    "199",
    "250.5",
    "300,00"]

patternPrice = re.compile(r'(?P<inteiro>^\d{1,})'
                          r'(?P<separador>\.{1}|,{1})'
                          r'(?P<flutuante>\d{0,2})$')
# Explicação: a palavra deve começar com pelo menos um numero, deve ter uma virgula ou um ponto e terminar com 2 digitos

print(f'Preço: ')
for price in productPrice:
    print(f'{"OK" if patternPrice.fullmatch(price) else "INVÁLIDO":8} | {price}')
print(f'')

### Data Validade ###
# A data de validade do produto deve estar no formato DD/MM/AAAA;
# O dia deve estar entre 01 e 31, o mês entre 01 e 12, e o ano deve ser composto por 4 dígitos.

productExpiratonDate = [
    "15/12/2025",
    "01/01/2026",
    "31/10/2025",
    "28/02/2024",
    "15/12/25",
    "32/12/2025",
    "30-12-2025",
    "00/00/0000",
    "31/04/2025",  # abril nao tem 31 dias
    "29/02/2023",  # 2023 não é bissexto
    "12/13/2025",
    "15/06/2030"]

patternExpirationDate = re.compile(r'(?P<dia>0[1-9]|1[\d]|2[\d]|3[0-1])'
                                   r'/'
                                   r'(?P<mes>0[1-9]|1[0-2])'
                                   r'/'
                                   r'(?P<ano>\d{4})')

# Explicação: A palavra deve ser composta por 3 grupos separados por barra (/). O primeiro grupo pode ser composto por 3 opções: numeros de 2 digitos que iniciam com 0 e o segundo digito vai de 1 a 9 ou numeros de 2 digitos que iniciam com 2 e o segundo digito vai de 0 a 9 ou numeros de 2 digitos que iniciam com 3 e o segundo digito vai de 0 a 1. O segundo grupo pode ser composto por 2 opções: numero de 2 digitos que iniciam em 0 e o segundo digito vai de 1 a 9 ou numeros de 2 digitos que iniciam em 1 e o segundo digito vai de 0 a 2. O terceiro grupo é um  numero de 4 digitos.
print(f"Data de Validade:")
for date in productExpiratonDate:
    print(f'{"OK" if patternExpirationDate.fullmatch(date) else "INVÁLIDO":8} | {date}')
