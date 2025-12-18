import re
from pypdf import PdfReader, PdfWriter
from pypdf.generic import TextStringObject, ArrayObject, NameObject

INPUT_PDF = "./PDFs/input_pdf.pdf"
OUTPUT_PDF = "./PDFs/renamed_pdf.pdf"


def normalize(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '_', text)
    text = re.sub(r'\s+', '_', text).strip('_')
    return text[:30]


# --- Read PDF ---
reader = PdfReader(INPUT_PDF)
writer = PdfWriter()
writer.clone_document_from_reader(reader)

fields = reader.get_fields()
mapping = {}

# --- Build mapping old_name -> new_name ---
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


# --- Rename fields and flatten hierarchy ---
# Update field names in AcroForm  
if "/AcroForm" in writer._root_object:
    acroform = writer._root_object["/AcroForm"]
    if "/Fields" in acroform:
        # Collect all leaf fields (actual form widgets) with their new names
        new_fields = []
        
        def collect_leaf_fields(field_obj, parent_name):
            """Recursively collect leaf fields and rename them"""
            field = field_obj.get_object()
            
            # Get current local field name
            local_name = field.get("/T")
            if not local_name:
                return
            
            # Build the full qualified name
            if parent_name:
                full_name = f"{parent_name}.{local_name}"
            else:
                full_name = local_name
            
            # Check if this is a leaf field (has no /Kids or is an actual widget)
            has_kids = "/Kids" in field
            
            if not has_kids:
                # This is a leaf field - rename it and remove parent reference
                if full_name in mapping:
                    new_name = mapping[full_name]
                    field.update({"/T": TextStringObject(new_name)})
                    
                # Remove parent reference to flatten the structure
                if "/Parent" in field:
                    del field["/Parent"]
                
                new_fields.append(field_obj)
            else:
                # This is a container - recurse into children
                if "/Kids" in field:
                    for kid in field["/Kids"]:
                        collect_leaf_fields(kid, full_name)
        
        # Collect all leaf fields
        for field in acroform["/Fields"]:
            collect_leaf_fields(field, "")
        
        # Replace the fields array with only the flattened leaf fields
        acroform[NameObject("/Fields")] = ArrayObject(new_fields)


# --- Write output ---
with open(OUTPUT_PDF, "wb") as f:
    writer.write(f)


# --- Print mapping for reference ---
print("\nRenamed fields:")
for old, new in mapping.items():
    print(f'"{old}": "{new}"')
