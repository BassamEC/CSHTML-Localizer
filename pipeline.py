import os
import json
from datetime import datetime
from extractor import CSHTMLExtractor
from translator import Translator
from resx_writer import ResxWriter
from replacer import TextReplacer

class CSHTMLLocalizationPipeline:
    def __init__(self):
        self.extractor = CSHTMLExtractor()
        self.translator = Translator()
        self.resx_writer = ResxWriter()
        self.replacer = TextReplacer()

    def process_cshtml_files(self, input_dir: str, output_dir: str = "LocalizedOutput"):
        if not os.path.exists(input_dir):
            return {"error": f"Input directory {input_dir} does not exist"}

        cshtml_files = [
            os.path.join(root, f)
            for root, _, files in os.walk(input_dir)
            for f in files if f.lower().endswith(".cshtml")
        ]
        if not cshtml_files:
            return {"error": "No CSHTML files found"}

        os.makedirs(output_dir, exist_ok=True)
        resources_dir = os.path.join(output_dir, "Resources", "Views")
        modified_views_dir = os.path.join(output_dir, "Views")
        os.makedirs(resources_dir, exist_ok=True)
        os.makedirs(modified_views_dir, exist_ok=True)

        all_english_resources = {}
        all_arabic_resources = {}
        results = []

        for file_path in cshtml_files:
            filename = os.path.basename(file_path)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            extracted = self.extractor.extract_and_generate_keys(content, filename)
            items = extracted.get('extracted_items', [])
            if not items:
                continue

            english_resources = {i['key']: i['original_text'] for i in items}
            arabic_resources = self.translator.translate(english_resources)

            view_name = os.path.splitext(filename)[0]
            self.resx_writer.create_resx_file(english_resources, os.path.join(resources_dir, f"{view_name}.en-US.resx"))
            self.resx_writer.create_resx_file(arabic_resources, os.path.join(resources_dir, f"{view_name}.ar-SA.resx"))

            modified_content = self.replacer.replace_text_with_resources(content, items)
            if "@inject IViewLocalizer Localizer" not in modified_content:
                modified_content = "@inject IViewLocalizer Localizer\n" + modified_content

            with open(os.path.join(modified_views_dir, filename), 'w', encoding='utf-8') as f:
                f.write(modified_content)

            all_english_resources.update(english_resources)
            all_arabic_resources.update(arabic_resources)

            results.append({"filename": filename, "resource_count": len(items)})

        if all_english_resources:
            self.resx_writer.create_resx_file(all_english_resources, os.path.join(output_dir, "Resources", "Global.en-US.resx"))
            self.resx_writer.create_resx_file(all_arabic_resources, os.path.join(output_dir, "Resources", "Global.ar-SA.resx"))

        summary = {
            "pipeline_complete": True,
            "files_processed": len(cshtml_files),
            "successful_conversions": len(results),
            "total_resource_strings": len(all_english_resources),
            "generated": datetime.now().isoformat()
        }
        with open(os.path.join(output_dir, "localization_summary.json"), 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        return summary
