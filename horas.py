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
            if h < 24 and m <60:
                return f'{h}:{m:02d}'
            else:
                return f'<span style="color:red">{grupo}</span>'
        
        # 8:30 o 18:05

        h_p_m = re.match(r'^(\d{1,2}):(\d{2})$', grupo)
        if h_p_m:
            h = int(h_p_m.group(1))
            m = int(h_p_m.group(2))
            if h < 24 and m < 60:
                return f'{h}:{m:02d}'
            else:
                return f'<span style="color:red">{grupo}</span>'
        
        # hora hablada

        hablado = re.match(r'^(\d{1,2})\s*(en punto|y cuarto|y media|menos cuarto)$', grupo)
        if hablado:
            h = int(hablado.group(1))
            f = hablado.group(2)

            if f == 'en punto':
                m = 0
            elif f == 'y cuarto':
                m = 15
            elif f == 'y media':
                m = 30
            elif f == 'menos cuarto':
                h -= 1
                if h == 0:
                    h = 12
                m = 45
            return f'{h}:{m:02d}'
        
        hablado_momento = re.match(r'^(\d{1,2})\s*(en punto|y cuarto|y media|menos cuarto)\s+de la\s+(mañana|tarde|noche)$', grupo)

        if hablado_momento:
            h = int(hablado_momento.group(1))
            f = hablado_momento.group(2)
            p = hablado_momento.group(3)

            # según hora hablada

            if f == 'en punto':
                m = 0
            elif f == 'y cuarto':
                m = 15
            elif f == 'y media':
                m = 30
            elif f == 'menos cuarto':
                h -= 1
                if h == 0:
                    h = 12
                m = 45
        
            # según momento del día 

            if p == 'mañana':
                if 1 <= h <= 11:
                    pass
            elif p == 'tarde':
                if 1 <= h <= 7:
                    h += 12
            elif p == 'noche':
                if 8 <= h <= 11:
                    h += 12
                elif h == 12:
                    return '00:00'  
            return f'{h}:{m:02d}'
        
        # momento del día

        momento = re.match(r'^(\d{1,2})\s+de la\s+(mañana|tarde|noche)$', grupo)
        if momento:
            h = int(momento.group(1))
            m = 0
            p = momento.group(2)
            if p == 'mañana':
                if 1 <= h <= 11:
                    pass
            elif p == 'tarde':
                if 1 <= h <= 7:
                    h += 12
            elif p == 'noche':
                if 8 <= h <= 11:
                    h += 12
                elif h == 12:
                    return '00:00'  
            return f'{h}:{m:02d}'
        
        return rojo(grupo)
    
    def rojo(texto):
        return f'<span style = "color:red">{texto}</span>' #devuelve en rojo las expresiones incorrectas
             
    
    compila= re.compile (r'\b\d{1,2}h(?:\d{1,2}m?)?'r'|\b\d{1,2}:\d{2}'r'|\b\d{1,2}\s*(?:en punto|y cuarto|y media|menos cuarto)(?:\s+de la\s+(?:mañana|tarde|noche))?'r'|\b\d{1,2}\s+de la\s+(?:mañana|tarde|noche)')

    with open(ficText, encoding = 'utf-8') as entrada, open(ficNorm, 'w', encoding = 'utf-8') as salida:
        salida.write('<htm><body><pre style="font-family:monospace;">\n')
        for linea in entrada:
            nueva = compila.sub(reemplaza, linea)
            nueva = re.sub(r'\s+de la (mañana|tarde|noche)', '', nueva, flags=re.IGNORECASE) # Elimina 'de la' y 'mañana', 'tarde', 'noche'
            salida.write(nueva)
        salida.write('</pre></body></html>')
    
normalizaHoras('horas.txt', 'horas_normalizadas.txt')
normalizaHoras('horas.txt', 'horas_normalizadas.html') # para que se vea el color rojo
