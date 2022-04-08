"""
{{ name }} © {{ year }} {{ author }}

{{ description }}
"""
STACK = {}
{% raw %}{% for card in stack %}
{{ card }}
STACK[card.name] = card
{% endfor %}
STACK[{{ start }}].show(){% endraw %}
