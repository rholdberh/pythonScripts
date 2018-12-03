import pyhdb
import datetime
import time


class Table(object):
    table_name = ""
    table_count = 0

    def __init__(self, table_name, table_count):
        self.table_name = table_name
        self.table_count = table_count

    def update_count(self, table_count):
        self.table_count = table_count

    def get_count(self):
        return self.table_count


def get_count_for_table(table):
    connection = pyhdb.connect(
        host="host",
        port=port,
        user="user",
        password="pass"
    )

    select = "SELECT COUNT(*) FROM %s" % (table)
    cursor = connection.cursor()
    cursor.execute(select)
    result = cursor.fetchone()[0]

    try:
        cursor.close()
    except ConnectionResetError:
        print("Oops")

    return result


def table_is_in_list(table_name, table_list):
    for table in table_list:
        if table_name == table.table_name:
            return table
    return None


def write_file(table_name, value):
    file_name = table_name + ".csv"
    f = open(file_name, "a+")
    f.write(value)
    f.write("\n")
    f.close()


def get_write_counts():
    tables = ["AAAA", "BBBB"]

    for table in tables:
        count = get_count_for_table(table)
        table_object = table_is_in_list(table, tables_object_list)
        if table_object is not None:
            previous_count = table_object.get_count()

            value = ""

            if previous_count < count:
                value += str(count) + "," + str(datetime.datetime.utcnow()) + ",i"

            elif previous_count == count:
                value += str(count) + "," + str(datetime.datetime.utcnow()) + ",e"

            else:
                value += str(count) + "," + str(datetime.datetime.utcnow()) + ",d"

            write_file(table, value)
            table_object.update_count(count)

        else:
            t = Table(table, count)
            tables_object_list.append(t)
            value = str(count) + "," + str(datetime.datetime.utcnow())
            write_file(table, value)


tables_object_list = []
counter = 0
while counter < 3600:
    get_write_counts()
    counter += 1
    time.sleep(10)
