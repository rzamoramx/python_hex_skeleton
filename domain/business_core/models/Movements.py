
from piccolo.table import Table
from piccolo.columns import Varchar, UUID, Timestamptz, Numeric, ForeignKey, Float
from domain.business_core.models.Account import Account


class Movements(Table, tablename="x_movements"):
    id = UUID(primary_key=True, null=False)
    name = Varchar(length=3, null=True)
    concept = Varchar(length=40, null=True)
    date = Timestamptz(null=False)
    amount = Numeric(null=False)
    issuer_name = Varchar(length=150, null=True)
    issuer_account = Varchar(length=18, null=True)
    issuer_bank = Varchar(length=10, null=True)
    created_date = Timestamptz(null=False)
    updated_date = Timestamptz(null=False)
    account_id = ForeignKey(references=Account)
    dollar_price = Float(null=False)
    quantity_dollars = Float(null=False)
    tracking_clave = Varchar(length=50, null=True)
    clabe = Varchar(length=20, null=True)
    status = Varchar(length=1, null=True)
