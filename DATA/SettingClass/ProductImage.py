import os

from DATA.DataBase.DBManager import connect_to_db
from DATA.DataBase.DBTableName import DBTableName
from DATA.SettingClass.Product import Product


class ProductImage:
    """
    Les images des produits
    """
    my_db = connect_to_db()
    table_name: str = DBTableName.product_image

    def __init__(self, id: int = None, path: str = None, description: str = None, product: Product = None,
                 real_path: str = None):
        self.id = id
        self.path = path
        self.real_path = real_path
        self.product = product
        self.description = description

    def get_by_id(self, category_id, return_map: bool = False):
        with connect_to_db() as bd_connection:
            with bd_connection.cursor(dictionary=True) as my_cursor:
                my_cursor.execute(f"SELECT * FROM {self.table_name} WHERE id = %s AND delete_at IS NULL;",
                                  [category_id])
                result = my_cursor.fetchone()
                return ProductImage.from_map(result) if not return_map else result

    def get_all(self, return_map: bool = False):
        with connect_to_db() as bd_connection:
            with bd_connection.cursor(dictionary=True) as my_cursor:
                my_cursor.execute(f"SELECT * FROM {self.table_name} WHERE delete_at IS NULL;")
                return [ProductImage.from_map(result) if not return_map else result for result in my_cursor.fetchall()]

    @classmethod
    def from_map(cls, category_map: dict):
        return None if not category_map else ProductImage(id=category_map.get("id"), path=category_map.get("path"),
                                                      description=category_map.get("description"))

    @staticmethod
    def get_by_product_id(product_id, return_map: bool = False):
        with connect_to_db() as bd_connection:
            with bd_connection.cursor(dictionary=True) as my_cursor:
                my_cursor.execute(f"SELECT * FROM {ProductImage.table_name} WHERE product_id = %s AND delete_at IS NULL;",
                                  [product_id])
                return [ProductImage.from_map(result) if not return_map else result for result in my_cursor.fetchall()]

    def get_last(self, return_map: bool = False):
        with connect_to_db() as bd_connection:
            with bd_connection.cursor(dictionary=True) as my_cursor:
                my_cursor.execute(f"SELECT * FROM {self.table_name} WHERE id = "
                                  f"(SELECT max(id) FROM {self.table_name}) AND delete_at IS NULL;")
                result = my_cursor.fetchone()
                return ProductImage.from_map(result) if not return_map else result

    def load_local_path(self):
        image_relatif_path = os.path.join("image_app", "product", self.path)
        self.real_path = os.path.join(os.getcwd().split("blanco")[0], "blanco", image_relatif_path)
        return self

    def create(self):
        with connect_to_db() as bd_connection:
            with bd_connection.cursor() as my_cursor:
                my_cursor.execute(f"INSERT INTO {self.table_name} (path, description, product_id) VALUES (%s, %s, %s);",
                                  [self.path, self.description, self.product.id])
                bd_connection.commit()
                return my_cursor.lastrowid

    def update(self):
        # assert self.path is not None
        with connect_to_db() as bd_connection:
            with bd_connection.cursor() as my_cursor:
                my_cursor.execute(f'''UPDATE {ProductImage.table_name} SET \
                path = %s {f", description = '{self.description}'" if self.description is not None else "" }  \
                WHERE id = %s;''', [self.path, self.id])
                bd_connection.commit()
                return my_cursor.lastrowid

    def get_path_from_real_path(self):
        self.path = self.real_path.split("/")[-1]
        return self

    @staticmethod
    def save_many_to_db(list_product_image) -> tuple[int]:
        list_product_image: list[ProductImage] = list_product_image
        with connect_to_db() as bd_connection:
            with bd_connection.cursor(dictionary=True) as my_cursor:
                my_cursor.executemany(f"INSERT INTO {ProductImage.table_name} (path, description, product_id) VALUES (%s, %s, %s);",
                                      [(product_image.path, product_image.description, product_image.product.id)
                                                                                 for product_image in list_product_image])
                bd_connection.commit()
                return tuple(range(my_cursor.lastrowid, my_cursor.lastrowid + my_cursor.rowcount))

    def delete_last_permanently(self, limit: int = 1):
        try:
            with connect_to_db() as bd_connection:
                with bd_connection.cursor() as my_cursor:
                    my_cursor.execute(f"DELETE FROM {self.table_name} ORDER BY id DESC LIMIT %s;", [limit])
                    bd_connection.commit()
                    return True
        except:
            return False

    def delete_permanently(self, product_image_id: int = None):
        with connect_to_db() as bd_connection:
            with bd_connection.cursor(dictionary=True) as my_cursor:
                my_cursor.execute(f"DELETE FROM {self.table_name} WHERE (`id` = %s);",
                                  [self.id if product_image_id is None else product_image_id])
                bd_connection.commit()
                return True

    def delete_range_permanently(self, id_list: tuple[int]):
        with connect_to_db() as bd_connection:
            with bd_connection.cursor(dictionary=True) as my_cursor:
                my_cursor.execute(f"DELETE FROM {self.table_name} WHERE id IN ({', '.join(str(v) for v in id_list)});")
                bd_connection.commit()
                return True
