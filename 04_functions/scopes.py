def serve_chai():
    chai_type = "Masala"  # local scope
    print(f"inside function {chai_type}")


chai_type = "Lemon"
serve_chai()
print(f"outside function {chai_type}")


def chai_counter():
    chai_order = "Lemon"  # Enclosing scope

    def print_order():
        chai_order = "Ginger"
        print("Inner: ", chai_order)

    print_order()
    print("Outer: ", chai_order)


chai_order = "Tulsi"
chai_counter()
print("Global: ", chai_order)
