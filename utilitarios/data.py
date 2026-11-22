class FormatarData:
        
    @staticmethod
    def _formatar_data(data) -> str:
        if not data:
            return ""
        
        partes_data = str(data).split("-")
        return f"{partes_data[2].zfill(2)}/{partes_data[1].zfill(2)}/{partes_data[0]}"