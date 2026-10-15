import os
import json
import zipfile

print("Restoring clean original layout in excel loaded.pbix...")

pbix_path = "Supply_Chain_Inventory_Analytics/powerbi/excel loaded.pbix"

if not os.path.exists(pbix_path):
    print(f"Error: {pbix_path} not found.")
    exit(1)

with zipfile.ZipFile(pbix_path, 'r') as z_in:
    files_map = {name: z_in.read(name) for name in z_in.namelist()}

# Restore original clean single-section layout
original_layout = {
    "id": 0,
    "resourcePackages": [
        {
            "resourcePackage": {
                "name": "SharedResources",
                "type": 2,
                "items": [
                    {
                        "type": 202,
                        "path": "BaseThemes/Fluent2-CY26SU08.json",
                        "name": "Fluent2-CY26SU08"
                    }
                ],
                "disabled": False
            }
        }
    ],
    "sections": [
        {
            "id": 0,
            "name": "7b77d56d33c640533dd4",
            "displayName": "Page 1",
            "filters": "[]",
            "ordinal": 0,
            "visualContainers": []
        }
    ],
    "config": json.dumps({"version": "5.54", "themeCollection": {"baseTheme": {"name": "Fluent2-CY26SU08", "version": "5.54", "type": 2}}, "activeSectionName": "7b77d56d33c640533dd4"})
}

with zipfile.ZipFile(pbix_path, 'w', zipfile.ZIP_DEFLATED) as z_out:
    for name, content in files_map.items():
        if name == 'Report/Layout':
            z_out.writestr(name, json.dumps(original_layout, indent=2).encode('utf-16le'))
        else:
            z_out.writestr(name, content)

print("Successfully restored excel loaded.pbix to clean native state!")
