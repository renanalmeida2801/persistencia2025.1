import requests

BASE_URL = "http://localhost:8000/livros"

def menu():
    print("\n=== MENU APENAS ===")
    print("1. Criar Livro")
    print("2. Listar Livros")
    print("3. Buscar Livro por ID")
    print("4. Editar Livro")
    print("5. Deletar Livro")
    print("0. Sair")

def criar_livro():
    try:
        id = int(input("ID: "))
        titulo = input("Título: ")
        autor = input("Autor: ")
        ano = int(input("Ano: "))
        genero = input("Gênero: ")

        data = {
            "id": id,
            "titulo": titulo,
            "autor": autor,
            "ano": ano,
            "genero": genero
        }

        r = requests.post(BASE_URL, json=data)
        print("Livro Adicionado:", r.json().get("mensagem", r.text))
    except ValueError:
        print("Erro: 'ID' e 'Ano' devem ser números inteiros.")
    except Exception as e:
        print("Erro inesperado:", e)

def listar_livros():
    r = requests.get(BASE_URL)
    livros = r.json()
    if not livros:
        print("Nenhum livro cadastrado.")
        return
    for livro in livros:
        print(f"[{livro['id']}] {livro['titulo']} - {livro['autor']} ({livro['ano']}) [{livro['genero']}]")

def buscar_livro():
    id = input("ID do livro: ")
    r = requests.get(f"{BASE_URL}/{id}")
    if r.status_code == 200:
        livro = r.json()
        print("\nLivro encontrado:")
        print(f"Título : {livro['titulo']}")
        print(f"Autor  : {livro['autor']}")
        print(f"Ano    : {livro['ano']}")
        print(f"Gênero : {livro['genero']}")
    else:
        print("Livro não encontrado.")

def atualizar_livro():
    id = input("ID do livro p/ atualizar: ")
    print("Informe os dados corretos:")
    try:
        titulo = input("Título: ")
        autor = input("Autor: ")
        ano = int(input("Ano: "))
        genero = input("Gênero: ")

        data = {
            "id": int(id),
            "titulo": titulo,
            "autor": autor,
            "ano": ano,
            "genero": genero
        }

        r = requests.put(f"{BASE_URL}/{id}", json=data)
        print("Livro Atualizado:", r.json().get("mensagem", r.text))
    except ValueError:
        print("Erro: Ano deve ser um número inteiro.")
    except Exception as e:
        print("Erro ao atualizar:", e)

def deletar_livro():
    id = input("ID do livro a deletar: ")
    r = requests.delete(f"{BASE_URL}/{id}")
    if r.status_code == 200:
        print("Livro Deletado:", r.json().get("mensagem", r.text))
    else:
        print("Livro não encontrado.")

# Loop principal
while True:
    menu()
    try:
        op = input("Escolha uma opção: ").strip()
        if op == '1':
            criar_livro()
        elif op == '2':
            listar_livros()
        elif op == '3':
            buscar_livro()
        elif op == '4':
            atualizar_livro()
        elif op == '5':
            deletar_livro()
        elif op == '0':
            print("Finalizando...")
            break
        else:
            print("Opção inválida!")
    except KeyboardInterrupt:
        print("\Finalizado.")
        break
