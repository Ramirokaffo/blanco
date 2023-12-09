from datetime import datetime

import MySQLdb
import mysql

from DATA.DataBase.DBTableName import DBTableName
from DATA.Enumeration.UserRoleEnum import UserRoleEnum
from DATA.SettingClass.BaseUser import BaseUser
from DATA.DataBase.DBManager import connect_to_db


class Staff(BaseUser):
    my_db = connect_to_db()
    current_staff = None

    def __init__(self, id: int = None, username: str = None, firstname: str = None, lastname: str = None,
                 phone_number: str = None, email: str = None, delete_at: datetime = None, create_at: datetime = None,
                 role: str = None, password: str = None, gender: str = None, profil: str = None, is_active: int = None):
        super().__init__(id, firstname, lastname, phone_number, create_at, delete_at, email)
        self.profil: str = profil
        self.gender: str = gender
        self.username: str = username
        self.password: str = password
        self.role: str = role
        self.is_active = is_active
        self.table_name: str = DBTableName.staff
        self.my_map = {}

    def __eq__(self, other):
        return other.id == self.id

    def to_map(self):
        self.my_map["id"] = self.id
        self.my_map["firstname"] = self.firstname
        self.my_map["lastname"] = self.lastname
        self.my_map["username"] = self.username
        self.my_map["phone_number"] = self.phone_number
        self.my_map["create_at"] = self.create_at
        self.my_map["delete_at"] = self.delete_at
        self.my_map["email"] = self.email
        self.my_map["profil"] = self.profil
        self.my_map["is_active"] = self.is_active
        self.my_map["gender"] = self.gender
        self.my_map["password"] = self.password
        self.my_map["role"] = self.role
        return self.my_map

    def save_to_db(self):
        with connect_to_db() as bd_connection:
            with bd_connection.cursor(dictionary=True) as my_cursor:
                my_cursor.execute("INSERT INTO staff (firstname, lastname, username, is_active, "
                                  "phone_number, email, role, gender, profil, password) "
                                  "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, sha(%s))",
                                  [self.firstname, self.lastname, self.username, self.is_active if self.is_active is not None else False,
                                   self.phone_number, self.email, self.role if self.role is not None else UserRoleEnum.SELLER,
                                   self.gender, self.profil, self.password])
                bd_connection.commit()
                return my_cursor.lastrowid

    def update(self, return_map: bool = False):
        if not self.id:
            raise Exception("Id Not Provide")
        query = ""
        params = []
        if self.firstname:
            query += "firstname = %s "
            params.append(self.firstname)
        if self.lastname:
            query += ", lastname = %s "
            params.append(self.lastname)
        if self.username:
            query += ", username = %s "
            params.append(self.username)
        if self.phone_number:
            query += ", phone_number = %s "
            params.append(self.phone_number)
        if self.email:
            query += ", email = %s "
            params.append(self.email)
        if self.role:
            query += ", role = %s "
            params.append(self.role)
        if self.gender:
            query += ", gender = %s "
            params.append(self.gender)
        if self.profil:
            query += ", profil = %s "
            params.append(self.profil)
        if self.password:
            query += ", password = sha(%s) "
            params.append(self.password)
        if query:
            query += f"WHERE id = {self.id};"
        else:
            return self if not return_map else self.to_map()
        if query.startswith(","):
            query = query.lstrip(",")
        try:
            with connect_to_db() as bd_connection:
                with bd_connection.cursor() as my_cursor:
                    my_cursor.execute(f"UPDATE {self.table_name} SET " + query, params)
        except MySQLdb as e:
            raise e
        return self if not return_map else self.to_map()

    def get_last(self, return_map: bool = False):
        with connect_to_db() as bd_connection:
            with bd_connection.cursor(dictionary=True) as my_cursor:
                my_cursor.execute(f"SELECT * FROM {self.table_name} WHERE id = "
                                  f"(SELECT max(id) FROM {self.table_name}) AND delete_at IS NULL;")
                result = my_cursor.fetchone()
                return Staff.from_map(result) if not return_map else result

    def get_last_as_map(self):
        return self.get_last(return_map=True)

    @classmethod
    def from_map(cls, staff_map: dict):
        return None if staff_map is None else Staff(
            id=staff_map.get("id"),
            username=staff_map.get("username"),
            lastname=staff_map.get("lastname"),
            firstname=staff_map.get("firstname"),
            email=staff_map.get("email"),
            password=staff_map.get("password"),
            is_active=staff_map.get("is_active"),
            role=staff_map.get("role"),
            gender=staff_map.get("gender"),
            profil=staff_map.get("profil"),
            create_at=staff_map.get("create_at"),
            delete_at=staff_map.get("delete_at"),
            phone_number=staff_map.get("phone_number"))

    def login(self, username: str, password: str, return_map: bool = False, just_active: bool = True):
        with connect_to_db() as bd_connection:
            with bd_connection.cursor(dictionary=True) as my_cursor:
                my_cursor.execute(
                f'''SELECT * FROM {self.table_name} WHERE username = %s AND password = sha(%s) AND delete_at IS NULL {"AND is_active = '1'" 
                if  not just_active else "" };''',
                [username, password])
                expected_taff = my_cursor.fetchone()
                return Staff.from_map(expected_taff) if not return_map else expected_taff

    def get_by_id(self, line_id: int = None, return_map: bool = False, just_active: bool = True):
        return self.get_by_column_name(column_name="id", return_map=return_map, just_active=just_active,
                                       value=self.id if line_id is None else line_id)

    def get_by_first_name(self, first_name: str = None, return_map: bool = False, just_active: bool = True):
        return self.get_by_column_name(column_name="first_name", return_map=return_map, just_active=just_active, value=first_name)

    def get_by_username_name(self, username: str = None, return_map: bool = False, just_active: bool = True):
        return self.get_by_column_name(column_name="username", return_map=return_map, just_active=just_active, value=username)

    def get_by_column_name(self, column_name: str, value: any, return_map: bool = False, just_active: bool = True):
        with connect_to_db() as bd_connection:
            with bd_connection.cursor(dictionary=True) as my_cursor:
                my_cursor.execute(
                f'''SELECT * FROM {self.table_name} WHERE {column_name} = %s AND delete_at IS NULL {"AND is_active = '1'" 
                if just_active else "" };''', [value])
                result = my_cursor.fetchone()
                return Staff.from_map(result) if not return_map else result

    def get_all(self, return_map: bool = False, just_active: bool = True):
        with connect_to_db() as bd_connection:
            with bd_connection.cursor(dictionary=True) as my_cursor:
                my_cursor.execute(f'''SELECT * FROM {self.table_name} WHERE delete_at IS NULL {"AND is_active = '1'" 
                if just_active else "" };''')
                return [Staff.from_map(result) if not return_map else result for result in my_cursor.fetchall()]

