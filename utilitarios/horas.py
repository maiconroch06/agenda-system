class FormatarHoras:
    
    @staticmethod
    def _formatar_hora(hora_inicio) -> str:
        if not hora_inicio:
            return ""
        
        partes_hora = str(hora_inicio).split(":")
        return f"{partes_hora[0].zfill(2)}:{partes_hora[1]}"
    
    @staticmethod
    def _formatar_telefone(telefone_cliente: str) -> str:
        if not telefone_cliente:
            return ""
        # Remove tudo que não for número
        numeros = "".join(filter(str.isdigit, str(telefone_cliente)))
        
        if len(numeros) == 11:  # Celular: (84) 99898-9898
            return f"({numeros[:2]}) {numeros[2:7]}-{numeros[7:]}"
        elif len(numeros) == 10:  # Fixo: (84) 3281-1234
            return f"({numeros[:2]}) {numeros[2:6]}-{numeros[6:]}"
        
        return telefone_cliente  # Retorna original se tiver outro tamanho