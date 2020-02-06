import json
from datetime import date, datetime

import psycopg2
from starlette.testclient import TestClient

from .api.main import app

# current_path = os.path.abspath('.')
# parent_path = os.path.dirname(current_path)
# sys.path.append(parent_path)


client = TestClient(app)

PATH_SCRIPT_DATA = "back_end/migrations/init_data.sql"


def get_postgres_cursor(host, usr, port, pwd, db):
    conn = f"host='{host}' user='{usr}' password='{pwd}' port={port} dbname='{db}'"
    conn = psycopg2.connect(conn)
    return conn


def execute_query(conn, cursor, query, commit=True):
    """
    :param query:
    ejecuta una consulta y no retorna nada
    """

    cursor.execute(query)
    if commit:
        conn.commit()


def get_token_request(user_name, password):
    obj = {
        "username": user_name,
        "password": password,
        "grant_type": None,
        "scope": None,
        "client_id": None,
        "client_secret": None

    }
    response = client.post(f"/token", headers={"accept": "application/json",
                                               "Content-Type": "application/x-www-form-urlencoded"}, data=obj)
    return response


def test_trunc_database():
    def __drop_all(conn):
        cursor = conn.cursor()
        queries = [
            "DELETE FROM c_transaction CASCADE;",
            "DELETE FROM c_coins CASCADE;",
            "DELETE FROM c_user CASCADE;",
            "DELETE FROM c_user_type CASCADE;",
            "DELETE FROM c_transaction_type CASCADE;",
        ]
        for q in queries:
            execute_query(conn, cursor, q)

        with open(PATH_SCRIPT_DATA, "r") as A:
            lines = A.readlines()

        for l in lines:
            execute_query(conn, cursor, l)

        cursor.close()
        conn.close()

    conn = get_postgres_cursor('cripto_postgres', 'postgres', 5432, 'postgres', 'cripto_db')
    __drop_all(conn)


def test_create_user(capsys):
    """
    with capsys.disabled():
        print("output not captured, going directly to sys.stdout")
    print("this output is also captured")
    """

    def _t(user_name, status, type_id, email, password, status_code_ok):
        obj = {
            "username": user_name,
            "status": status,
            "type_id": type_id,
            "email": email,
            "password": password
        }
        response = client.post(f"/user/", headers={"accept": "application/json"}, json=obj)
        assert response.status_code == status_code_ok

    _t("testing", 1, 1, "testing@testing.com", "testing", 422)
    _t("usuario400", 1, 2, "estenoesunemail", "testing", 422)
    _t("usuario108", 1, 2, "email@email.com", "testing", 200)
    _t("usuario_test", 1, 2, "email@email.com", "testing", 400)
    _t("usuario108", 1, 2, "email2@email.com", "testing", 400)
    _t("usuario101", 1, 2, "email2@email.com", "testing", 200)


def test_login(capsys):
    """
    with capsys.disabled():
        print("output not captured, going directly to sys.stdout")
    print("this output is also captured")
    """

    def _t(user_name, password, status_code_ok):
        assert get_token_request(user_name, password).status_code == status_code_ok

    _t("email@email.com", "badpass", 401)
    _t("email200@email.com", "testing", 401)
    _t("email@email.com", "testing", 200)


def test_create_coin(capsys):
    """
    with capsys.disabled():
        print("output not captured, going directly to sys.stdout")
    print("this output is also captured")
    """
    req = get_token_request("master@master.com", "master")
    token = json.loads(req.content)

    def _t(id, desc, status, status_code_ok, created_at=str(date.today())):
        obj = {
            "description": desc,
            "id": id,
            "created_at": created_at,
            "status": status
        }
        response = client.post(f"/coin/", headers={"accept": "application/json",
                                                   "Authorization": f"{token['token_type']} {token['access_token']}"}
                               , json=obj)
        assert response.status_code == status_code_ok

    _t("BTx", "bitcoin2", 1, 422)
    _t("B C", "bitcoin3", 1, 422)
    _t("BTC", "bitcoin", 1, 200)
    _t("BTC2", "bitcoin4", 1, 422)
    _t("UYU", "pesos uruguayos", 1, 200)

    req = get_token_request("email@email.com", "testing")  # is not admin
    token = json.loads(req.content)
    _t("ARG", "pesos argentinos", 1, 401)


def test_create_transaction(capsys):
    """
    with capsys.disabled():
        print("output not captured, going directly to sys.stdout")
    print("this output is also captured")
    """
    req = get_token_request("email@email.com", "testing")
    token = json.loads(req.content)

    def _t(value, coin, sender, t_type, receiver, status_code_ok, t_date=str(datetime.now())):
        obj = {
            "send_value": value,
            "date": t_date,
            "coin_id": coin,
            "type_id": t_type,
            "user_sender_username": sender,
            "user_receiver_username": receiver
        }
        response = client.post(f"/transaction/", headers={"accept": "application/json",
                                                          "Authorization": f"{token['token_type']} {token['access_token']}"}
                               , json=obj)
        assert response.status_code == status_code_ok

    def check_balance(money, coin):
        response = client.get(f"/user/balance", headers={"accept": "application/json",
                                                         "Authorization": f"{token['token_type']} {token['access_token']}"})
        assert response.status_code == 200 and money == response.json()[coin]

    _t(1500, "BTC", None, 2, 'usuario108', 200)
    check_balance(1500, "BTC")
    _t(500, "BTC", 'usuario108', 3, 'usuario101', 200)
    check_balance(1000, "BTC")
    _t(500, "BTC", None, 3, 'usuario108', 400)
    _t(500, "BTC", 'usuario108', 1, None, 200)
    check_balance(500, "BTC")
    _t(500, "BTC", 'usuario101', 2, None, 400)
    _t(500, "BTCA", 'usuario108', 2, None, 400)
    _t(500, "UYU", 'usuario101', 3, 'usuario108', 400)
    _t(500, "BTC", 'usuario108', 1, None, 200)
    check_balance(0, "BTC")
    _t(500, "BTC", 'usuario108', 1, None, 400)

    req = get_token_request("email2@email.com", "testing")
    token = json.loads(req.content)
    check_balance(500, "BTC")


test_trunc_database()
