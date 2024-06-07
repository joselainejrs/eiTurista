import unicodedata

def avaliacao_texto(texto: str) -> str:
    texto = texto.lower()
    texto = unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('ASCII')
    return texto

def padronizar_tipo_depoimento(tipo_depoimento: str) -> str:
    tipoDepoimento_normalizado = avaliacao_texto(tipo_depoimento)
    if tipoDepoimento_normalizado == 'transito':
        return 'Trânsito'
    if tipoDepoimento_normalizado == 'restaurante':
        return 'Restaurante'
    if tipoDepoimento_normalizado == 'lazer':
        return 'Lazer'
    if tipoDepoimento_normalizado == 'tempo':
        return 'Tempo'
    return tipo_depoimento