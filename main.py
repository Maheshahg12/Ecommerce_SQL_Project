
from database_handler import DatabaseHandler
from tabulate import tabulate
import os

DB_FILE = "ecommerce.db"


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def pause():
    input("\nPress Enter to continue...")


def print_products(rows):
    if not rows:
        print("No products found.")
        return
    headers = ["ID", "Name", "Price", "Quantity", "CreatedAt"]
    print(tabulate(rows, headers=headers, tablefmt="pretty"))


def main():
    db = DatabaseHandler(DB_FILE)
    db.initialize_db()

    while True:
        clear()
        print("====== Product Management System ======")
        print("1. Add Product")
        print("2. View Products")
        print("3. Search Product")
        print("4. Filter by Price")
        print("5. Update Product")
        print("6. Delete Product")
        print("7. Exit")
        print("=======================================")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            name = input("Product name: ").strip()
            price = input("Price: ").strip()
            qty = input("Quantity: ").strip()
            try:
                pid = db.add_product(name, float(price), int(qty))
                print(f"✅ Product added with ID {pid}")
            except Exception as e:
                print(f"❌ Error adding product: {e}")
            pause()

        elif choice == "2":
            rows = db.get_products()
            print_products(rows)
            pause()

        elif choice == "3":
            term = input("Search term: ")
            rows = db.find_products_by_name(term)
            print_products(rows)
            pause()

        elif choice == "4":
            min_p = input("Min price (leave blank for none): ").strip()
            max_p = input("Max price (leave blank for none): ").strip()
            min_p = float(min_p) if min_p else None
            max_p = float(max_p) if max_p else None
            rows = db.filter_products(min_p, max_p)
            print_products(rows)
            pause()

        elif choice == "5":
            pid = input("Enter product ID to update: ").strip()
            product = db.get_product(int(pid))
            if not product:
                print("Product not found.")
                pause()
                continue
            print("Current:", product)
            new_name = input("New name (leave blank to keep): ").strip() or None
            new_price = input("New price (leave blank to keep): ").strip() or None
            new_qty = input("New quantity (leave blank to keep): ").strip() or None
            try:
                ok = db.update_product(int(pid), new_name, float(new_price) if new_price else None, int(new_qty) if new_qty else None)
                print("✅ Updated." if ok else "❌ No changes made.")
            except Exception as e:
                print(f"❌ Error updating: {e}")
            pause()

        elif choice == "6":
            pid = input("Enter product ID to delete: ").strip()
            confirm = input("Type DELETE to confirm: ")
            if confirm == "DELETE":
                ok = db.delete_product(int(pid))
                print("🗑 Deleted." if ok else "❌ Product not found.")
            else:
                print("Deletion cancelled.")
            pause()

        elif choice == "7":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Try again.")
            pause()


if __name__ == "__main__":
    main()