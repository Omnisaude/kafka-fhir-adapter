

def is_mensagem_valida(mensagem: dict) -> bool:

    if not mensagem.get('address').get('state') in ['CA']:
        return False

    return True