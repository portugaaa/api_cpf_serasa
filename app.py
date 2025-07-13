from flask import Flask, request, Response
import re

app = Flask(__name__)

API_KEY = "zunkyzz"
DATA_FILE = "dados.txt"

def buscar_cpf(cpf_procurado):
    """Busca um CPF no arquivo e retorna o bloco formatado"""
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as file:
            conteudo = file.read()
            
            # Procura o bloco do CPF usando regex
            padrao = re.compile(
                r'RESULTADO\s*\n'  # Ignora "RESULTADO" original
                r'NOME:\s*(.*?)\s*\n'
                r'CPF:\s*' + re.escape(cpf_procurado) + r'\s*\n'
                r'NASCIMENTO:\s*(.*?)\s*\n'
                r'SEXO:\s*(.*?)\s*\n',
                re.DOTALL
            )
            
            resultado = padrao.search(conteudo)
            if resultado:
                nome = resultado.group(1).strip()
                nascimento = resultado.group(2).strip()
                sexo = resultado.group(3).strip()
                
                # Monta a resposta no novo formato
                resposta = (
                    f"🔍 Dados Encontrados\n\n"
                    f"NOME: {nome}\n"
                    f"CPF: {cpf_procurado}\n"
                    f"NASCIMENTO: {nascimento}\n"
                    f"SEXO: {sexo}\n"
                )
                return resposta
            return None
            
    except FileNotFoundError:
        return "arquivo_nao_encontrado"

@app.route('/consultar', methods=['GET'])
def consultar():
    # Verifica API Key
    if request.args.get('apikey') != API_KEY:
        return Response("ERRO: API Key inválida", status=401, mimetype='text/plain')
    
    # Pega e valida o CPF
    cpf = request.args.get('cpf', '').strip()
    if not cpf.isdigit() or len(cpf) != 11:
        return Response("ERRO: CPF inválido (deve ter 11 dígitos)", status=400, mimetype='text/plain')
    
    # Consulta o CPF
    resultado = buscar_cpf(cpf)
    
    if resultado == "arquivo_nao_encontrado":
        return Response("ERRO: Arquivo de dados não encontrado", status=500, mimetype='text/plain')
    elif resultado:
        return Response(resultado, mimetype='text/plain')
    else:
        return Response("🔍 Dados Encontrados\n\nCPF não registrado", mimetype='text/plain')

if __name__ == '__main__':
    app.run(debug=True)
