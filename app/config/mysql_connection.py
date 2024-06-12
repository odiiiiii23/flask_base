"""Archivo de configuración de la conexión a la base de datos MySQL."""

# Standard libraries
import os

# PyMSQL
import pymysql.cursors


class MySQLConnection:
    """Modelo de la clase de conexión a la base de datos MySQL."""

    def __init__(self):
        """Constructor de la clase."""

        # Configurar la conexión a la base de datos
        connection = pymysql.connect(
            host=os.getenv("MYSQL_HOST"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            db=os.getenv("MYSQL_DB"),
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )

        # Guardar la conexión en la instancia de la clase
        self.connection = connection

    def query_db(self, query, data=None):
        """
        Método para consultar la base de datos.
        Recibe la consulta y los datos a insertar en la consulta.

        - Si la consulta es un INSERT devolverá el ID del registro insertado.
        - Si la consulta es un SELECT devolverá los registros de la base de
        datos como una lista de diccionarios.
        - Si la consulta es un UPDATE o DELETE no devolverá nada.
        """

        with self.connection.cursor() as cursor:
            try:
                query = cursor.mogrify(query, data)
                print(f"Running Query: {query}")
                cursor.execute(query, data)

                # Si la consulta es un INSERT
                if query.lower().find("insert") >= 0:
                    self.connection.commit()
                    return cursor.lastrowid
                # Si la consulta es un SELECT
                elif query.lower().find("select") >= 0:
                    result = cursor.fetchall()
                    return result
                # Si la consulta es un UPDATE o DELETE
                else:
                    self.connection.commit()
            except Exception as e:
                # Si hay un error, imprimirlo y devolver False
                print(f"Something went wrong: {e}")
                return False
            finally:
                # Cerrar la conexión a la base de datos
                self.connection.close()


def connect_to_mysql():
    """Método para conectar a la base de datos MySQL."""
    return MySQLConnection()
