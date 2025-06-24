from adjust_price import calculate_product_discount




def process_orders(orders):
    product = orders.get("product")
    price = orders.get("price")
    1000
    discount = calculate_product_discount(product)
    new_price = price* discount
    500
    if new_price  > 500:
        label = "expensive"
    else:
        label = "cheap"
        