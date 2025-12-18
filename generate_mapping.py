import re
from pypdf import PdfReader, PdfWriter

def normalize(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '_', text)
    text = re.sub(r'\s+', '_', text).strip('_')
    return text[:30]

reader = PdfReader("./PDFs/input_pdf.pdf")
fields = reader.get_fields()

mapping = {}

for old_field_name, field in fields.items():
    tooltip = field.get("/TU")
    alternate = field.get("/Alt")

    source = tooltip or alternate or old_field_name
    normalized_name = normalize(source)

    i = 1
    base = normalized_name
    while normalized_name in mapping.values():
        i += 1
        normalized_name = f"{base}_{i}"

    mapping[old_field_name] = normalized_name

for k, v in mapping.items():
    print(f'"{k}": "{v}",')