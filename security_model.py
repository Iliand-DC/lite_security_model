import copy as cp
import random
import dearpygui.dearpygui as dpg

access_variable = ['Нет прав', 'Читать', 'Запись',
                    'Передача прав','Читать/Запись',
                    'Читать/Передача прав','Запись/Передача прав',
                    'Полные права']

class AccessMatrix:
    def __init__(self, matrix, user_list, file_list):
        self.access_matrix = cp.deepcopy(matrix)
        self.user_list = cp.deepcopy(user_list)
        self.file_list = cp.deepcopy(file_list)

    def set_right(self, userId, fileId, newRight):
        self.access_matrix[userId][fileId] = newRight

    def get_access(self, userId, fileId):
        return self.access_matrix[userId][fileId]
    
    def get_users_count(self):
        return len(self.access_matrix)
    
    def get_files_count(self):
        return len(self.access_matrix[:,1])

    def active_user(self, user_name):
        global active_user 
        active_user = user_name
    
    def can_be_changed(self, user_name, file_name):
            right = ''
            user_id = self.user_list.index(user_name)
            file_id = self.file_list.index(file_name)
            right = self.access_matrix[user_id][file_id]
            if 'Передача прав' in right:
                return True
            elif 'Полные права' in right:
                return True
            else: False

    def get_access_to_file(self, userName, file_name, doing):
        result = ''
        user_id = self.user_list.index(userName)
        file_id = self.file_list.index(file_name)
        right = self.get_access(user_id, file_id)

        if right == 'Полные права':
            result += ('Доступ получен\n')
        elif doing in right:
            result += ('Доступ получен\n')
        else:
            result += ('В доступе отказано\n')

        return result

    def change_rights(self, right, user_name, file_name, main_user):
        result = ''
        if self.can_be_changed(main_user, file_name):
            user_id = int(self.user_list.index(user_name))
            file_id = int(self.file_list.index(file_name))
            self.set_right(user_id, file_id, right)
            result += ('Права успешно сменены\n')
        else: 
            result += ('Нет прав для смены прав\n')
        return result

    def show_access_level(self, userName):
        result = ''
        user_id = self.user_list.index(userName)
        result += 'Уровень доступа для пользователя: ' + userName +'\n'
        for i in range(len(self.file_list)):
            result += 'Для ' + self.file_list[i] + ': '
            result += self.access_matrix[user_id][i] + '\n'
        return result
                

file1 = 'Файл1'
file2 = 'Файл2'
file3 = 'Файл3'

file_array = [file1, file2, file3]

user1 = 'Админчик'
user2 = 'Юзверь1'
user3 = 'Юзверь2'
user4 = 'Юзверь3'
user5 = 'Юзверь4'
user6 = 'Гост1'
user7 = 'Гост2'
user8 = 'Гост3'

user_array = [user1, user2, user3, user4, user5, user6, user7, user8]

def init_matrix(users, files):
    matrix = []
    for i in range(len(users)):
        matrix.append(['Нет прав']*len(files))
    return matrix

matrix = init_matrix(user_array, file_array)

def create_matrix(matrix):
    for i in range((len(matrix))):
        for j in range(len(matrix[i])):
            matrix[i][j] = random.choice(access_variable)
    admin_id = user_array.index('Админчик')
    for i in range(len(matrix[admin_id])):
        matrix[admin_id][i] = access_variable[len(access_variable)-1]

create_matrix(matrix)

matrix_of_access = AccessMatrix(matrix, user_array, file_array)
[matrix_of_access.show_access_level(i) for i in user_array]

def showAllFiles(sender, app_data):
    with dpg.window(autosize=True):
        dpg.add_text(matrix_of_access.show_access_level(dpg.get_value('newUserName')))

def getAccess(sender, app_data):
    with dpg.window(autosize=True):
        dpg.add_text(matrix_of_access.get_access_to_file(dpg.get_value('newUserName'),
                                                         dpg.get_value('fileName'), 
                                                         dpg.get_value('command')))

def getAccessToFile(sender, app_data):
    with dpg.window(label='Получить доступ к файлу',autosize=True):
        dpg.add_input_text(label='Имя файла', tag='fileName')
        dpg.add_input_text(label='Команда', tag='command')
        dpg.add_button(label='Выполнить', callback=getAccess)

def change(sender, app_data):
    with dpg.window(autosize=True):
        dpg.add_text(matrix_of_access.change_rights(dpg.get_value('accessLevel'), 
                                                    dpg.get_value('user'), 
                                                    dpg.get_value('file'), 
                                                    dpg.get_value('newUserName')))

def changeRights(sender, app_data):
    with dpg.window(label='Изменить права пользователя',autosize=True):
        dpg.add_input_text(label='Имя пользователя', default_value='', tag='user')
        dpg.add_input_text(label='Имя файла', default_value='', tag='file')
        dpg.add_input_text(label='Новый уровень доступа', default_value='', tag='accessLevel')
        dpg.add_button(label='Выполнить', callback=change)
        

def login(sender, app_data):
    with dpg.window(autosize=True):
        dpg.add_button(label='Просмотреть уровень доступа ко всем файлам', callback=showAllFiles)
        dpg.add_button(label='Получить доступ к файлу', callback=getAccessToFile)
        dpg.add_button(label='Изменить права другого пользователя', callback=changeRights)


dpg.create_context()

with dpg.font_registry():
    with dpg.font("my_font.ttf", 25, default_font=True, tag="Default font") as f:
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)

# Создать окно с разрешением 2560*1600
with dpg.window(tag = 'Main', autosize=True):
    dpg.add_input_text(label="Имя пользователя", default_value="", tag='newUserName')
    btn = dpg.add_button(label='Войти')
    dpg.set_item_callback(btn, login)
    
dpg.bind_font('Default font')
dpg.create_viewport(title='Модель безопасности', width=900, height=540)
dpg.setup_dearpygui()
dpg.set_primary_window('Main', True)
dpg.show_viewport()
dpg.start_dearpygui()

dpg.destroy_context()
