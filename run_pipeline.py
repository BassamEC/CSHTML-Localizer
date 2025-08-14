from pipeline import CSHTMLLocalizationPipeline

if __name__ == "__main__":
    pipeline = CSHTMLLocalizationPipeline()
    
    input_folder = "Views"          # Path to your original Views folder
    output_folder = "LocalizedOutput"  # Output folder for processed files

    print("Starting CSHTML localization pipeline...")
    summary = pipeline.process_cshtml_files(input_folder, output_folder)

    if summary.get("pipeline_complete"):
        print("✅ Localization pipeline complete!")
        print(f"📁 Output folder: {output_folder}")
        print(f"📄 Files processed: {summary['files_processed']}")
        print(f"✨ Total resource strings: {summary['total_resource_strings']}")
    else:
        print("❌ Pipeline error:", summary.get("error"))
