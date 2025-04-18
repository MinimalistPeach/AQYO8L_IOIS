import os
from spyne import Application, rpc, ServiceBase, Integer, Unicode, Date, Array
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
import mysql.connector
from spyne.model.primitive import String
from dotenv import load_dotenv

load_dotenv()

class PersonService(ServiceBase):

    @rpc(_returns=Array(Unicode))
    def get_all_person(ctx):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT nev, szul_ido, szul_hely," \
        "anyja_neve, nem, lakcim, email FROM szemelyek")
        results = cursor.fetchall()
        conn.close()

        if not results:
            return []

        persons_list = [f"{nev} ({szul_ido} - {szul_hely} - {anyja_neve} - {nem} - {lakcim} - {email})" for nev, szul_ido, szul_hely, anyja_neve, nem, lakcim, email in results]
        return persons_list

    @rpc(Unicode, Date, Unicode, Unicode, Unicode, Unicode, Unicode, _returns=Unicode)
    def add_person(ctx, nev, szul_ido, szul_hely, anyja_neve, nem, lakcim, email):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO szemelyek (nev, szul_ido, szul_hely," \
        "anyja_neve, nem, lakcim, email) VALUES (%s, %s, %s, %s, %s, %s, %s)", (nev, szul_ido, szul_hely, anyja_neve, nem, lakcim, email))
        conn.commit()
        conn.close()
        return "Személy sikeresen felvételre került!"
    
def get_db_connection():
    return mysql.connector.connect(
            host=os.environ.get("DB_HOST", "mariadb"),
            port=os.environ.get("DB_PORT", 3306),
            user=os.environ.get("DB_USER", "szemelynyilvantarto"),
            password=os.environ.get("DB_PASSWORD", "szemelynyilvantarto123"),
            database=os.environ.get("DB_NAME", "aqyo8l_iois")
    )

soap_app = Application([PersonService],
                       tns='spyne.person.service',
                       in_protocol=Soap11(validator='lxml'),
                       out_protocol=Soap11())

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    print("SOAP szerver fut a http://0.0.0.0:8000/soap címen...")
    wsgi_app = WsgiApplication(soap_app)
    server = make_server('0.0.0.0', 8000, wsgi_app)
    server.serve_forever()
