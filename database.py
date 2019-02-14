""""
	The module for handling database connections
"""

import mysql.connector

class db_context:
    def __init__(self, config):
        self._config = config

    def __enter__(self):
        self._db = mysql.connector.connect(
            host = self._config["host"],
            database = self._config["database"],
            user = self._config["credentials"]["mysql-username"],
            passwd = self._config["credentials"]["mysql-password"]
        )
        self._db_cursor = self._db.cursor(buffered = True)
        return self

    def list_illegal_phrases(self, group_jid):
        sql = """SELECT ip.phrase_text 
				FROM group_chat gc
				JOIN group_chat_illegal_phrases ip ON gc.id = ip.group_chat_id
				WHERE gc.group_jid = '{0}'""".format(group_jid)
        
        self._db_cursor.execute(sql)
     
        # for..yield would have been better but it results that database object instead of an plain list
        list = []

        for x in self._db_cursor:
            list.append(x[0])

        return list


    # TODO: How this works against SQL injections?
    def add_illegal_phrase(self, group_jid, phrase_text):
        # First, INSERT group if it does not exists in the database  
        self._db_cursor.execute("SELECT gc.* FROM group_chat gc WHERE gc.group_jid = '{0}'".format(group_jid))
        exists_results = self._db_cursor.fetchall()

        if not exists_results or len(exists_results) == 0:
            print("Inserting new group '"+group_jid+"' to the database. The sql script:");
            self._db_cursor.execute("INSERT INTO group_chat(group_jid) VALUES ({0})".format(group_jid))
            self._db_cursor.fetchall()

        # Yet before insert, fetch the row data, so we will know the id. 
        # This could be handled in an otherway, might be a bit slow solution?
        # Maybe you should use operations??
        #print("id: " + exists_results[0][0] + ", phrase_text: " + phrase_text)
        exists_results = self._db_cursor.execute("SELECT gc.* FROM group_chat gc WHERE gc.group_jid = '{0}'".format(group_jid))
        exists_results = self._db_cursor.fetchall()
        self._db_cursor.execute("INSERT INTO group_chat_illegal_phrases(group_chat_id, phrase_text) VALUES ('{0}', '{1}')".format(exists_results[0][0], phrase_text))

    def __exit__(self, exception_type, exception_value, traceback):
        self._db_cursor.close()
        self._db.close()