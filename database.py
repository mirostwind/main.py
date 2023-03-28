import psycopg2

def get_connection():
    conn = psycopg2.connect(database='f26bot', user='postgres', password='3052102', host='localhost', port=5432)
    return conn

def create_table_profile():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS profile(
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(300),
    last_name VARCHAR(300),
    user_name VARCHAR(200),
    telegram_id BIGINT
    )
    """)
    conn.commit()
    conn.close()

def update_profile_contact(user_id, phone):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"""
    Update profile SET phone = '{phone}'
    where telegram_id = {user_id}
    """)

    conn.commit()
    conn.close()


def get_user_data_with_telegram_id(telegram_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"""
    select * from profile
    where telegram_id = {telegram_id}
    """)

    data = cursor.fetchall()
    return data


def alter_table_profile():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
        ALTER TABLE profile
        ADD COLUMN phone VARCHAR(12);
        """)
    except Exception as e:
        pass
    conn.commit()
    conn.close()


def modify_table_profile_phone():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
        ALTER TABLE profile
        ALTER COLUMN phone TYPE VARCHAR(30);
        """)
    except Exception as e:
        pass
    conn.commit()
    conn.close()


def create_table_region():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS region(
    id SERIAL PRIMARY KEY,
    title VARCHAR(100)
    )
    """)
    conn.commit()
    conn.close()

def create_table_district():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS district(
    id SERIAL PRIMARY KEY,
    region_id INT,
    title VARCHAR(100)
    )
    """)

    conn.commit()
    conn.close()

def check_user_in_table(telegram_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"""
    select * from profile
    where telegram_id={telegram_id}
""")
    data = cursor.fetchall()

    if data:
        return True
    return False

def get_region_by_title(title):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"""
    select * from region
    where title = %s
""", (title,))
    data = cursor.fetchall()
    return data

def get_district_by_title(title):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"""
    select * from district
    where title = %s
    """, (title, ))
    data = cursor.fetchall()
    return data

def get_district_by_id(id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"""
    select * from district
    where id = %s
    """, (id, ))
    data = cursor.fetchall()
    return data

def get_region_by_id(id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"""
    select * from region
    where id = %s
    """, (id, ))
    data = cursor.fetchall()
    conn.commit()
    conn.close()
    return data

def districts_by_region_id(region_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"""
    select * from district
    where region_id = {region_id}
    """)
    data = cursor.fetchall()
    return data

def insert_user_to_table(first_name, last_name, username, telegram_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"""
    insert into profile(first_name, last_name, user_name, telegram_id)
    values(%s, %s, %s, %s)
    """, (first_name, last_name, username, telegram_id))

    conn.commit()
    conn.close()

def insert_region_to_table(id, title):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"""
    insert into region(id, title)
    values(%s, %s)
    """, (id, title))

    conn.commit()
    conn.close()

def insert_district_to_table(id,region_id, title,):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"""
    insert into district(id,region_id, title)
    values(%s, %s, %s)
    """, (id, region_id, title))

    conn.commit()
    conn.close()

def select_all_regions():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"""
    select * from region
""")
    data = cursor.fetchall()
    conn.commit()
    conn.close()
    return data


def restore_regions():
    import pandas as pd
    data = pd.read_csv('data/regions.csv', encoding='utf-8')
    data = data.values.tolist()
    # print(data)
    for row in data:
        insert_region_to_table(row[0], row[1])

def restore_districts():
    import pandas as pd
    data = pd.read_csv('data/districts.csv', encoding='utf-8')
    data = data.values.tolist()
    for row in data:
        # print(row)
        insert_district_to_table(row[0], row[3], row[1])


create_table_profile()
create_table_region()
modify_table_profile_phone()
create_table_district()
alter_table_profile()