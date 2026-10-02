from django import template
from django.utils.safestring import mark_safe
from django.templatetags.static import static

register = template.Library()

@register.simple_tag
def render_ducky_avatar(avatar_data, size="54px", extra_class=""):
    """
    Renderiza el avatar de pato compuesto con sus 4 capas modulares transparentes.
    avatar_data puede ser un dict con keys: body, clothes, head, face
    o una instancia de GamePlayer.
    """
    if hasattr(avatar_data, 'avatar_dict'):
        data = avatar_data.avatar_dict
    elif isinstance(avatar_data, dict):
        data = avatar_data
    else:
        data = {}

    body = data.get('body') or 'body_yellow'
    clothes = data.get('clothes') or ''
    face = data.get('face') or 'face_calm'
    head = data.get('head') or ''

    body_url = static(f"quiz_games/avatars/bodies/{body}.svg")
    clothes_url = static(f"quiz_games/avatars/clothes/{clothes}.svg") if clothes else ""
    face_url = static(f"quiz_games/avatars/faces/{face}.svg") if face else ""
    head_url = static(f"quiz_games/avatars/heads/{head}.svg") if head else ""

    html = [
        f'<div class="ducky-composite-avatar {extra_class}" style="width:{size}; height:{size}; position:relative; display:inline-block; flex-shrink:0;">',
        f'  <img src="{body_url}" alt="Cuerpo" class="ducky-layer ducky-layer-body" style="position:absolute; top:0; left:0; width:100%; height:100%; z-index:10; object-fit:contain; pointer-events:none;">'
    ]

    if clothes_url:
        html.append(f'  <img src="{clothes_url}" alt="Ropa" class="ducky-layer ducky-layer-clothes" style="position:absolute; top:0; left:0; width:100%; height:100%; z-index:20; object-fit:contain; pointer-events:none;">')

    if face_url:
        html.append(f'  <img src="{face_url}" alt="Cara" class="ducky-layer ducky-layer-face" style="position:absolute; top:0; left:0; width:100%; height:100%; z-index:30; object-fit:contain; pointer-events:none;">')

    if head_url:
        html.append(f'  <img src="{head_url}" alt="Sombrero" class="ducky-layer ducky-layer-head" style="position:absolute; top:0; left:0; width:100%; height:100%; z-index:40; object-fit:contain; pointer-events:none;">')

    html.append('</div>')
    return mark_safe("\n".join(html))
