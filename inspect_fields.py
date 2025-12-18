from pypdf import PdfReader

reader = PdfReader("./PDFs/input_pdf.pdf")
fields = reader.get_fields()

for field_name, field in fields.items():
    print(f"Field Name: {field_name}")
    print("  Type:", field.get("/FT"))
    # print("  Tooltip:", field.get("/TU"))
    # print("  Alternate:", field.get("/Alt"))
    # print("  Partial:", field.get("/T"))
    print("-" * 40)