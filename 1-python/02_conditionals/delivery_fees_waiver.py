order_amount = int(input("Enter the order amount: "))
delivery_fee = 0 if order_amount > 300 else 30
    
print(f"delivery_fee: {delivery_fee}")