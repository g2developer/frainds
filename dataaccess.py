import sqlite3


class DataAccess:
    conn = None

    cmm_lst = None
    cmm_target_lst = None

    def __init__(self):
        self.conn = sqlite3.connect('./data/frainds.db')
        self.get_command_list()
        self.get_command_target_list()

    def get_config_value(self, config_name):
        lst = self.conn.cursor().execute(f'''
        SELECT value FROM config WHERE name='{config_name}'
        ''').fetchall()

        return None if len(lst) == 0 else lst[0][0]

    def get_config_option(self, config_name, option_name=None):
        sql = f'''
        SELECT * FROM config_option WHERE config_name='{config_name}'
        '''
        if option_name :
            sql += f" AND name='{option_name}'"
        lst = self.conn.cursor().execute(sql).fetchall()
        if len(lst) == 1:
            return lst[0][2]
        return lst

    def update_config(self, config_name, config_value):
        try:
            self.conn.cursor().execute(f'''
            UPDATE config 
               SET value='{config_value}'
             WHERE name='{config_name}'
                    ''')
            self.conn.commit()
        except Exception as e:
            print(e)

    def get_command_list(self):
        self.cmm_lst = self.conn.cursor().execute(f'''
        SELECT * FROM command
        ''').fetchall()

    def get_command_target_list(self):
        self.cmm_target_lst = self.conn.cursor().execute(f'''
        SELECT * FROM command_target
        ''').fetchall()


    def close(self):
        self.conn.close()



if __name__ == "__main__":

    da = DataAccess()
    chatai = da.get_config_value('chatai')
    print(chatai)
    lst = da.get_config_option('chatai')
    print(lst)
    da.close()
