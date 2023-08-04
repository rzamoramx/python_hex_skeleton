
from piccolo.table import Table
from piccolo.columns import Varchar


class User(Table, tablename="x_user"):
    id = Varchar(length=36, primary_key=True, null=False)
    nombre = Varchar(lenght=40, null=False)
    apaterno = Varchar(lenght=40, null=False)
    amaterno = Varchar(lenght=40, null=False)
    email = Varchar(lenght=100, null=False)
    genero = Varchar(lenght=16, null=False)
