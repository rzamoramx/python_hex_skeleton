
from piccolo.table import Table
from piccolo.columns import Varchar


class Account(Table, tablename="x_account"):
    contract_id = Varchar(length=150, primary_key=True, null=False)
    account_id = Varchar(length=8, null=False)
