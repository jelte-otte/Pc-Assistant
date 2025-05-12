import os
import vobject
import json

def convert_vcf_to_json(vcf_filename='contacten.vcf', json_filename='contacts.json'):
    """
    Converteert een .vcf-bestand naar een contacts.json in de 'contacts/' map.
    Neemt alleen de eerste telefoonnummer per contact mee.
    """
    base_path = 'contacts'
    vcf_path = os.path.join(base_path, vcf_filename)
    json_path = os.path.join(base_path, json_filename)

    if not os.path.exists(vcf_path):
        print(f"VCF-bestand '{vcf_path}' niet gevonden.")
        return

    contacts_list = []

    with open(vcf_path, 'r', encoding='utf-8') as file:
        for vcard in vobject.readComponents(file):
            contact = {}
            if hasattr(vcard, 'fn'):
                contact['name'] = vcard.fn.value
            if hasattr(vcard, 'tel'):
                tel = vcard.contents.get('tel', [])[0].value  # eerste nummer
                contact['phone'] = tel
            if contact.get('name') and contact.get('phone'):
                contacts_list.append(contact)

    with open(json_path, 'w', encoding='utf-8') as json_file:
        json.dump(contacts_list, json_file, indent=4, ensure_ascii=False)

    print(f"{len(contacts_list)} contacten opgeslagen in '{json_path}'")
