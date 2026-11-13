class FormatarTelefone:
    
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