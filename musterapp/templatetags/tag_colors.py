from django import template
from django.core.urlresolvers import reverse
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from musterapp import views

register = template.Library()


_colormap = {
    'aliceblue': '#f0f8ff', 'eisfarben': '#f0f8ff',
    'antiquewhite': '#faebd7', 'antikweiß': '#faebd7',
    'aqua': '#00ffff', 'wasser': '#00ffff',
    'aquamarine': '#7fffd4', 'aquamarinblau': '#7fffd4',
    'azure': '#f0ffff', 'himmelblau': '#f0ffff',
    'beige': '#f5f5dc',
    'bisque': '#ffe4c4', 'biskuit': '#ffe4c4',
    'black': '#000000', 'schwarz': '#000000',
    'blanchedalmond': '#ffebcd', 'mandelweiß': '#ffebcd',
    'blue': '#0000ff', 'blau': '#0000ff',
    'blueviolet': '#8a2be2', 'blauviolett': '#8a2be2',
    'brown': '#a52a2a', 'braun': '#a52a2a',
    'burlywood': '#deb887', 'gelbbraun': '#deb887',
    'cadetblue': '#5f9ea0', 'kadettenblau': '#5f9ea0',
    'chartreuse': '#7fff00', 'hellgrün': '#7fff00',
    'chocolate': '#d2691e', 'schokolade': '#d2691e',
    'coral': '#ff7f50', 'koralle': '#ff7f50',
    'cornflowerblue': '#6495ed', 'kornblumenblau': '#6495ed',
    'cornsilk': '#fff8dc', 'mais': '#fff8dc',
    'crimson': '#dc143c', 'karmesinrot': '#dc143c',
    'cyan': '#00ffff', 'türkis (cyan = aqua)': '#00ffff',
    'darkblue': '#00008b', 'dunkelblau': '#00008b',
    'darkcyan': '#008b8b', 'dunkeltürkis': '#008b8b',
    'darkgoldenrod': '#b8860b', 'dunkle goldrutenfarbe': '#b8860b',
    'darkgreen': '#006400', 'dunkelgrün': '#006400',
    'darkgrey': '#a9a9a9', 'dunkelgrau': '#a9a9a9',
    'darkkhaki': '#bdb76b', 'dunkelkhaki': '#bdb76b',
    'darkmagenta': '#8b008b', 'dunkelmagenta': '#8b008b',
    'darkolivegreen': '#556b2f', 'dunkles olivgrün': '#556b2f',
    'darkorange': '#ff8c00', 'dunkles orange': '#ff8c00',
    'darkorchid': '#9932cc', 'dubkle orchidee': '#9932cc',
    'darkred': '#8b0000', 'dunkelrot': '#8b0000',
    'darksalmon': '#e9967a', 'dunkle lachsfarbe': '#e9967a',
    'darkseagreen': '#8fbc8f', 'dunkles seegrün': '#8fbc8f',
    'darkslateblue': '#483d8b', 'dunkles schieferblau': '#483d8b',
    'darkslategrey': '#2f4f4f', 'dunkles schiefergrau': '#2f4f4f',
    'darkturquoise': '#00ced1', 'dunkeltürkis': '#00ced1',
    'darkviolet': '#9400d3', 'dunkelvilolett': '#9400d3',
    'deeppink': '#ff1493', 'tiefrosa': '#ff1493',
    'deepskyblue': '#00bfff', 'tiefes himmelblau': '#00bfff',
    'dimgrey': '#696969', 'dunkelgrau': '#696969',
    'dodgerblue': '#1e90ff', 'persenningblau': '#1e90ff',
    'firebrick': '#b22222', 'backstein': '#b22222',
    'floralwhite': '#fffaf0', 'blütenweiß': '#fffaf0',
    'forestgreen': '#228b22', 'waldgrün': '#228b22',
    'fuchsia': '#ff00ff', 'fuchsie (fuchsia = magenta)': '#ff00ff',
    'gainsboro': '#dcdcdc',
    'ghostwhite': '#f8f8ff', 'geisterweiß': '#f8f8ff',
    'gold': '#ffd700',
    'goldenrod': '#daa520', 'goldrute': '#daa520',
    'gray': '#808080', 'grey': '#808080', 'grau': '#808080',
    'green': '#008000', 'grün': '#008000',
    'greenyellow': '#adff2f', 'grüngelb': '#adff2f',
    'honeydew': '#f0fff0', 'honigmelone': '#f0fff0',
    'hotpink': '#ff69b4', 'leuchtendes rosa': '#ff69b4',
    'indianred': '#cd5c5c', 'indischrot': '#cd5c5c',
    'indigo': '#4b0082',
    'ivory': '#fffff0', 'elfenbein': '#fffff0',
    'khaki': '#f0e68c', 'staubfarben': '#f0e68c',
    'lavender': '#e6e6fa', 'lavendel': '#e6e6fa',
    'lavenderblush': '#fff0f5', 'lavendelrosa': '#fff0f5',
    'lawngreen': '#7cfc00', 'rasengrün': '#7cfc00',
    'lemonchiffon': '#fffacd', 'chiffongelb': '#fffacd',
    'lightblue': '#add8e6', 'hellblau': '#add8e6',
    'lightcoral': '#f08080', 'helles korallenrot': '#f08080',
    'lightcyan': '#e0ffff', 'helles cyan': '#e0ffff',
    'lightgoldenrodyellow': '#fafad2', 'helles goldrutengelb': '#fafad2',
    'lightgray': '#d3d3d3', 'hellgrau': '#d3d3d3',
    'lightgreen': '#90ee90', 'hellgrün': '#90ee90',
    'lightpink': '#ffb6c1', 'hellrosa': '#ffb6c1',
    'lightsalmon': '#ffa07a', 'helle lachsfarbe': '#ffa07a',
    'lightseagreen': '#20b2aa', 'helles seegrün': '#20b2aa',
    'lightskyblue': '#87cefa', 'helles himmelblau': '#87cefa',
    'lightslategrey': '#778899', 'helles schiefergrau': '#778899',
    'lightsteelblue': '#b0c4de', 'helles stahlblau': '#b0c4de',
    'lightyellow': '#ffffe0', 'hellgelb': '#ffffe0',
    'lime': '#00ff00', 'limone': '#00ff00',
    'limegreen': '#32cd32', 'limonengrün': '#32cd32',
    'linen': '#faf0e6', 'leinen': '#faf0e6',
    'magenta': '#ff00ff', 'magenta (magenta = fuchsia)': '#ff00ff',
    'maroon': '#800000', 'kastanie': '#800000',
    'mediumaquamarine': '#66cdaa', 'mittleres aquamarin': '#66cdaa',
    'mediumblue': '#0000cd', 'mittleres blau': '#0000cd',
    'mediumorchid': '#ba55d3', 'mittlere orchedee': '#ba55d3',
    'mediumpurple': '#9370db', 'mittleres violett': '#9370db',
    'mediumseagreen': '#3cb371', 'mittleres seegrün': '#3cb371',
    'mediumslateblue': '#7b68ee', 'mittleres schieferblau': '#7b68ee',
    'mediumspringgreen': '#00fa9a', 'mittleres frühlingsgrün': '#00fa9a',
    'mediumturquoise': '#48d1cc', 'mittlere türkis': '#48d1cc',
    'mediumvioletred': '#c71585', 'mittleres violettrot': '#c71585',
    'midnightblue': '#191970', 'mitternachtsblau': '#191970',
    'mintcream': '#f5fffa', 'cremige minze': '#f5fffa',
    'mistyrose': '#ffe4e1', 'altrosa': '#ffe4e1',
    'moccasin': '#ffe4b5', 'mokassin': '#ffe4b5',
    'navajowhite': '#ffdead', 'navajoweiß': '#ffdead',
    'navy': '#000080', 'marinenblau': '#000080',
    'oldlace': '#fdf5e6', 'alte spitze': '#fdf5e6',
    'olive': '#808000', 'olivgrün': '#808000',
    'olivedrab ': '#6b8e23', 'olivgraubraun': '#6b8e23',
    'orange': '#ffa500',
    'orangered': '#ff4500', 'orangerot': '#ff4500',
    'orchid': '#da70d6', 'orchidee': '#da70d6',
    'palegoldenrod': '#eee8aa', 'blasse goldrutenfarbe': '#eee8aa',
    'palegreen': '#98fb98', 'blassgrün': '#98fb98',
    'paleturquoise': '#afeeee', 'blasstürkis': '#afeeee',
    'palevioletred': '#db7093', 'blasses violettrot': '#db7093',
    'papayawhip': '#ffefd5', 'papayacreme': '#ffefd5',
    'peachpuff': '#ffdab9', 'pfirsich': '#ffdab9',
    'peru': '#cd853f',
    'pink': '#ffc0cb', 'rosa': '#ffc0cb',
    'plum': '#dda0dd', 'pflaume': '#dda0dd',
    'powderblue': '#b0e0e6', 'taubenblau': '#b0e0e6',
    'purple': '#800080', 'violett': '#800080',
    'red': '#ff0000', 'rot': '#ff0000',
    'rosybrown': '#bc8f8f', 'rosiges braun': '#bc8f8f',
    'royalblue': '#4169e1', 'königsblau': '#4169e1',
    'saddlebrown': '#8b4513', 'sattelbraun': '#8b4513',
    'salmon': '#fa8072', 'lachsfarben': '#fa8072',
    'sandybrown': '#f4a460', 'sandbraun': '#f4a460',
    'seagreen': '#2e8b57', 'seegrün': '#2e8b57',
    'seashell': '#fff5ee', 'muschel': '#fff5ee',
    'sienna': '#a0522d', 'siennaerde': '#a0522d',
    'silver': '#c0c0c0', 'silber': '#c0c0c0',
    'skyblue': '#87ceeb', 'himmelblau': '#87ceeb',
    'slateblue': '#6a5acd', 'schieferblau': '#6a5acd',
    'slategrey': '#708090', 'schiefergrau': '#708090',
    'snow': '#fffafa', 'schneeweiß': '#fffafa',
    'springgreen': '#00ff7f', 'frühlingsgrün': '#00ff7f',
    'steelblue': '#4682b4', 'stahlblau': '#4682b4',
    'tan': '#d2b48c', 'hautfarben': '#d2b48c',
    'teal': '#008080', 'krickentengrün': '#008080',
    'thistle': '#d8bfd8', 'distel': '#d8bfd8',
    'tomato': '#ff6347', 'tomate': '#ff6347',
    'turquoise': '#40e0d0', 'türkis': '#40e0d0',
    'violet': '#ee82ee', 'veilchen': '#ee82ee',
    'wheat': '#f5deb3', 'weizen': '#f5deb3',
    'white': '#ffffff', 'weiß': '#ffffff',
    'whitesmoke': '#f5f5f5', 'rauchfarben': '#f5f5f5',
    'yellow': '#ffff00', 'gelb': '#ffff00',
    'yellowgreen': '#9acd32', 'gelbgrün': '#9acd32',
}


@register.filter
def color(value):
    value = value.lower()
    if value in _colormap:
        return _colormap[value]

    h = hash(value) % (16 ** 6)
    return "#{:06x}".format(h)


@register.filter(is_safe=True, needs_autoescape=True)
def as_tag(value, autoescape=True):
    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x: x

    tag_color = color(value)
    html = '<span class="tag" style="background-color: {};">{}</span>'.format(
        esc(tag_color), esc(value.upper()))
    return mark_safe(html)

@register.filter(is_safe=True, needs_autoescape=True)
def as_taga(value, autoescape=True):
    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x: x

    url = "{}?q={}".format(reverse(views.search), value.lower())
    tag_color = color(value)
    html = '<a href="{}" class="tag" style="background-color: {};">{}</span>'.format(
        url, esc(tag_color), esc(value.upper()))
    return mark_safe(html)
