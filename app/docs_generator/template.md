# {{ spec.title }}

{{ spec.description }}

### Required Fields

{% for field in spec.required %}
- {{ field }}
{% endfor %}

### Parameters:

| Name | Type | Required | Description |
|-----|------|----------|-------------|
{% for param, details in spec.properties.items() -%}
| {{ param }} | {{ details.type }} | {{ 'Yes' if param in spec.required else 'No' }} | {{ details.description | default('N/A') }} {% if details.examples %}</br></br> Examples :</br> <pre>{{  details.examples | to_yaml  }}</pre> {% endif %} |
{% endfor %}
