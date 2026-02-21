def product_card_text(product) -> str:
    stock = 'В наличии' if product['in_stock'] else 'Нет в наличии'
    return (
        f"🛍 {product['name']}\n\n"
        f"{product['description']}\n\n"
        f"Цена: {product['price']} ₽\n"
        f"Статус: {stock}"
    )
