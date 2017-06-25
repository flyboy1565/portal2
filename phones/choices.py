
def phone_types():
    return (
        ("PTS", "POTS"),
        ("SIP", "SIP"),
        ('RO', 'Regional Office'),
        ('RCF', 'RCF'),
    )
    

def note_types():
    return (
        ('Site', 'Site Note'),
        ('Bill', 'Billing Note'),
        ('Audit', 'Audit Note'),
    )
    
    
def account_types():
    return (
        ('Master', 'Master Account'),
        ('POTS', 'POTS Account'),
        ('Data', 'Data Account'),
        ('Fire', 'Fire Account'),
    )
    
def stick_types():
    return (
        ('NA', 'Not Available'),
        ('Stick', 'Stick'),
        ('ComSwtch', 'Combo Switch'),
    )