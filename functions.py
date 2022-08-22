def get_error_buchungen(fehlercode):
    result = {}
    if fehlercode == '0':
        result['message'] = "Welcome back!"
        result['box'] = "mbgreen"
    if fehlercode == '1':
        result['message'] = "Buchungssatz wurde erstellt!"
        result['box'] = "mbgreen"
    if fehlercode == '2':
        result['message'] = "Position fehlt oder fehlerhaft (nur Ziffern)!"
        result['box'] = "mbred"
    if fehlercode == '3':
        result['message'] = "Position unbekannt!"
        result['box'] = "mbred"
    if fehlercode == '4':
        result['message'] = "Rechnungsdatum fehlt oder fehlerhafte Eingabe (TT.MM.JJJJ)!"
        result['box'] = "mbred"
    if fehlercode == '5':
        result['message'] = "Zahlungseingang / -ausgang enthält fehlerhafte Eingabe (TT.MM.JJJJ)!"
        result['box'] = "mbred"
    if fehlercode == '6':
        result['message'] = "Brutto Eingabe fehlt oder fehlerhaft (0.00)!"
        result['box'] = "mbred"
    if fehlercode == '7':
        result['message'] = "USt-Schlüssel unbekannt oder fehlerhaft (nur Zahlen)!"
        result['box'] = "mbred"
    if fehlercode == '9':
        result['message'] = "Kostenstelle fehlt oder fehlerhaft (nur Zahlen)!"
        result['box'] = "mbred"
    if fehlercode == '10':
        result['message'] = "Eintrag entfernt / storniert!"
        result['box'] = "mbgreen"
    if fehlercode == '11':
        result['message'] = "Eintrag geändert!"
        result['box'] = "mbgreen"
    return result

def get_error_config(fehlercode):
    result = {}
    if fehlercode == '0':
        result['message'] = "Welcome back!"
        result['box'] = "mbgreen"
    if fehlercode == '1':
        result['message'] = "Eintrag wurde erzeugt!"
        result['box'] = "mbgreen"
    if fehlercode == '2':
        result['message'] = "Positionsnummer fehlt oder fehlerhaft (Nur Zahlen)!"
        result['box'] = "mbred"
    if fehlercode == '3':
        result['message'] = "Positionsbezeichnung fehlt!"
        result['box'] = "mbred"
    if fehlercode == '4':
        result['message'] = "USt-Code fehlt oder fehlerhaft (Nur Zahlen)!"
        result['box'] = "mbred"
    if fehlercode == '5':
        result['message'] = "USt-Satz fehlt oder fehlerhaft (Nur Zahlen)!"
        result['box'] = "mbred"
    if fehlercode == '6':
        result['message'] = "USt-Beschreibung fehlt!"
        result['box'] = "mbred"
    if fehlercode == '7':
        result['message'] = "Eintrag entfernt!"
        result['box'] = "mbgreen"
    if fehlercode == '8':
        result['message'] = "Zuordnung Einnahme / Ausgabe fehlt!"
        result['box'] = "mbred"
    if fehlercode == '9':
        result['message'] = "Position existiert bereits!"
        result['box'] = "mbred"
    if fehlercode == '10':
        result['message'] = "USt-Code existiert bereits!"
        result['box'] = "mbred"
    return result