from flask import Flask, render_template, request, redirect
import requests

# Cria a aplicação Flask.
app = Flask(__name__)

# Lista Python simples em memória para armazenar os Pokémons capturados.
colecao = []


# ==============================================================================
# @app.route() é um decorator do Flask. Ele associa a URL "/" à função index().
#  Ele pega a função logo abaixo e a "conecta" ao servidor web do Flask.
#     * GET:  Usado quando o usuário apenas ACESSA ou NAVEGA na página.
#     * POST: Usado quando o usuário ENVIA DADOS (como um formulário de busca).
# ==============================================================================
@app.route('/', methods=['GET', 'POST'])
def index():
    pokemon_encontrado = None
    erro = None

    # Verifica se a requisição é do tipo POST (o usuário clicou em "Buscar")
    if request.method == 'POST':
        # Captura o valor digitado no input 'nome', converte para minúsculas e limpa espaços
        nome = request.form.get('nome').lower().strip()

        # Bloco de Tratamento de Exceções
        try:
            # Chamada HTTP GET para a PokeAPI (timeout de 5 segundos)
            # O parâmetro timeout=5 define o tempo máximo de espera (em segundos) que a sua aplicação aceita aguardar pela resposta do servidor da PokeAPI.
            resposta = requests.get(f"https://pokeapi.co/api/v2/pokemon/{nome}", timeout=5)

            # Código HTTP 200 = Sucesso
            if resposta.status_code == 200:
                dados = resposta.json()
                pokemon_encontrado = {
                    "nome": dados['name'],
                    "sprite": dados['sprites']['front_default']
                }
            else:
                erro = f"O Pokémon '{nome}' não foi encontrado!"

        except requests.exceptions.RequestException:
            erro = "Erro de conexão com a PokeAPI."

    # Renderiza o HTML enviando as variáveis necessárias para o Jinja2
    return render_template('index.html', pokemon=pokemon_encontrado, colecao=colecao, erro=erro)


# ==============================================================================
# ROTA COM PARÂMETRO DINÂMICO
#
# O trecho '<nome>' na URL cria uma variável dinâmica!
# Se o usuário acessar '/capturar/pikachu', a variável 'nome' dentro da função
# receberá a string "pikachu" automaticamente.
#
# Como não especificamos 'methods', o Flask assume que ela aceita apenas 'GET'.
# ==============================================================================
@app.route('/capturar/<nome>')
def capturar(nome):
    try:
        res = requests.get(f"https://pokeapi.co/api/v2/pokemon/{nome}", timeout=5)

        if res.status_code == 200:
            dados = res.json()

            novo_pokemon = {
                "nome": nome,
                "sprite": dados['sprites']['front_default']
            }

            # Adiciona o novo Pokémon à lista
            colecao.append(novo_pokemon)

    except Exception:
        pass

    # Redireciona o navegador de volta para a rota raiz ('/')
    return redirect('/')


# Executa o servidor local
if __name__ == '__main__':
    app.run(debug=True)