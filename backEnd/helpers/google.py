from googletrans import Translator

def traduzir(texto):
        translator = Translator()
        traducao = translator.translate(texto, src='en', dest='pt')
        return traducao.text