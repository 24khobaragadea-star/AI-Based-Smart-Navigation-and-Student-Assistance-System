import pandas as pd
from db import get_db_connection

EXCEL_FILE = "../DATA/Smart_Campus_Complete_Systematic_Dataset (5).xlsx"


def clean(value):
    if pd.isna(value):
        return None
    return str(value).strip()


def import_sheet(connection, excel_sheet, table, mapping):
    df = pd.read_excel(EXCEL_FILE, sheet_name=excel_sheet)

    cursor = connection.cursor()

    # Remove previous partial import
    cursor.execute(f"DELETE FROM `{table}`")

    mysql_columns = ", ".join(
        f"`{mysql_col}`" for mysql_col in mapping.values()
    )

    placeholders = ", ".join(["%s"] * len(mapping))

    sql = f"""
        INSERT INTO `{table}` ({mysql_columns})
        VALUES ({placeholders})
    """

    for _, row in df.iterrows():
        values = [
            clean(row[excel_col])
            for excel_col in mapping.keys()
        ]

        cursor.execute(sql, tuple(values))

    connection.commit()
    cursor.close()

    print(f"{excel_sheet}: {len(df)} records imported")


def main():

    print("======================================")
    print("SMART CAMPUS DATA IMPORT")
    print("======================================")
    print()

    print("Connecting to MySQL...")

    connection = get_db_connection()

    print("MySQL connection successful!")
    print()

    # -------------------------------------------------
    # FACULTY
    # -------------------------------------------------

    import_sheet(
        connection,
        "FACULTY_ALL",
        "faculty",
        {
            "FACULTY NAME": "faculty_name",
            "DEPARTMENT": "department",
            "BUILDING": "building",
            "FLOOR": "floor",
            "ROOM NO.": "room_no",
            "E-MAIL": "email"
        }
    )

    # -------------------------------------------------
    # CLASSROOMS
    # -------------------------------------------------

    import_sheet(
        connection,
        "CLASSROOMS_ALL",
        "classrooms",
        {
            "ROOM NO.": "room_no",
            "BUILDING": "building",
            "FLOOR": "floor",
            "SOURCE": "source"
        }
    )

    # -------------------------------------------------
    # LABS
    # -------------------------------------------------

    import_sheet(
        connection,
        "LABS_ALL",
        "labs",
        {
            "LAB ROOM NO.": "lab_room_no",
            "BUILDING": "building",
            "FLOOR": "floor",
            "SOURCE": "source"
        }
    )

    # -------------------------------------------------
    # OFFICES
    # -------------------------------------------------

    import_sheet(
        connection,
        "OFFICES_ALL",
        "offices",
        {
            "OFFICE": "office",
            "BUILDING": "building",
            "FLOOR": "floor",
            "TIMING": "timing",
            "SERVICES": "services",
            "SOURCE": "source"
        }
    )

    # -------------------------------------------------
    # DEPARTMENTS
    # -------------------------------------------------

    import_sheet(
        connection,
        "DEPARTMENTS_ALL",
        "departments",
        {
            "DEPARTMENT": "department",
            "HOD": "hod",
            "ROOM NO.": "room_no",
            "E-MAIL": "email",
            "SOURCE": "source"
        }
    )

    # -------------------------------------------------
    # ADMIN SERVICES
    # -------------------------------------------------

    import_sheet(
        connection,
        "ADMIN_SERVICES",
        "admin_services",
        {
            "BLOCK NAME": "block_name",
            "DEPARTMENT / ROOM": "department_room",
            "SERVICES PROVIDED": "services_provided",
            "SOURCE": "source"
        }
    )

    # -------------------------------------------------
    # DT SEATING PLAN
    # -------------------------------------------------

    import_sheet(
        connection,
        "DT_SEATING_PLAN",
        "dt_seating_plan",
        {
            "FLOOR": "floor",
            "FACULTY NAME": "faculty_name",
            "ROOM / CABIN NO.": "room_cabin_no",
            "SOURCE SHEET": "source_sheet",
            "SOURCE ROW": "source_row"
        }
    )

    connection.close()

    print()
    print("======================================")
    print("ALL DATA IMPORTED SUCCESSFULLY!")
    print("======================================")


if __name__ == "__main__":
    main()