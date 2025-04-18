import os
from spyne import Application, rpc, ServiceBase, Unicode, Date, Iterable
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

class PersonService(ServiceBase):

    @rpc(_returns=Iterable(Unicode))
    def get_all_person(ctx):
        conn = mysql.connector.connect(
            host=os.environ.get("DB_HOST", "localhost"),
            user=os.environ.get("DB_USER", "szemelynyilvantarto"),
            password=os.environ.get("DB_PASSWORD", "szemelynyilvantarto123"),
            database=os.environ.get("DB_NAME", "aqyo8l_iois")
        )
        cursor = conn.cursor()
        cursor.execute("SELECT nev, szul_ido, szul_hely," \
        "anyja_neve, nem, lakcim, email FROM szemelyek")
        results = cursor.fetchall()
        conn.close()

        for nev, szul_ido, szul_hely, anyja_neve, nem, lakcim, email in results:
            yield f"{nev} ({szul_ido} - {szul_hely} - {anyja_neve} - {nem} - {lakcim} - {email})"

    @rpc(Unicode, Date, _returns=Unicode)
    def add_person(ctx, nev, szul_ido, szul_hely, anyja_neve, nem, lakcim, email):
        conn = mysql.connector.connect(
            host=os.environ.get("DB_HOST", "localhost"),
            user=os.environ.get("DB_USER", "szemelynyilvantarto"),
            password=os.environ.get("DB_PASSWORD", "szemelynyilvantarto123"),
            database=os.environ.get("DB_NAME", "aqyo8l_iois")
        )
        cursor = conn.cursor()
        cursor.execute("INSERT INTO szemelyek (nev, szul_ido, szul_hely," \
        "anyja_neve, nem, lakcim, email) VALUES (%s, %s, %s, %s, %s, %s, %s)", (nev, szul_ido, szul_hely, anyja_neve, nem, lakcim, email))
        conn.commit()
        conn.close()
        return "Személy sikeresen felvételre került!"

soap_app = Application([PersonService],
                       tns='soap.person.service',
                       in_protocol=Soap11(),
                       out_protocol=Soap11())

wsgi_app = WsgiApplication(soap_app)

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    print("SOAP szerver fut a http://localhost:8000/soap címen...")
    server = make_server('0.0.0.0', 8000, wsgi_app)
    server.serve_forever()
