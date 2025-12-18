from pypdf import PdfReader

reader = PdfReader("./PDFs/renamed_pdf.pdf")
fields = reader.get_fields()

print("First 10 renamed fields:")
for i, (field_name, field) in enumerate(fields.items()):
    if i >= 10:
        break
    print(f"  {field_name}")
