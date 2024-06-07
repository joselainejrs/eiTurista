from controllers.localidade import localidade_route
from controllers.depoimento import depoimento_route

# Lista de todos os blueprints para facilitar a importação
all_blueprints = [
    localidade_route,
    depoimento_route,
]