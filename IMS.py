import json

class Product:
    def __init__(self, product_id, name, quantity, price, reorder_level):
        self.product_id = product_id
        self.name = name
        self.quantity = quantity
        self.price = price
        self.reorder_level = reorder_level
    
    def update_quantity(self, amount):
        self.quantity += amount
    
    def needs_reorder(self):
        return self.quantity <= self.reorder_level

class Supplier:
    def __init__(self, supplier_id, name, contact):
        self.supplier_id = supplier_id
        self.name = name
        self.contact = contact
        self.orders = []
    
    def add_order(self, product_id, quantity):
        self.orders.append({"product_id": product_id, "quantity": quantity})
    
    def get_orders(self):
        return self.orders

class Inventory:
    def __init__(self, filename='inventory_data.json'):
        self.filename = filename
        self.load_data()
    
    def load_data(self):
        try:
            with open(self.filename, 'r') as file:
                data = json.load(file)
                self.products = {pid: Product(**details) for pid, details in data.get("products", {}).items()}
                self.suppliers = {sid: Supplier(**details) for sid, details in data.get("suppliers", {}).items()}
        except FileNotFoundError:
            self.products = {}
            self.suppliers = {}
    
    def save_data(self):
        data = {
            "products": {pid: self.products[pid].__dict__ for pid in self.products},
            "suppliers": {sid: self.suppliers[sid].__dict__ for sid in self.suppliers}
        }
        with open(self.filename, 'w') as file:
            json.dump(data, file, indent=4)
    
    def add_product(self, product_id, name, quantity, price, reorder_level):
        self.products[product_id] = Product(product_id, name, quantity, price, reorder_level)
        self.save_data()
    
    def update_stock(self, product_id, amount):
        if product_id in self.products:
            self.products[product_id].update_quantity(amount)
            self.save_data()
        else:
            print("Product not found.")
    
    def delete_product(self, product_id):
        if product_id in self.products:
            del self.products[product_id]
            self.save_data()
        else:
            print("Product not found.")
    
    def view_inventory(self):
        for product in self.products.values():
            print(f"{product.name} - Quantity: {product.quantity}, Price: ${product.price}, Needs Reorder: {product.needs_reorder()}")
    
    def add_supplier(self, supplier_id, name, contact):
        self.suppliers[supplier_id] = Supplier(supplier_id, name, contact)
        self.save_data()
    
    def view_suppliers(self):
        for supplier in self.suppliers.values():
            print(f"{supplier.name} - Contact: {supplier.contact}, Orders: {supplier.get_orders()}")

def main():
    inventory = Inventory()
    while True:
        print("\n1. Add Product\n2. Update Stock\n3. Delete Product\n4. View Inventory\n5. Add Supplier\n6. View Suppliers\n7. Exit")
        choice = input("Enter your choice: ")
        
        if choice == '1':
            product_id = input("Enter product ID: ")
            name = input("Enter product name: ")
            quantity = int(input("Enter quantity: "))
            price = float(input("Enter price: "))
            reorder_level = int(input("Enter reorder level: "))
            inventory.add_product(product_id, name, quantity, price, reorder_level)
        elif choice == '2':
            product_id = input("Enter product ID: ")
            amount = int(input("Enter stock change amount: "))
            inventory.update_stock(product_id, amount)
        elif choice == '3':
            product_id = input("Enter product ID to delete: ")
            inventory.delete_product(product_id)
        elif choice == '4':
            inventory.view_inventory()
        elif choice == '5':
            supplier_id = input("Enter supplier ID: ")
            name = input("Enter supplier name: ")
            contact = input("Enter contact details: ")
            inventory.add_supplier(supplier_id, name, contact)
        elif choice == '6':
            inventory.view_suppliers()
        elif choice == '7':
            print("Exiting... Thank you!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
