from configuration.db_connection import Database


def test_db_connection():
    db = Database()
    sql_out = db.run_query("SELECT email from tblRegistration where email = chetan123@gmail.com")
    assert sql_out == 1



