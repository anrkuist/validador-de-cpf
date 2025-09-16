import re
import azure.functions as func
import logging
import json
import requests

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

def validar_digitos_cpf(cpf: str) -> tuple[bool, str]:

    # Remove qualquer caractere que não seja número
    cpf = re.sub(r'[^0-9]', '', cpf)

    # Confere se o CPF tem 11 dígitos e não é uma sequência de números iguais
    if len(cpf) != 11 or len(set(cpf)) == 1:
        return False, cpf
    
    # Calcula o primeiro dígito
    soma = 0
    for i in range(9):
        soma += int(cpf[i]) * (10 - i)
    digito1 = (soma * 10) % 11
    if digito1 == 10:
        digito1 = 0
    
    # Calcula o segundo dígito
    soma = 0
    for i in range(10):
        soma += int(cpf[i]) * (11 - i)
    digito2 = (soma * 10) % 11
    if digito2 == 10:
        digito2 = 0
    
    # Retorna se é válido + a versão limpa do CPF
    return cpf[-2:] == f"{digito1}{digito2}", cpf

@app.route(route="validarcpf")
def validar_cpf(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request for CPF validation.')

    cpf = req.params.get('cpf')
    if not cpf:
        try:
            req_body = req.get_json()
        except ValueError:
            return func.HttpResponse("Invalid JSON body.", status_code=400)
        else:
            cpf = req_body.get('cpf')

    if cpf:
        # Remove qualquer caractere que não seja número
        valido, cpf_limpo = validar_digitos_cpf(cpf)

        # Chama a função para validar os dígitos do CPF
        if not valido:
            return func.HttpResponse(
                json.dumps({"cpf": cpf, "valido": False, "error": "CPF invalido (digitos nao conferem)"}),
                status_code=400,
                mimetype="application/json"
            )
        
        url = f"https://scpa-backend.saude.gov.br/public/scpa-usuario/validacao-cpf/{cpf_limpo}"
        
        try:
            response = requests.get(url, timeout=10)

            if response.status_code == 200:
                # CPF válido
                return func.HttpResponse(
                    json.dumps({"cpf": cpf, "valido": True, "mensagem": "CPF encontrado na Receita Federal"}),
                    mimetype="application/json"
                )
            else:
                # CPF não encontrado
                return func.HttpResponse(
                    json.dumps({"cpf": cpf, "valido": False, "error": "CPF nao encontrado na Receita Federal"}),
                    status_code=400,
                    mimetype="application/json"
                )
            
        except Exception as e:
            return func.HttpResponse(
                json.dumps({"error": f"Erro na consulta: {str(e)}"}),
                status_code=500,
                mimetype="application/json"
            )
    else:
        return func.HttpResponse(
             "Passe um CPF na query string (?cpf=123456789) ou no corpo da requisição.",
             status_code=400
        )