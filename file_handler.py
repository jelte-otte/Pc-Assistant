from PySide6.QtWidgets import QFileDialog, QMessageBox
import os
import shutil
import vobject
import json

def upload_file(parent):
    """
    Open een QFileDialog om een VCF-bestand te selecteren, wijzig de naam naar 'contacts.vcf',
    maak een 'contacts'-map aan indien nodig, sla het bestand op in die map, converteer
    het naar 'contacts.json', en verwijder 'contacts.vcf'.
    Args:
        parent: Het ouder-widget voor de QFileDialog.
    Returns:
        str: Het pad naar het opgeslagen JSON-bestand, of None als er niets is geselecteerd.
    """
    file_dialog = QFileDialog(parent)
    file_dialog.setNameFilter("VCF bestanden (*.vcf);;Alle bestanden (*.*)")
    file_dialog.setFileMode(QFileDialog.ExistingFile)
    
    if file_dialog.exec():
        selected_files = file_dialog.selectedFiles()
        file_path = selected_files[0]
        saved_path = process_uploaded_file(file_path, parent)
        if saved_path:
            return saved_path
        else:
            QMessageBox.critical(parent, "Fout", "Fout bij het verwerken van het bestand.")
    return None

def process_uploaded_file(file_path, parent):
    """
    Wijzig de naam van het geüploade VCF-bestand naar 'contacts.vcf', maak een 'contacts'-map
    aan indien nodig, verplaats het bestand naar die map, converteer het naar 'contacts.json',
    en verwijder 'contacts.vcf'.
    Args:
        file_path (str): Het pad naar het geüploade bestand.
        parent: Het ouder-widget voor QMessageBox.
    Returns:
        str: Het pad naar het opgeslagen JSON-bestand, of None bij een fout.
    """
    try:
        # Maak de 'contacts'-map aan als die niet bestaat
        contacts_dir = os.path.join(os.path.dirname(__file__), "contacts")
        os.makedirs(contacts_dir, exist_ok=True)
        
        # Doelpad voor het VCF-bestand: contacts/contacts.vcf
        vcf_destination_path = os.path.join(contacts_dir, "contacts.vcf")
        
        # Kopieer het bestand naar de nieuwe locatie met de nieuwe naam
        shutil.copy2(file_path, vcf_destination_path)
        
        # Converteer het VCF-bestand naar JSON en ontvang het JSON-pad
        json_path = convert_vcf_to_json(parent=parent)
        
        # Verwijder contacts.vcf na succesvolle conversie
        if json_path and os.path.exists(vcf_destination_path):
            try:
                os.remove(vcf_destination_path)
                print(f"Bestand '{vcf_destination_path}' succesvol verwijderd.")
            except Exception as e:
                QMessageBox.warning(parent, "Waarschuwing", f"Kon 'contacts.vcf' niet verwijderen: {str(e)}")
        
        return json_path if json_path else None
    
    except Exception as e:
        QMessageBox.critical(parent, "Fout", f"Fout bij het verwerken van het bestand: {str(e)}")
        return None

def convert_vcf_to_json(vcf_filename='contacts.vcf', json_filename='contacts.json', parent=None):
    """
    Converteert een .vcf-bestand naar een contacts.json in de 'contacts/' map.
    Neemt alleen de eerste telefoonnummer per contact mee.
    Args:
        vcf_filename (str): Naam van het VCF-bestand.
        json_filename (str): Naam van het JSON-bestand.
        parent: Het ouder-widget voor QMessageBox (optioneel).
    Returns:
        str: Het pad naar het JSON-bestand, of None bij een fout.
    """
    base_path = 'contacts'
    vcf_path = os.path.join(base_path, vcf_filename)
    json_path = os.path.join(base_path, json_filename)

    if not os.path.exists(vcf_path):
        error_msg = f"VCF-bestand '{vcf_path}' niet gevonden."
        if parent:
            QMessageBox.critical(parent, "Fout", error_msg)
        else:
            print(error_msg)
        return None

    contacts_list = []

    try:
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

        success_msg = f"{len(contacts_list)} contacten opgeslagen in '{json_path}'"
        if parent:
            QMessageBox.information(parent, "Succes", success_msg)
        else:
            print(success_msg)
        
        return json_path

    except Exception as e:
        error_msg = f"Fout bij het converteren van VCF naar JSON: {str(e)}"
        if parent:
            QMessageBox.critical(parent, "Fout", error_msg)
        else:
            print(error_msg)
        return None