from calendar import month
from db.connection_db import session
from contoller.energy_bill import calculate_energy_bill

year = 2023
month = 9
result = calculate_energy_bill(session, month, year)

for id_service, EA, EC, EE1, EE2 in result:
    print("id_service: {:.2f} EA: {:.2f} EC: {:.2f} EE1: {:.2f} EE2: {:.2f}".format(id_service, EA, EC, EE1, EE2))

session.close()
