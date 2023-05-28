from typing import Optional
from django.shortcuts import HttpResponse
from django.template.loader import get_template

from io import BytesIO
from xhmtl2pdf import pisa


def render_to_pdf(template, context: Optional[dict]):
    template = get_template(template)
    html = template.render(context)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None
