
import re

def normalizaHoras(ficText, ficNorm):

    """
    Función que normaliza horas de un fichero de texto a un formato HH:MM
    """
    def reemplaza(match):
        grupo = match.group()

        # 8h30 o 08h5m
        h_m = re.match(r'^(\d{1,2})h(?:(\d{1,2})m?)?$', grupo)
        if h_m:
            h = int(h_m.group(1))
            m = int(h_m.group(2)) if h_m.group(2) else 0
            return f'{h}:{m:02d}'
        

        
        # 8:30 o 18:05
        h_p_m = re.match(r'^(\d{1,2}):(\d{2})$', grupo)
        if h_p_m:
            return grupo
        
        # hora hablada

        hablado = re.match(r'^(\d{1,2})\s*(en punto|y cuarto|y media|menos cuarto)$', grupo)
        if hablado:
            h = int(hablado.group(1))
            f = hablado.group(2)

            if f == 'en punto':
                return f'{h:02d}:00'
            elif f == 'y cuarto':
                return f'{h:02d}:15'
            elif f == 'y media':
                return f'{h:02d}:30'
            elif f == 'menos cuarto':
                h -= 1
                if h == 0:
                    h = 12
                return f'{h:02d}:45'
            return grupo
        
        # momento del día

        momento = re.match(r'^(\d{1,2})\s+de la\s+(mañana|tarde|noche)$', grupo)
        if momento:
            h = int(momento.group(1))
            p = momento.group(2)
            if p == 'mañana':
                if 1 <= h <= 11:
                    return f'{h:02d}:{m:02d}'
            elif p == 'tarde':
                if 1 <= h <= 7:
                    return f'{h+12:02d}:{m:02d}'
            elif p == 'noche':
                if 8 <= h <= 11:
                    return f'{h+12:02d}:{m:02d}'
                elif h == 12:
                    return '00:00' 
            return grupo
        return grupo
    
    
    compila= re.compile (r'\b\d{1,2}h(?:\d{1,2}m?)?'r'|\b\d{1,2}:\d{2}'r'|\b\d{1,2}\s*(?:en punto|y cuarto|y media|menos cuarto)'r'|\b\d{1,2}\s+de la\s+(?:mañana|tarde|noche)')

    with open(ficText, encoding = 'utf-8') as entrada, open(ficNorm, 'w', encoding = 'utf-8') as salida:
        for linea in entrada:
            nueva = compila.sub(reemplaza, linea)
            salida.write(nueva)
    
normalizaHoras('horas.txt', 'horas_normalizadas.txt')
