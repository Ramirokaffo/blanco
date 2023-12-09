

class StaffRole:

    def __init__(self, id: int = None, can_sale: bool = None, can_delete_sale: bool = None,
                 can_add_product: bool = None, can_edit_product: bool = None, can_add_user: bool = None,
                 can_delete_product: bool = None, can_delete_user: bool = None):
        self.id = id
        self.can_sale = can_sale
        self.can_delete_sale = can_delete_sale
        self.can_add_product = can_add_product
        self.can_edit_product = can_edit_product
        self.can_add_user = can_add_user
        self.can_delete_product = can_delete_product
        self.can_delete_user = can_delete_user
