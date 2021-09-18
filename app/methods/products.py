import sqlalchemy

_db_ = sqlalchemy.create_engine("postgres://postgres:123456789@192.168.0.110:5432/main")
_connection_ = _db_.connect()


def _eanExists_(ean):


def getEan(ean):
