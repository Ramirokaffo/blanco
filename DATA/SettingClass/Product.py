from datetime import datetime

from DATA.DataBase.DBManager import connect_to_db
from DATA.DataBase.DBTableName import DBTableName
from DATA.SettingClass.Category import Category
from DATA.SettingClass.Gamme import Gamme
from DATA.SettingClass.GrammageType import GrammageType
from DATA.SettingClass.Rayon import Rayon


class Product:
    """
    La class qui manipule les produits
    """
    # my_db = connect_to_db()
    table_name: str = DBTableName.product

    def __init__(self, id: int = None, code: str = None, name: str = None, description: str = None, brand: str = None,
                 color: str = None, max_salable_price: int = None, stock: int = None,
                 stock_limit: int = None, exp_alert_period: int = None, grammage: float = None, is_price_reducible=None,
                 category: Category = None, gamme: Gamme = None, grammage_type: GrammageType = None,
                 rayon: Rayon = None, delete_at: datetime = None,
                 create_at: datetime = None):
        self.id = id
        self.code = code
        self.name = name
        self.description = description
        self.brand = brand
        self.color = color
        self.stock_limit = stock_limit
        self.stock = stock
        self.max_salable_price = max_salable_price
        self.exp_alert_period = exp_alert_period
        self.delete_at = delete_at
        self.create_at = create_at
        self.grammage = grammage
        self.category = category
        self.gamme = gamme
        self.rayon = rayon
        self.my_map = {}
        self.grammage_type = grammage_type
        self.is_price_reducible = is_price_reducible
        # self.

    def to_map(self, load_relation: bool = False, load_all: bool = False):
        self.my_map["id"] = self.id
        self.my_map["code"] = self.code
        self.my_map["name"] = self.name
        self.my_map["description"] = self.description
        self.my_map["grammage"] = self.grammage
        self.my_map["brand"] = self.brand
        self.my_map["color"] = self.color
        self.my_map["stock_limit"] = self.stock_limit
        self.my_map["max_salable_price"] = self.max_salable_price
        self.my_map["is_price_reducible"] = self.is_price_reducible
        self.my_map["exp_alert_period"] = self.exp_alert_period
        self.my_map["delete_at"] = self.delete_at
        self.my_map["create_at"] = self.create_at
        self.my_map["stock"] = self.stock
        if load_relation:
            self.my_map["right_supply"] = self.get_right_supply_as_map()
            return self.load_all_one_relation(return_map=True)
        else:
            self.my_map["category_id"] = None if self.category else self.category.id
            self.my_map["gamme_id"] = None if self.gamme else self.gamme.id
            self.my_map["grammage_type_id"] = None if self.grammage_type else self.grammage_type.id
            self.my_map["rayon_id"] = None if self.rayon else self.rayon.id
            return self.my_map

    def save_to_db(self) -> int:
        with connect_to_db() as bd_connection:
            with bd_connection.cursor() as my_cursor:
                my_cursor.execute(
                    f"INSERT INTO {self.table_name} (code, name, description, brand, color, stock_limit, exp_alert_period, "
                    "grammage, is_price_reducible, category_id, gamme_id, grammage_type_id, rayon_id, max_salable_price) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);",
                    [self.code.lstrip().rstrip(), self.name.lstrip().rstrip(), self.description.lstrip().rstrip(),
                     self.brand, self.color, self.stock_limit,
                     self.exp_alert_period, self.grammage, self.is_price_reducible, self.category.id if self.category
                     else None, self.gamme.id if self.gamme else None,
                     self.grammage_type.id, self.rayon.id, self.max_salable_price])
                bd_connection.commit()
                return my_cursor.lastrowid

    @staticmethod
    def find_sale_product(name: str) -> list[str | None]:
        with connect_to_db() as bd_connection:
            with bd_connection.cursor() as my_cursor:
                my_cursor.execute(f"SELECT name FROM {Product.table_name} WHERE name LIKE '%{name}%' AND delete_at IS NULL;")
                return [product[0] for product in my_cursor.fetchall()]

    @staticmethod
    def find_product_by_name(name: str, return_map: bool = False):
        with connect_to_db() as bd_connection:
            with bd_connection.cursor(dictionary=True) as my_cursor:
                my_cursor.execute(f"SELECT * FROM {Product.table_name} LEFT JOIN (SELECT {DBTableName.supply}.product_id, "
                                  f"SUM({DBTableName.supply}.product_count_rest) AS stock FROM {DBTableName.supply} "
                                  f"GROUP BY {DBTableName.supply}.product_id) "
                                  f"as {DBTableName.supply} ON {DBTableName.supply}.product_id = "
                                  f"{Product.table_name}.id WHERE UPPER({Product.table_name}.name) = UPPER(%s) AND "
                                  f"{Product.table_name}.delete_at IS NULL;", [name])
                product = my_cursor.fetchone()
                return Product.from_map(product) if not return_map else product

    @staticmethod
    def get_by_id(product_id: int = None, return_map: bool = False):
        with connect_to_db() as bd_connection:
            with bd_connection.cursor(dictionary=True) as my_cursor:
                my_cursor.execute(f"SELECT * FROM {Product.table_name} LEFT JOIN (SELECT {DBTableName.supply}.product_id, "
                                  f"SUM({DBTableName.supply}.product_count_rest) AS stock FROM {DBTableName.supply} "
                                  f"GROUP BY {DBTableName.supply}.product_id) "
                                  f"as {DBTableName.supply} ON {DBTableName.supply}.product_id = "
                                  f"{Product.table_name}.id WHERE {Product.table_name}.id = %s AND {Product.table_name}.delete_at IS NULL;",
                                  [product_id])
                product = my_cursor.fetchone()
                return Product.from_map(product) if not return_map else product

    def get_last(self, return_map: bool = False):
        with connect_to_db() as bd_connection:
            with bd_connection.cursor(dictionary=True) as my_cursor:
                my_cursor.execute(f"SELECT * FROM {self.table_name} LEFT JOIN (SELECT {DBTableName.supply}.product_id, "
                                  f"SUM({DBTableName.supply}.product_count_rest) AS stock FROM {DBTableName.supply} "
                                  f"GROUP BY {DBTableName.supply}.product_id) "
                                  f"AS {DBTableName.supply} ON {DBTableName.supply}.product_id = "
                                  f"{self.table_name}.id WHERE {self.table_name}.delete_at IS NULL "
                                  f"ORDER BY {self.table_name}.id DESC LIMIT 1;")
                product = my_cursor.fetchone()
                return Product.from_map(product) if not return_map else product

    @staticmethod
    def get_by_code(product_code: str = None, return_map: bool = False):
        with connect_to_db() as bd_connection:
            with bd_connection.cursor(dictionary=True) as my_cursor:
                my_cursor.execute(f"SELECT * FROM {Product.table_name} LEFT JOIN (SELECT {DBTableName.supply}.product_id, "
                                  f"SUM({DBTableName.supply}.product_count_rest) AS stock FROM {DBTableName.supply} "
                                  f"GROUP BY {DBTableName.supply}.product_id) "
                                  f"as {DBTableName.supply} ON {DBTableName.supply}.product_id = "
                                  f"{Product.table_name}.id WHERE UPPER({Product.table_name}.code) = UPPER(%s) AND "
                                  f"{Product.table_name}.delete_at IS NULL;",
                                  [product_code])
                product = my_cursor.fetchone()
                return Product.from_map(product) if not return_map else product

    def get_product_list(self, count: int = 50, page: int = 0, return_map: bool = False):
        with connect_to_db() as bd_connection:
            with bd_connection.cursor(dictionary=True) as my_cursor:
                my_cursor.execute(f"SELECT * FROM {self.table_name} LEFT JOIN (SELECT {DBTableName.supply}.product_id, "
                                  f"SUM({DBTableName.supply}.product_count_rest) AS stock FROM {DBTableName.supply} "
                                  f"GROUP BY {DBTableName.supply}.product_id) "
                                  f"as {DBTableName.supply} ON {DBTableName.supply}.product_id = "
                                  f"{self.table_name}.id WHERE {self.table_name}.delete_at IS NULL LIMIT %s OFFSET %s;",
                                  [count, count * page])
                return [Product.from_map(product) if not return_map else product for product in my_cursor.fetchall()]

    @staticmethod
    def get_product_by_category_name(category_name, count: int = 50, page: int = 0, return_map: bool = False):
        with connect_to_db() as bd_connection:
            with bd_connection.cursor(dictionary=True) as my_cursor:
                my_cursor.execute(f"SELECT * FROM {Product.table_name} "
                                  f"LEFT JOIN (SELECT {DBTableName.supply}.product_id, "
                                  f"SUM({DBTableName.supply}.product_count_rest) AS stock FROM {DBTableName.supply} "
                                  f"GROUP BY {DBTableName.supply}.product_id) "
                                  f"as {DBTableName.supply} ON {DBTableName.supply}.product_id = "
                                  f"{Product.table_name}.id LEFT JOIN (SELECT {Category.table_name}.id, "
                                  f"{Category.table_name}.name FROM "
                                  f"{DBTableName.category}) AS category ON "
                                  f"{DBTableName.category}.id = {Product.table_name}.category_id "
                                  f"WHERE {DBTableName.category}.name = %s AND "
                                  f"{Product.table_name}.delete_at IS NULL LIMIT %s OFFSET %s;",
                                  [category_name, count, count * page])
                return [Product.from_map(product) if not return_map else product for product in my_cursor.fetchall()]

    @staticmethod
    def get_product_count_by_category_name(category_name: str) -> int:
        with connect_to_db() as bd_connection:
            with bd_connection.cursor(dictionary=True) as my_cursor:
                my_cursor.execute(f"SELECT COUNT(*) AS product_count FROM {Product.table_name} "
                                  f" LEFT JOIN (SELECT {Category.table_name}.id, "
                                  f"{Category.table_name}.name FROM "
                                  f"{DBTableName.category}) AS category ON "
                                  f"{DBTableName.category}.id = {Product.table_name}.category_id "
                                  f"WHERE {DBTableName.category}.name = %s AND "
                                  f"{Product.table_name}.delete_at IS NULL;",
                                  [category_name])
                return my_cursor.fetchone()["product_count"]

    def get_search_result(self, search_input: str, count: int = 50, page: int = 0, return_map: bool = False):
        with connect_to_db() as bd_connection:
            with bd_connection.cursor(dictionary=True) as my_cursor:
                my_cursor.execute(f"SELECT * FROM {self.table_name} LEFT JOIN (SELECT {DBTableName.supply}.product_id, "
                                  f"SUM({DBTableName.supply}.product_count_rest) AS stock FROM {DBTableName.supply} "
                                  f"GROUP BY {DBTableName.supply}.product_id) "
                                  f"as {DBTableName.supply} ON {DBTableName.supply}.product_id = {self.table_name}.id "
                                  f"WHERE ({self.table_name}.code LIKE '{search_input}%' OR "
                                  f"{self.table_name}.name LIKE '%{search_input}%' OR "
                                  f"{self.table_name}.description LIKE '%{search_input}%') AND "
                                  f"{self.table_name}.delete_at IS NULL LIMIT %s OFFSET %s;",
                                  [count, count * page])
                return [Product.from_map(product) if not return_map else product for product in my_cursor.fetchall()]

    @staticmethod
    def get_product_with_stock_critic(count: int = 50, page: int = 0, return_map: bool = False):
        with connect_to_db() as bd_connection:
            with bd_connection.cursor(dictionary=True) as my_cursor:
                my_cursor.execute(f"SELECT * FROM {Product.table_name} LEFT JOIN (SELECT {DBTableName.supply}.product_id, "
                                  f"SUM({DBTableName.supply}.product_count_rest) AS stock FROM {DBTableName.supply} "
                                  f"GROUP BY {DBTableName.supply}.product_id) "
                                  f"AS {DBTableName.supply} ON {DBTableName.supply}.product_id = "
                                  f"{Product.table_name}.id WHERE {Product.table_name}.stock_limit >= "
                                  f"{DBTableName.supply}.stock AND {Product.table_name}.delete_at IS NULL "
                                  f"LIMIT %s OFFSET %s;", [count, count * page])
                return [Product.from_map(product) if not return_map else product for product in my_cursor.fetchall()]

    @staticmethod
    def check_type(value, typ: type = int):
        try:
            return typ(value)
        except:
            return None

    @classmethod
    def from_map(cls, data_map: dict):
        return Product(id=Product.check_type(data_map.get("id")),
                       code=data_map.get("code"),
                       name=data_map.get("name"),
                       create_at=data_map.get("create_at"),
                       delete_at=data_map.get("delete_at"),
                       description=data_map.get("description"),
                       stock=data_map.get("stock"),
                       max_salable_price=Product.check_type(data_map.get("max_salable_price"), typ=float),
                       brand=data_map.get("brand"), color=data_map.get("color"),
                       stock_limit=Product.check_type(data_map.get("stock_limit")),
                       exp_alert_period=Product.check_type(data_map.get("exp_alert_period")),
                       grammage=Product.check_type(data_map.get("grammage"), typ=float),
                       is_price_reducible=Product.check_type(data_map.get("is_price_reducible"), typ=bool),
                       rayon=Rayon(id=Product.check_type(data_map.get("rayon_id"))),
                       category=Category(id=Product.check_type(data_map.get("category_id"))),
                       gamme=Gamme(id=Product.check_type(data_map.get("gamme_id"))),
                       grammage_type=GrammageType(id=Product.check_type(data_map.get("grammage_type_id")))) \
            if data_map else None

    def get_stock(self) -> int:
        with connect_to_db() as bd_connection:
            with bd_connection.cursor(dictionary=True) as my_cursor:
                my_cursor.execute(
                    f"SELECT SUM(product_count_rest) as stock FROM {DBTableName.supply} WHERE product_count_rest != '0' AND "
                    f"product_id = %s AND delete_at IS NULL ORDER BY create_at ASC LIMIT 1;",
                    [self.id])
                supply_map = my_cursor.fetchone()
                return supply_map["stock"]

    def get_right_supply_as_map(self):
        with connect_to_db() as bd_connection:
            with bd_connection.cursor(dictionary=True) as my_cursor:
                my_cursor.execute(
                    f"SELECT * FROM {DBTableName.supply} WHERE product_count_rest != '0' AND product_id = %s AND delete_at "
                    f"IS NULL ORDER BY create_at ASC LIMIT 1;",
                    [self.id])
                return my_cursor.fetchone()

    def load_category(self, return_map: bool = False) -> Category | dict:
        if not return_map:
            self.category = Category().get_by_id(category_id=self.category.id)
            return self.category
        self.my_map[DBTableName.category] = Category().get_by_id(category_id=self.category.id, return_map=return_map)
        return self.my_map[DBTableName.category]

    def load_gamme(self, return_map: bool = False) -> Gamme | dict:
        if not return_map:
            self.gamme = Gamme().get_by_id(category_id=self.gamme.id)
            return self.gamme
        self.my_map[DBTableName.gamme] = Gamme().get_by_id(category_id=self.gamme.id, return_map=return_map)
        return self.my_map[DBTableName.gamme]

    def load_grammage_type(self, return_map: bool = False) -> GrammageType | dict:
        if not return_map:
            self.grammage_type = GrammageType().get_by_id(category_id=self.grammage_type.id)
            return self.grammage_type
        self.my_map[DBTableName.grammage_type] = GrammageType().get_by_id(category_id=self.grammage_type.id,
                                                                          return_map=return_map)
        return self.my_map[DBTableName.grammage_type]

    def load_rayon(self, return_map: bool = False) -> Rayon | dict:
        if not return_map:
            self.rayon = Rayon().get_by_id(rayon_id=self.rayon.id)
            return self.rayon
        self.my_map[DBTableName.rayon] = Rayon().get_by_id(rayon_id=self.category.id, return_map=return_map)
        return self.my_map[DBTableName.rayon]

    def load_all_one_relation(self, return_map: bool = False):
        self.load_rayon(return_map=return_map)
        self.load_gamme(return_map=return_map)
        self.load_category(return_map=return_map)
        self.load_grammage_type(return_map=return_map)
        return self.my_map if return_map else self

    def delete_last_permanently(self, limit: int = 1) -> bool:
        with connect_to_db() as bd_connection:
            with bd_connection.cursor() as my_cursor:
                my_cursor.execute(f"DELETE FROM {self.table_name} ORDER BY id DESC LIMIT %s;", [limit])
                bd_connection.commit()
                return True


# for i in Product().get_search_result("RUB", return_map=True):
#     print(i)