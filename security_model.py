import copy as cp
import random

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

    def get_access_to_file(self, file_name, doing):
        user_id = self.user_list.index(active_user)
        file_id = self.file_list.index(file_name)
        right = self.get_access(user_id, file_id)

        if right == 'Полные права':
            print('Доступ получен\n')
        elif doing in right:
            print('Доступ получен\n')
        else:
            print('В доступе отказано\n')

        print()

    def change_rights(self, right, user_name, file_name):
        if self.can_be_changed(active_user, file_name):
            user_id = int(self.user_list.index(user_name))
            file_id = int(self.file_list.index(file_name))
            self.set_right(user_id, file_id, right)
            print('Права успешно сменены\n')
        else: 
            print('Нет прав для смены прав\n')
        print()

    def show_access_level(self, userName):
        user_id = self.user_list.index(userName)
        print('Уровень доступа для пользователя: ',userName)
        for i in range(len(self.file_list)):
            print('Для ',self.file_list[i], end=': ')
            print(self.access_matrix[user_id][i])
        print()

    def menu(self):
        choise = ''
        while choise != '4':
            print('Выберите действие: ')
            print('1. Просмотреть уровни доступа для файла')
            print('2. Получить доступ к файлу')
            print('3. Изменить права другого пользователя')
            print('4. Выбрать другого пользователя')
            print('Введите номер действия: ')
            choise = input()
            if choise == '1':
                self.show_access_level(active_user)
            elif choise == '2':
                print('Введите имя файла:', end=' ')
                fileName = input()
                print('Введите действие:',end=' ')
                doing = input()
                self.get_access_to_file(fileName, doing)
            elif choise == '3':
                print('Введите имя того, кому хотите сменить права доступа:',end=' ')
                userName = input()
                print('Введите название файла:', end=' ')
                fileName = input()
                print('Какие права вы хотите присвоить:', end=' ')
                newRights = input()
                self.change_rights(newRights, userName, fileName)
        print()
                

file1 = 'file1'
file2 = 'file2'
file3 = 'file3'

file_array = [file1, file2, file3]

user1 = 'Admin'
user2 = 'User'
user3 = 'Guest'

user_array = [user1, user2, user3]

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
    admin_id = user_array.index('Admin')
    print(admin_id)
    for i in range(len(matrix[admin_id])):
        matrix[admin_id][i] = access_variable[len(access_variable)-1]

create_matrix(matrix)

matrix_of_access = AccessMatrix(matrix, user_array, file_array)
[matrix_of_access.show_access_level(i) for i in user_array]

choise = ''
while choise!='0':
    userName = ''
    print('1. Войти в пользователя')
    print('0. Завершить')
    choise = input()
    if choise == '1':
        print('Введите имя пользователя:', end=' ')
        userName = input()
        matrix_of_access.active_user(str(userName))
        matrix_of_access.menu()
