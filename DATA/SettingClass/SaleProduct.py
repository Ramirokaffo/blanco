from datetime import date

from DATA.DataBase.DBManager import connect_to_db
from DATA.DataBase.DBTableName import DBTableName
from DATA.SettingClass.Product import Product
from DATA.SettingClass.Sale import Sale
from DATA.SettingClass.Supply import Supply


class SaleProduct:
    my_db = connect_to_db()
    table_name = DBTableName.sale_product

    def __init__(self, id: int = None, product_count: int = None, unit_price: float = None, unit_coast: float = None,
                 supply: Supply = None, sale: Sale = None):
        self.id = id
        self.product_count = product_count
        self.unit_price = unit_price
        self.unit_coast = unit_coast
        self.supply = supply
        self.sale = sale

    def save_to_db(self) -> int:
        with connect_to_db() as bd_connection:
            with bd_connection.cursor(dictionary=True) as my_cursor:
                my_cursor.execute(
                    f"INSERT INTO {self.table_name} (product_count, unit_price, unit_coast, supply_id, sale_id) "
                    "VALUES (%s, %s, %s, %s, %s);",
                    [self.product_count, self.unit_price, self.unit_coast, self.supply.id, self.sale.id])
                bd_connection.commit()
                return my_cursor.lastrowid

    @staticmethod
    def save_many_to_db(list_sale_product) -> tuple[int]:
        list_sale_product: list[SaleProduct] = list_sale_product
        with connect_to_db() as bd_connection:
            with bd_connection.cursor() as my_cursor:
                my_cursor.executemany(f"INSERT INTO {SaleProduct.table_name} (product_count, unit_price, unit_coast, supply_id, "
                                      f"sale_id) VALUES (%s, %s, %s, %s, %s);", [(sale_product.product_count,
                                                                                  sale_product.unit_price,
                                                                                  sale_product.unit_coast,
                                                                                  sale_product.supply.id,
                                                                                  sale_product.sale.id)
                                                                                 for sale_product in list_sale_product])
                bd_connection.commit()
                return tuple(range(my_cursor.lastrowid, my_cursor.lastrowid + my_cursor.rowcount))

    @classmethod
    def from_map(cls, sale_product_map: dict):
        return None if sale_product_map is None else SaleProduct(id=sale_product_map["id"],
                           product_count=sale_product_map["product_count"],
                           unit_price=sale_product_map["unit_price"],
                           unit_coast=sale_product_map["unit_coast"],
                           sale=Sale(id=sale_product_map["sale_id"]),
                           supply=Supply(id=sale_product_map["supply_id"]))

    @staticmethod
    def get_sale_product_sale_with_id(sale_id: int = None):
        with connect_to_db() as bd_connection:
            with bd_connection.cursor(dictionary=True) as my_cursor:
                my_cursor.execute(f"SELECT * FROM {SaleProduct.table_name} WHERE sale_id = %s;",
                                  [sale_id])
                return [SaleProduct.from_map(sale_product) for sale_product in my_cursor.fetchall()]

    @staticmethod
    def get_by_id(sale_product_id: int = None):
        with connect_to_db() as bd_connection:
            with bd_connection.cursor(dictionary=True) as my_cursor:
                my_cursor.execute(f"SELECT * FROM {SaleProduct.table_name} WHERE id = %s;",
                                  [sale_product_id])
                return SaleProduct.from_map(my_cursor.fetchone())

    @staticmethod
    def get_by_sale_id(sale_id: int = None, return_map: bool = False):
        with connect_to_db() as bd_connection:
            with bd_connection.cursor(dictionary=True) as my_cursor:
                my_cursor.execute(f"SELECT * FROM {SaleProduct.table_name} "
                                f"LEFT JOIN {DBTableName.sale} ON {SaleProduct.table_name}.sale_id = {DBTableName.sale}.id"
                                  f" WHERE {DBTableName.sale}.id = %s;",
                                  [sale_id])
                results = my_cursor.fetchall()
                return [SaleProduct.from_map(result) if not return_map else result for result in results]

    @staticmethod
    def get_last_product_sale_price(product_id: int, limit: int = 10):
        with connect_to_db() as bd_connection:
            with bd_connection.cursor(dictionary=True) as my_cursor:
                my_cursor.execute(f"SELECT DISTINCT {SaleProduct.table_name}.unit_price AS product_sale_price FROM {SaleProduct.table_name} "
                                  f"LEFT JOIN {DBTableName.supply} ON {SaleProduct.table_name}.supply_id = {DBTableName.supply}.id "
                                  f"LEFT JOIN {DBTableName.product} ON {DBTableName.supply}.product_id = "
                                  f"{DBTableName.product}.id WHERE product_id = %s "
                                  f"ORDER BY {SaleProduct.table_name}.id DESC LIMIT %s;", [product_id, limit])
                result = my_cursor.fetchall()
                return [item["product_sale_price"] for item in result]

    def load_supply(self):
        self.supply = Supply().get_by_id(self.supply.id)
        return self.supply

    def delete_last_permanently(self, limit: int = 1):
        with connect_to_db() as bd_connection:
            with bd_connection.cursor(dictionary=True) as my_cursor:
                my_cursor.execute(f"DELETE FROM {self.table_name} ORDER BY id DESC LIMIT %s;", [limit])
                bd_connection.commit()
                return True

    def delete_permanently(self, sale_product_id: int = None):
        with connect_to_db() as bd_connection:
            with bd_connection.cursor(dictionary=True) as my_cursor:
                my_cursor.execute(f"DELETE FROM {self.table_name} WHERE (`id` = %s);",
                                  [self.id if sale_product_id is None else sale_product_id])
                bd_connection.commit()
                return True

    def delete_range_permanently(self, id_list: tuple[int]):
        with connect_to_db() as bd_connection:
            with bd_connection.cursor(dictionary=True) as my_cursor:
                my_cursor.execute(f"DELETE FROM {self.table_name} WHERE id IN ({', '.join(str(v) for v in id_list)});")
                bd_connection.commit()
                return True

# print(SaleProduct.get_by_sale_id(sale_id=132, return_map=True))
