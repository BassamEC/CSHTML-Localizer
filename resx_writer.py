import os
import xml.etree.ElementTree as ET
from xml.dom import minidom

class ResxWriter:
    def create_resx_file(self, translations: dict, filepath: str):
        root = ET.Element("root")
        headers = {
            "resmimetype": "text/microsoft-resx",
            "version": "2.0",
            "reader": "System.Resources.ResXResourceReader, System.Windows.Forms, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089",
            "writer": "System.Resources.ResXResourceWriter, System.Windows.Forms, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089"
        }
        for name, value in headers.items():
            resheader = ET.SubElement(root, "resheader", name=name)
            ET.SubElement(resheader, "value").text = value
        for key, text in sorted(translations.items()):
            data = ET.SubElement(root, "data", name=key)
            data.set("xml:space", "preserve")
            ET.SubElement(data, "value").text = text
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        rough_string = ET.tostring(root, encoding='unicode')
        reparsed = minidom.parseString(rough_string)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('<?xml version="1.0" encoding="utf-8"?>\n' + reparsed.toprettyxml(indent="  ")[23:])
