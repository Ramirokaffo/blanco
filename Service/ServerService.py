import os.path
import signal
import io
from PIL import Image
from flask import Flask, jsonify, request, send_file, abort
import threading

from DATA.SettingClass.Category import Category
from DATA.SettingClass.Daily import Daily
from DATA.SettingClass.Exercise import Exercise
from DATA.SettingClass.Gamme import Gamme
from DATA.SettingClass.GrammageType import GrammageType
from DATA.SettingClass.Inventory import Inventory
from DATA.SettingClass.Product import Product
from DATA.SettingClass.ProductImage import ProductImage
from DATA.SettingClass.Rayon import Rayon
from DATA.SettingClass.SaleProduct import SaleProduct
from DATA.SettingClass.Staff import Staff
from DATA.SettingClass.Supply import Supply
from Service.ImageService import ImageService
from UI.Home.Vente.VentePage import VentePage

app = Flask(__name__)


def check_user(f):
    def decorated_function(*args, **kwargs):
        user_id = request.headers.get("userId")
        if not user_id:
            return abort(400, "Utilisateur non identififé")
        expected_user = Staff().get_by_id(line_id=int(user_id))
        if expected_user is None:
            return abort(403, "L'utilisateur n'existe pas")
        return f(*args, **kwargs)

    return decorated_function


class ServerService:
    qr_code_path = ""
    server_base_url = ""

    def __init__(self):
        self.port = 9090
        pass

    @staticmethod
    @app.get("/login/<string:login>/<string:password>")
    def login(login, password):
        user = Staff().login(username=login, password=password, return_map=True, just_active=False)
        if user:
            return jsonify({"status": 1, "user": user})
        else:
            return jsonify({"status": 0})

    @staticmethod
    @app.get("/image/<string:folder>/<string:image>")
    @check_user
    def get_image(folder, image):
        image_relatif_path = os.path.join("image_app", folder, image)
        image_path = os.path.join(os.getcwd().split("blanco")[0], "blanco", image_relatif_path)
        img = Image.open(image_path)
        img_io = io.BytesIO()
        img.save(img_io, "JPEG")
        img_io.seek(0)
        return send_file(img_io, mimetype="image/jpeg")

    @staticmethod
    def add_images_url(product_image_as_map: list[dict], folder: str) -> list[dict]:
        for image in product_image_as_map:
            image["url"] = ServerService.get_image_url(image.get("path"), folder)
        return product_image_as_map

    @staticmethod
    def get_image_url(image_relatif_path: str, folder: str):
        return ServerService.server_base_url + "/image/" + folder + "/" + image_relatif_path

    @staticmethod
    @app.get("/get_user_by_id/<int:user_id>")
    def get_user_by_id(user_id):
        return jsonify(Staff().get_by_id(line_id=user_id, return_map=True, just_active=False))

    @staticmethod
    @check_user
    @app.get("/get_product_list/<int:page>/<int:count>")
    def get_product_list(page, count):
        return jsonify(Product().get_product_list(count=count, page=page, return_map=True))

    @staticmethod
    @check_user
    @app.get("/search_product")
    def search_product():
        data = request.values.to_dict()
        search_input = data.get("search_input")
        page = int(data.get("page"))
        count = int(data.get("count"))
        return jsonify(Product().get_search_result(search_input=search_input, count=count, page=page, return_map=True))

    @staticmethod
    @app.get("/get_product_by_id/<int:product_id>")
    def get_product_by_id(product_id):
        expected_product = Product().get_by_id(product_id=product_id)
        product_images = ServerService.add_images_url(ProductImage().get_by_product_id(
            product_id=product_id, return_map=True), folder="product")
        if expected_product:
            full_product = expected_product.to_map(load_relation=True)
            full_product["images"] = product_images
            return jsonify(full_product)

    @staticmethod
    @app.get("/get_staff_by_login/<string:login>")
    def get_staff_by_login(login):
        expected_product = Staff().get_by_username_name(username=login, return_map=True)
        if expected_product:
            return jsonify({"user": expected_product, "status": 1})
        else:
            return jsonify({"status": 0})

    @staticmethod
    @check_user
    @app.get("/get_product_by_code/<string:product_code>")
    def get_product_by_code(product_code):
        data = request.values.to_dict()
        return_all = data.get("return_all")
        expected_product = Product().get_by_code(product_code=product_code)
        if expected_product:
            if return_all == "1":
                return jsonify(ServerService.get_product_by_id(expected_product.id))
            else:
                return jsonify(expected_product.to_map(load_relation=True) if expected_product else None)
        return jsonify(None)

    @staticmethod
    @check_user
    @app.get("/get_product_by_name/<string:product_name>")
    def get_product_by_name(product_name):
        expected_product = Product().find_product_by_name(name=product_name)
        return jsonify(expected_product.to_map(load_relation=True) if expected_product else None)

    @staticmethod
    @check_user
    @app.get("/get_category")
    def get_category():
        return jsonify(Category().get_all(return_map=True))

    @staticmethod
    @check_user
    @app.get("/get_rayon")
    def get_rayon():
        return jsonify(Rayon().get_all(return_map=True))

    @staticmethod
    @check_user
    @app.get("/get_gamme")
    def get_gamme():
        return jsonify(Gamme().get_all(return_map=True))

    @staticmethod
    @check_user
    @app.get("/get_grammage_type")
    def get_grammage_type():
        return jsonify(GrammageType().get_all(return_map=True))

    @staticmethod
    @app.post("/create_user")
    def create_user():
        user = request.json
        staff = Staff.from_map(user)
        staff.save_to_db()
        return jsonify({"status": 1, "user": staff.get_last_as_map()})

    @staticmethod
    @check_user
    @app.post("/create_inventory")
    def create_inventory():
        user_id = request.headers.get("userId")
        staff = Staff().get_by_id(line_id=int(user_id))
        inventory = request.json
        create_inventory = Inventory.from_map(inventory)
        create_inventory.saver_staff = staff
        create_inventory.daily = Exercise.get_current_exercise()
        created_inventory_id = create_inventory.save_to_db()
        return jsonify({"status": 1, "inventory": create_inventory.get_by_id(id=created_inventory_id, return_map=True)})

    @staticmethod
    @check_user
    @app.post("/sale")
    def sale():
        data = request.values.to_dict()
        current_sale = data.get("current_sale") == "1"
        if current_sale:
            right_page = VentePage.get_shown_page()
            if not right_page:
                right_page = VentePage.last_shown
                if not right_page:
                    right_page = VentePage.list_sale_page[0].add_tab()
        else:
            right_page = VentePage.list_sale_page[0].add_tab()
        data = request.json
        for sale_product_data in data["sale_products"]:
            current_supply: Supply = Supply().find_right_product_supply(product_id=sale_product_data["product_id"])
            if current_supply:
                product = current_supply.load_product()
            else:
                product = Product().get_by_id(product_id=sale_product_data["product_id"])
                current_supply = Supply(product=product, unit_coast=0)
            if not right_page.has_this_product(product):
                right_page.fill_tab_line_with_sale_product(
                    [SaleProduct(supply=current_supply,
                                 product_count=sale_product_data["product_count"],
                                 unit_price=sale_product_data["unit_price"],
                                 unit_coast=current_supply.unit_coast if current_supply else 0)])
        return jsonify({"status": 1})

    @staticmethod
    @check_user
    @app.post("/update_user")
    def update_user():
        user = request.json
        staff = Staff.from_map(user)
        staff.update()
        staff.my_db.commit()
        return jsonify({"status": 1, "user": staff.get_last_as_map()})

    @staticmethod
    @check_user
    @app.post("/create_product")
    def create_product():
        expected_user = Staff().get_by_id(request.headers.get("userId"))
        query_params = request.values.to_dict()
        data = request.form.to_dict()
        images = request.files.getlist("images")
        product_count = data.get("stock")
        is_image_save = False
        is_supply_save = False
        is_product_save = False
        saved_product_image_count = 0
        try:
            Product.from_map(data).save_to_db()
            is_product_save = True
            product = Product().get_last()
            for file in images:
                ProductImage(path=file.filename, description=file.headers.get("description"),
                             product=product).create()
                saved_product_image_count += 1
                file.save(ImageService.get_saved_path(file.filename, "product"))
            is_image_save = True
            Supply(product=product, saver_staff=expected_user, product_count=product_count,
                   product_count_rest=product_count, unit_price=data.get("unit_price"),
                   daily=Daily.get_current_daily()).save_to_db()
            is_supply_save = True
            if query_params.get("inventory_mode") == "1":
                Inventory(valid_product_count=product_count, invalid_product_count=0,
                          exercise=Exercise.get_current_exercise(), product=product,
                          saver_staff=expected_user).save_to_db()
        except:
            if is_product_save:
                Product().delete_last_permanently()
            if is_image_save:
                ProductImage().delete_last_permanently(limit=saved_product_image_count)
            if is_supply_save:
                Supply().delete_last_permanently()
            raise Exception()
        return jsonify({"status": 1, "product": product.to_map(load_relation=True)})

    @staticmethod
    @app.get("/test_connexion")
    def test_connection():
        return jsonify({"status": 1})

    def start_command(self, ip):
        ServerService.server_base_url = f"http://{ip}:{self.port}"
        app.run(host=ip, port=self.port)

    def start_server(self, ip):
        server_thread = threading.Thread(target=self.start_command, kwargs={"ip": ip})
        server_thread.start()

    @staticmethod
    def stop_server():
        os.kill(os.getpid(), signal.SIGINT)


# ip = WIFIService.get_local_ip()
#
# ServerService().start_server(ip)
