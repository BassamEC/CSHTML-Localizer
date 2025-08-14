# prompts.py

EXTRACTION_PROMPT = """
You are an expert in web development and internationalization. Extract ALL translatable static text content from the given HTML/CSHTML file and generate appropriate resource keys.

EXTRACT:
1. Text inside HTML tags (h1, h2, p, span, div, button, label, etc.)
2. Title tag content
3. Input placeholder text
4. Image alt text
5. Button/input value attributes
6. Static parts of mixed Razor/HTML content
7. Data attribute text values
8. Aria-label text

IGNORE:
- Pure Razor expressions like @ViewBag.Title, @Model.Name
- JavaScript code and variables
- CSS classes, IDs, and styling
- URLs and file paths
- Pure numbers without context
- HTML tag names and attributes (except content)

SPECIAL HANDLING:
- For mixed content like "Welcome @Model.Name!", extract only "Welcome " and "!"
- Preserve context by noting what the dynamic part represents

GENERATE resource keys in format: FileName.ElementType.Description
Example: "Home.Button.Submit", "Contact.Label.Email", "Login.Error.InvalidCredentials"

Return JSON:
{{
    "extracted_items": [
        {{
            "key": "Home.Heading.Welcome",
            "original_text": "Welcome to our website",
            "line_number": 10,
            "context": "Main heading in hero section"
        }}
    ]
}}

CSHTML FILE ({content})
"""

TRANSLATION_PROMPT = """
Translate these English web UI texts to Arabic. Keep the same keys.
Use Modern Standard Arabic suitable for web interfaces.
Consider RTL layout and web conventions.

English texts:
{texts}

Return JSON with same keys:
{{
    "key1": "Arabic translation",
    "key2": "Arabic translation"
}}
"""
