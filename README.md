# CSHTML-Localizer

# CSHTML-Translator

An automated pipeline to extract translatable text from CSHTML (Razor) view files, generate English + Arabic resource files (.resx), and replace static text in views with localization keys.

Designed to be easy to run and easy to swap out the LLM components if you want to use your own extractor/translator.

## Features

- ✅ Extracts static UI text (titles, headings, buttons, placeholders, alt text, aria-labels, mixed Razor static parts, etc.)
- ✅ Generates .resx files per view and a global .resx
- ✅ Replaces strings in views with `@Localizer["ResourceKey"]`
- ✅ Produces a language selector partial and controller snippet for culture switching
- ✅ Summarizes work in `localization_summary.json`
- ✅ Easy to replace the extractor/translator with your own tools

## Quick Start

### 1. Prerequisites

- Python 3.9+
- OpenAI API key (optional - see Custom extractor/translator section)

Install Python dependencies:

```powershell
pip install openai python-dotenv
```

Create `.env` file in project root:

```ini
OPENAI_API_KEY=sk-...
```

> **Note:** If you don't want to use the LLM, you can skip the API key and use your own translator/extractor (see [Custom extractor/translator](#custom-extractortranslator) section).

### 2. Project Layout

Place these files in your project root (or adapt relative paths in `run_pipeline.py`):

```
project_root/
├── run_pipeline.py
├── pipeline.py
├── extractor.py
├── translator.py
├── prompts.py
├── resx_writer.py
├── replacer.py
├── views/             ← put your .cshtml files here (input)
└── output/            ← pipeline writes here (LocalizedOutput by default)
```

Create `views/` directory and add your `.cshtml` files there. **Back up your originals if needed.**

### 3. Run the Pipeline

```
python run_pipeline.py
```

## What the Pipeline Does

1. 📁 Reads `views/*.cshtml`
2. 🔍 Calls extractor → gets extraction JSON
3. 🌐 Calls translator → gets translation JSON
4. 📄 Writes `.resx` files to `output/Resources/Views/` and `output/Resources/Global.*.resx`
5. 📝 Writes modified views to `output/Views/`
6. 🎛️ Creates `output/Controllers/HomeController.cs` and `output/Startup_Localization_Config.cs`
7. 📊 Writes `output/localization_summary.json`


## Output Files

The pipeline generates:

- `output/Resources/Views/<ViewName>.en-US.resx` (per-view English)
- `output/Resources/Views/<ViewName>.ar-SA.resx` (per-view Arabic)  
- `output/Resources/Global.en-US.resx` and `output/Resources/Global.ar-SA.resx`
- `output/Views/<ViewName>.cshtml` (modified views)
- `output/Views/Shared/_LanguageSelector.cshtml`
- `output/Controllers/HomeController.cs`
- `output/Startup_Localization_Config.cs`
- `output/localization_summary.json`

## Data Flow

```
views/View.cshtml
      ↓ (read)
Extractor (.py) —→ produces extraction JSON
      ↓ (mapping if needed)
Translator (.py) —→ produces translation JSON  
      ↓
Resx writer (.py) —→ writes .resx files
Replacer (.py) —→ writes modified .cshtml
```

## Required JSON Formats

⚠️ **Do not change these formats unless you update the pipeline code**

### 1. Extraction JSON (extractor output)

```json
{
  "file": "Home.cshtml",
  "strings": [
    { "key": "Home_Title", "value": "Welcome to our site" },
    { "key": "Home_Intro", "value": "We provide excellent service." }
  ]
}
```

Alternative format (older pipeline):
```json
{
  "extracted_items": [
    { 
      "key": "Home.Heading.Welcome", 
      "original_text": "Welcome to our website", 
      "line_number": 10, 
      "context": "hero" 
    }
  ]
}
```

### 2. Translation JSON (per language)

```json
{
  "file": "Home.cshtml",
  "translations": [
    { "key": "Home_Title", "value": "مرحبًا بك في موقعنا" },
    { "key": "Home_Intro", "value": "نحن نقدم خدمة ممتازة." }
  ]
}
```

### 3. RESX Output Example

```xml
<data name="Home_Title" xml:space="preserve">
  <value>مرحبًا بك في موقعنا</value>
</data>
```

## Custom Extractor/Translator

To replace LLM extraction/translation:

1. **Write extractor script** that reads `views/<file>.cshtml` and outputs extraction JSON
2. **Write translator script** that reads extraction JSON and outputs translation JSON per language
3. **Update pipeline** to use your scripts instead of the default LLM-based ones
4. **Ensure JSON formats match** the required formats above

## LLM Verification & Manual Review

⚠️ **LLM-based extraction & translation are fast but not perfect**

### Common Issues:
- Missed strings (especially inside conditionals or complex Razor)
- Partial extractions for mixed content  
- Translation nuance or context errors

### Always Review:
1. Open `output/localization_summary.json` to see processed files & counts
2. Inspect `<ViewName>.en-US.resx` and `<ViewName>.ar-SA.resx`
3. Open modified views in `output/Views/` and run your app locally
4. Check for layout or RTL issues
5. Manually edit `.resx` files as needed (they are plain XML)

## Integrating into Your .NET Project

1. Copy `output/Resources/` to your project root
2. Merge the `HomeController.cs` method into your controllers
3. Add localization configuration from `Startup_Localization_Config.cs` to your `Startup.cs`
4. Add `@await Html.PartialAsync("_LanguageSelector")` to your `_Layout.cshtml`
5. Install required NuGet packages:
   - `Microsoft.AspNetCore.Mvc.Localization`
   - `Microsoft.Extensions.Localization`

## Configuration

Edit `prompts.py` to customize LLM prompts. Keep the `{content}` placeholder in the extraction prompt unless you also update `extractor.py`.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError` / relative import errors | Run from package parent or use absolute imports |
| `openai.OpenAIError: api_key client option must be set` | Set `OPENAI_API_KEY` in `.env` |
| `KeyError: 'cshtml_content'` | Ensure your prompt uses `{content}` placeholder |

## License

This project is licensed under the GNU General Public License v3.0 (GPL-3.0).

This means:
- ✅ You can use, modify, and distribute this software
- ✅ Source code must be made available when distributing
- ✅ Any derivative works must also be licensed under GPL-3.0
- ✅ Commercial use is allowed, but with the above restrictions

See the [LICENSE](LICENSE) file for full details.

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch  
5. Create a Pull Request
