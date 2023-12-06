from calendar import month
from db.connection_db import session
from contoller.energy_bill import calculate_energy_bill

year = 2023
month = 9
result = calculate_energy_bill(session, month, year)
print(result)

session.close()