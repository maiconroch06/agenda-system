Instalação do ambiente Virtual - LINUX

sudo apt update

//Esse comando instala o pacote necessário para criar ambientes virtuais do Python
sudo apt install python3-venv -y


python3 -m venv .venv

source .venv/bin/activate

deactivate

Instalação do ambiente Virtual - WINDOWS

python --version

python -m venv .venv
.venv\Scripts\Activate.ps1

//Se o PowerShell bloquear o script
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

.venv\Scripts\Activate.ps1

//Verificar se está ativo
python --version
where.exe python 
//SAÍDA DO COMANDO{.venv\Scripts\python.exe}

python -m pip install --upgrade pip
pip install flask

COMANDOS FUTUROS
Se quiser que outros dispositivos da sua rede possam acessar a API
flask --app main run --host=0.0.0.0 --port=5000


COMANDOS PARA ACESSAR ARQUIVOS
<img src="{{ url_for('static', filename='img/logo.png') }}">
<link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
<script src="{{ url_for('static', filename='js/script.js') }}"></script>
FONTES TBM ESTARIA AQUI.
