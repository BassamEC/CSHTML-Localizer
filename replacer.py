class TextReplacer:
    def replace_text_with_resources(self, cshtml_content: str, extracted_items: list):
        modified_content = cshtml_content
        sorted_items = sorted(extracted_items, key=lambda x: x.get('line_number', 0), reverse=True)
        for item in sorted_items:
            original_text = item['original_text']
            resource_key = item['key']
            replacements = [
                (f'>{original_text}<', f'>@Localizer["{resource_key}"]<'),
                (f'"{original_text}"', f'"@Localizer["{resource_key}"]"'),
                (f"'{original_text}'", f"'@Localizer[\"{resource_key}\"]'"),
                (f'placeholder="{original_text}"', f'placeholder="@Localizer["{resource_key}"]"'),
                (f'value="{original_text}"', f'value="@Localizer["{resource_key}"]"'),
                (f'title="{original_text}"', f'title="@Localizer["{resource_key}"]"'),
                (f'alt="{original_text}"', f'alt="@Localizer["{resource_key}"]"')
            ]
            for old, new in replacements:
                if old in modified_content:
                    modified_content = modified_content.replace(old, new)
                    break
        return modified_content
