import unicodedata

def avaliacao_texto(texto: str) -> str:
    texto = texto.lower()
    texto = unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('ASCII')
    return texto

def padronizar_tipo_depoimento(tipo_depoimento: str) -> str:
    tipo_depoimento_normalizado = avaliacao_texto(tipo_depoimento)
    if tipo_depoimento_normalizado == 'transito':
        return 'Trânsito'
    if tipo_depoimento_normalizado == 'restaurante':
        return 'Restaurante'
    if tipo_depoimento_normalizado == 'lazer':
        return 'Lazer'
    if tipo_depoimento_normalizado == 'tempo':
        return 'Tempo'
    return tipo_depoimento