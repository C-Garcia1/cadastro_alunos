import sqlite3

def conectar_banco():
    conectar = sqlite3.connect('sql/banco.db')
    conectar.execute("PRAGMA foreign_keys = ON")
    return conectar

def main():
    conexao = conectar_banco()
    print("Banco conectado com sucesso!")
    conexao.close()

if __name__ == "__main__":
    main()
