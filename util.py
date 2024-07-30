
def format_argent(argent):
    argent = round(argent, 2)
    argent = "{:,}".format(argent).replace(',', ' ')
    return argent

def format_temps(temps): # en heure
    if temps < 24:
        return str(temps) + " H "
    day = temps / 24
    return str(round(day, 1)) + " J "
