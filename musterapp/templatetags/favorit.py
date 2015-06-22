from django import template

register = template.Library()

@register.inclusion_tag('musterapp/fav_button.html', takes_context=True)
def fav_button(context, target_id):
    favorites = context["favorites"]
    faved = target_id in favorites and favorites[target_id]
    return {
        'id': target_id,
        'faved': faved
    }