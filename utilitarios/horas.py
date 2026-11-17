class FormatarHoras:
    
    @staticmethod
    def _formatar_hora(hora_inicio) -> str:
        if not hora_inicio:
            return ""
        
        partes_hora = str(hora_inicio).split(":")
        return f"{partes_hora[0].zfill(2)}:{partes_hora[1]}"
    