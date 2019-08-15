from django.template.response import TemplateResponse


class TemplateResponseNotFound(TemplateResponse):
    status_code = 404