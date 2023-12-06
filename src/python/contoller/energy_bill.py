from db.connection_db import (
    Consumption,
    Tariffs,
    Injection,
    Records,
    Services,
    XmDataHourlyPerAgent,
)
from sqlalchemy import func, extract


def calculate_energy_bill(session, month, year):
    """
    Calculates the values of Active Energy (AE), Excess Energy Commercialization (EC),
    Excess Energy Type 1 (EE1) and Excess Energy Type 2 (EE2) for all services in a
    specific month and year.

    The function uses the tables 'consumption', 'injection', 'tariffs', 'records',
    'services', and 'xm_data_hourly_per_agent' to calculate the values. These calculations
    are based on the sum of consumed and injected energy values, applying the corresponding
    tariffs.

    Args:
        session (Session): SQLAlchemy session object for interacting with the databases.
        month (int): Month for which the calculation is to be made, represented as an integer (1-12).
        year (int): Year for which the calculation is to be made, represented as an integer number.

    Returns:
        list of tuples: A list of tuples, where each tuple contains the values computed for a
        specific service. Each tuple consists of: (id_service, EA, EC, EE1, EE2)

    Example:
        # Create an SQLAlchemy session.
            session = Session()

        # Calculate values for September 2023.
            results = calculate_energy_bill(session, 9, 2023)
            for result in results:
                print(result)
    """
    result = []
    unique_id_service = (
        session.query(Records.id_service)
        .filter(
            extract("year", Records.record_timestamp) == year,
            extract("month", Records.record_timestamp) == month,
        )
        .distinct()
        .all()
    )

    # Extracts the values of id_service from the tuples
    unique_id_service_values = [record[0] for record in unique_id_service]

    if len(unique_id_service_values) == 0:
        print(f"No charges for the month's bill {month}/{year}.")

    for id_service in unique_id_service_values:
        EA = 0
        EC = 0
        EE1 = 0
        EE2 = 0

        # Get CU and C - Tariffs
        # Search for the service with the given id_service
        service = session.query(Services).filter_by(id_service=id_service).one()

        # Search for the rates associated with that service
        tariffs = (
            session.query(Tariffs)
            .filter_by(
                id_market=service.id_market,
                cdi=service.cdi,
                voltage_level=service.voltage_level,
            )
            .one()
        )

        # Calculate EA
        value_consumption = (
            session.query(func.sum(Consumption.value))
            .join(Records, Consumption.id_record == Records.id_record)
            .filter(Records.id_service == id_service)
            .scalar()
        )
        EA = value_consumption * tariffs.CU

        # Calculate EA
        value_injection = (
            session.query(func.sum(Injection.value))
            .join(Records, Injection.id_record == Records.id_record)
            .filter(Records.id_service == id_service)
            .scalar()
        )
        EC = value_injection * tariffs.C

        # Calculate EE1
        quantity_EE1 = 0
        if value_injection <= value_consumption:
            quantity_EE1 = value_injection
        else:
            quantity_EE1 = value_consumption
        EE1 = quantity_EE1 * tariffs.CU * -1

        # Calculate EE2
        quantity_EE2 = 0
        if value_injection > value_consumption:
            quantity_EE2 = value_consumption - value_injection

        # Obtain hourly injection data - records.record_timestamp, injection.value, xm_data_hourly_per_agent.value
        hourly_injection = (
            session.query(
                Records.record_timestamp,
                func.sum(Injection.value),
                XmDataHourlyPerAgent.value,
            )
            .join(Injection, Records.id_record == Injection.id_record)
            .join(
                XmDataHourlyPerAgent,
                Records.record_timestamp == XmDataHourlyPerAgent.record_timestamp,
            )
            .filter(
                Records.id_service == id_service,
                extract("month", Records.record_timestamp) == month,
                extract("year", Records.record_timestamp) == year,
            )
            .group_by(Records.record_timestamp, XmDataHourlyPerAgent.value)
            .order_by(Records.record_timestamp)
            .all()
        )


        accumulated_sum = 0
        # Iterate over the data to find the time where the limit is exceeded.
        for timestamp, injection_value, xm_data_hourly_per_agent_value in hourly_injection:
            accumulated_sum += injection_value
            if accumulated_sum > EE1:
                EE2 += quantity_EE2 * xm_data_hourly_per_agent_value
            else:
                # take the negative CU as the rate
                EE2 += quantity_EE2 * tariffs.CU * - 1
        
        result.append((id_service, EA, EC, EE1, EE2))
    return result
