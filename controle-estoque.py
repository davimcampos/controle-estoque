import mysql.connector
import pandas as pd


conexao = mysql.connector.connect(
    host='localhost',
    user='root',
    password='1234',
    database='estoque',
)

cursor = conexao.cursor()


def menu():
    print("\n 1-Armazenar produto\n 2-Consultar estoque\n 3-Adicionar/Remover unidade do produto\n 4-Entrada/Saida de produtos\n 5-Remover produto do estoque")
    opcao = input("\nDigite: ")
    if (opcao == "1"):
        opcao1()
    if (opcao == "2"):
        opcao2()
    if (opcao == "3"):
        opcao3()
    if (opcao == "4"):
        opcao4()
    if (opcao == "5"):
        opcao5()
    else:
        print("\nComando inválido.")
        menu()


def adicionar():
    produtoAdicionar = input("Nome do produto: ")
    quantidade = input("quantidade que deseja adicionar: ")
    quantidadeAdicionar = int(quantidade)
    dataAdicao = input("Data da adição - formato: ano-mes-dia: ")
    decisao = input(
        "Tem certeza que deseja adicionar este produto ao estoque? s/n: ")

    if (decisao == "s"):
        comandoProdutos = f'UPDATE produtos SET quantidade = {"quantidade"}+{quantidadeAdicionar} WHERE nom_produto = "{produtoAdicionar}"'
        comandoEntradaSaida = f'INSERT INTO entrada_e_saida(nom_produto, quantidade, data, situacao) VALUES("{produtoAdicionar}", {quantidadeAdicionar}, "{dataAdicao}", "adicionado")'
        cursor.execute(comandoProdutos)
        cursor.execute(comandoEntradaSaida)
        conexao.commit()
        print("\n", quantidadeAdicionar, "unidades do produto",
              produtoAdicionar, "foram adicionados ao estoque.")
        menu()
    if (decisao == "n"):
        print("\nVocê decidiu não adicionar.")
    else:
        print("\ncomando indisponível")
        menu()


def remover():
    produtoRemover = input("Nome do produto: ")
    quantidade = input("quantidade que deseja remover: ")
    quantidadeRemover = int(quantidade)
    dataRemocao = input("Data da remoção - formato: ano-mes-dia: ")
    decisao = input(
        "Tem certeza que deseja remover este produto do estoque? s/n: ")
    if (decisao == "s"):
        comandoProdutos = f'UPDATE produtos SET quantidade = {"quantidade"}-{quantidadeRemover} WHERE nom_produto = "{produtoRemover}"'
        comandoEntradaSaida = f'INSERT INTO entrada_e_saida(nom_produto, quantidade, data, situacao) VALUES("{produtoRemover}", {quantidadeRemover}, "{dataRemocao}", "removido")'
        cursor.execute(comandoProdutos)
        cursor.execute(comandoEntradaSaida)
        conexao.commit()
        print("\n", quantidadeRemover, "unidades do produto",
              produtoRemover, "foram removidas do estoque.")
        menu()
    if (decisao == "n"):
        print("\nVocê decidiu, não deletar.")
        menu()
    else:
        print("\ncomando indisponível")
        menu()


def opcao1():
    print("\n===ARMAZENAR===")
    produto = input("Nome do produto: ")
    quantidadeSTR = input("Quantidade: ")
    quantidade = int(quantidadeSTR)
    dataInclusao = input("Data de inclusão - formato: ano-mes-dia: ")
    comando = f'INSERT INTO produtos(nom_produto, quantidade, data) VALUES("{produto}", {quantidade}, "{dataInclusao}")'
    comandoEntradaSaida = f'INSERT INTO entrada_e_saida(nom_produto, quantidade, data, situacao) VALUES("{produto}", {quantidade}, "{dataInclusao}", "adicionado")'
    cursor.execute(comando)
    cursor.execute(comandoEntradaSaida)
    conexao.commit()
    print(quantidade, "Produtos ", produto,
          "foram adicionados ao estoque.")
    menu()


def opcao2():
    print("\n===CONSULTAR ESTOQUE===\n")
    comando = f'SELECT nom_produto, quantidade FROM produtos'
    cursor.execute(comando)
    resultado = cursor.fetchall()
    df = pd.read_sql(comando, conexao)
    consultarEstoque = pd.DataFrame(df)
    print(consultarEstoque)
    menu()


def opcao3():
    print("\n===ADICIONAR/REMOVER PRODUTO===")
    print("\n1-Adicionar produto\n2-Remover produto\n3-Voltar")
    opcaoRemoverAdicionar = input("Digite: ")
    if (opcaoRemoverAdicionar == "1"):
        adicionar()

    if (opcaoRemoverAdicionar == "2"):
        remover()

    if (opcaoRemoverAdicionar == "3"):
        menu()
    else:
        print("\nopção indisponível")
        menu()


def opcao4():
    print("===ENTRADA E SAÍDA DE PRODUTOS===")
    comando = f'SELECT * FROM entrada_e_saida'
    cursor.execute(comando)
    resultado = cursor.fetchall()
    df = pd.read_sql(comando, conexao)
    tabEntradaSaida = pd.DataFrame(df)
    print(tabEntradaSaida)
    menu()


def opcao5():
    print("==REMOVER PRODUTO DO ESTOQUE==")
    produtoDeletar = input("Nome do produto: ")
    decisao = input(
        "Tem certeza que deseja remover o produto do estoque? s/n: ")
    if (decisao == "s"):
        comando = f'DELETE FROM produtos WHERE nom_produto = "{produtoDeletar}"'
        cursor.execute(comando)
        conexao.commit()
        print("\nO produto", produtoDeletar, "foi removido do estoque.")
        menu()
    if (decisao == "n"):
        print("\nVocê decidiu não remover o produto",
              produtoDeletar, "do estoque.")
        menu()
    else:
        print("\nComando inválido.")


menu()
cursor.close()
conexao.close()
