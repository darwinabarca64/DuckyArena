import secrets


def generate_unique_game_code():
    """
    Genera un código PIN de 6 dígitos numéricos asegurando unicidad absoluta
    en la tabla Game para evitar violaciones de clave única.
    """
    from .models import Game
    while True:
        code = f"{secrets.randbelow(1000000):06d}"
        if not Game.objects.filter(code=code).exists():
            return code
