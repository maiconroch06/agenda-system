from models.Address import Address
from models.BarberShop import BarberShop
from models.User import User

def initialize():
    id_endereco = Address.insertDefaultAdress()
    id_gestor = User.insertUserGestor(id_endereco)
    BarberShop.insertDefualtBarbearia(id_gestor,id_endereco) 