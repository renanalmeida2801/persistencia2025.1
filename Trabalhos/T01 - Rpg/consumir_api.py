import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def menu():
    print("\n--- CONSUMIDOR DE API FASTAPI ---")
    print("1. CRUD - Criar entidade")
    print("2. CRUD - Listar entidades")
    print("3. CRUD - Atualizar entidade")
    print("4. CRUD - Deletar entidade")
    print("5. Quantidade de registros")
    print("6. Download ZIP")
    print("7. Filtrar registros")
    print("8. Hash SHA256 do CSV")
    print("9. Exportar para XML")
    print("0. Sair")

def escolher_entidade():
    print("\n--- Escolha a entidade ---")
    print("1. Personagem")
    print("2. Habilidade")
    print("3. Equipamento")
    escolha = input(">> ")
    return ["personagem", "habilidade", "equipamento"][int(escolha) - 1]

def criar(entidade):
    dados = json.loads(input(f"Digite os dados do(a) {entidade} como JSON:\n>> "))
    r = requests.post(f"{BASE_URL}/{entidade}", json=dados)
    print("Status:", r.status_code)
    print("Resposta:", r.json())

def listar(entidade):
    r = requests.get(f"{BASE_URL}/{entidade}")
    print("Status:", r.status_code)
    print(json.dumps(r.json(), indent=2, ensure_ascii=False))

def atualizar(entidade):
    id_entidade = input(f"ID do(a) {entidade} a atualizar: ")
    dados = json.loads(input(f"Digite os dados atualizados (incluindo o mesmo ID):\n>> "))
    r = requests.put(f"{BASE_URL}/{entidade}/{id_entidade}", json=dados)
    print("Status:", r.status_code)
    print("Resposta:", r.json())

def deletar(entidade):
    id_entidade = input(f"ID do(a) {entidade} a deletar: ")
    r = requests.delete(f"{BASE_URL}/{entidade}/{id_entidade}")
    print("Status:", r.status_code)
    print("Resposta:", r.json())

def quantidade(entidade):
    r = requests.get(f"{BASE_URL}/{entidade}/quantidade")
    print("Status:", r.status_code)
    print("Resposta:", r.json())

def zipar(entidade):
    r = requests.get(f"{BASE_URL}/{entidade}/zip")
    with open(f"{entidade}.zip", "wb") as f:
        f.write(r.content)
    print(f"Arquivo {entidade}.zip salvo com sucesso.")

def filtrar(entidade):
    print("Digite o filtro (ex: classe=Monge ou tipo=Espada):")
    chave, valor = input(">> ").split("=")
    r = requests.get(f"{BASE_URL}/{entidade}/filtrar", params={chave.strip(): valor.strip()})
    print("Status:", r.status_code)
    print(json.dumps(r.json(), indent=2, ensure_ascii=False))

def hash_csv(entidade):
    r = requests.get(f"{BASE_URL}/{entidade}/hash")
    print("Status:", r.status_code)
    print("Hash SHA256:", r.json())

def xml(entidade):
    r = requests.get(f"{BASE_URL}/{entidade}/xml")
    with open(f"{entidade}.xml", "wb") as f:
        f.write(r.content)
    print(f"Arquivo {entidade}.xml salvo com sucesso.")

def main():
    while True:
        menu()
        opcao = input("Escolha uma opção: ")
        if opcao == "0":
            print("Saindo...")
            break
        if opcao not in map(str, range(1, 10)):
            print("Opção inválida.")
            continue
        entidade = escolher_entidade()
        try:
            {
                "1": criar,
                "2": listar,
                "3": atualizar,
                "4": deletar,
                "5": quantidade,
                "6": zipar,
                "7": filtrar,
                "8": hash_csv,
                "9": xml
            }[opcao](entidade)
        except Exception as e:
            print("Erro:", e)

if __name__ == "__main__":
    main()
