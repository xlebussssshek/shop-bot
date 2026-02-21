from __future__ import annotations

from collections.abc import Sequence
import aiosqlite


class Repo:
    def __init__(self, db_path: str):
        self.db_path = db_path

    async def _connect(self) -> aiosqlite.Connection:
        db = await aiosqlite.connect(self.db_path)
        db.row_factory = aiosqlite.Row
        await db.execute('PRAGMA foreign_keys = ON')
        return db

    async def list_categories(self) -> list[aiosqlite.Row]:
        async with await self._connect() as db:
            cur = await db.execute('SELECT id, name FROM categories ORDER BY name')
            return await cur.fetchall()

    async def add_category(self, name: str) -> int:
        async with await self._connect() as db:
            cur = await db.execute('INSERT INTO categories(name) VALUES (?)', (name,))
            await db.commit()
            return cur.lastrowid

    async def rename_category(self, category_id: int, name: str) -> None:
        async with await self._connect() as db:
            await db.execute('UPDATE categories SET name = ? WHERE id = ?', (name, category_id))
            await db.commit()

    async def delete_category(self, category_id: int) -> None:
        async with await self._connect() as db:
            await db.execute('DELETE FROM categories WHERE id = ?', (category_id,))
            await db.commit()

    async def list_products_by_category(self, category_id: int) -> list[aiosqlite.Row]:
        async with await self._connect() as db:
            cur = await db.execute(
                'SELECT id, name, description, price, in_stock FROM products WHERE category_id = ? ORDER BY id DESC',
                (category_id,),
            )
            return await cur.fetchall()

    async def list_all_products(self) -> list[aiosqlite.Row]:
        async with await self._connect() as db:
            cur = await db.execute(
                'SELECT p.id, c.name AS category_name, p.name, p.description, p.price, p.in_stock '
                'FROM products p JOIN categories c ON c.id = p.category_id ORDER BY p.id DESC'
            )
            return await cur.fetchall()

    async def get_product(self, product_id: int) -> aiosqlite.Row | None:
        async with await self._connect() as db:
            cur = await db.execute(
                'SELECT id, category_id, name, description, price, in_stock FROM products WHERE id = ?',
                (product_id,),
            )
            return await cur.fetchone()

    async def add_product(self, category_id: int, name: str, description: str, price: float, in_stock: bool = True) -> int:
        async with await self._connect() as db:
            cur = await db.execute(
                'INSERT INTO products(category_id, name, description, price, in_stock) VALUES (?, ?, ?, ?, ?)',
                (category_id, name, description, price, int(in_stock)),
            )
            await db.commit()
            return cur.lastrowid

    async def update_product(self, product_id: int, name: str, description: str, price: float, in_stock: bool) -> None:
        async with await self._connect() as db:
            await db.execute(
                'UPDATE products SET name = ?, description = ?, price = ?, in_stock = ? WHERE id = ?',
                (name, description, price, int(in_stock), product_id),
            )
            await db.commit()

    async def delete_product(self, product_id: int) -> None:
        async with await self._connect() as db:
            await db.execute('DELETE FROM products WHERE id = ?', (product_id,))
            await db.commit()

    async def set_product_stock(self, product_id: int, in_stock: bool) -> None:
        async with await self._connect() as db:
            await db.execute('UPDATE products SET in_stock = ? WHERE id = ?', (int(in_stock), product_id))
            await db.commit()

    async def add_to_cart(self, user_id: int, product_id: int, qty: int = 1) -> None:
        async with await self._connect() as db:
            await db.execute(
                'INSERT INTO cart_items(user_id, product_id, quantity) VALUES (?, ?, ?) '
                'ON CONFLICT(user_id, product_id) DO UPDATE SET quantity = quantity + excluded.quantity',
                (user_id, product_id, qty),
            )
            await db.commit()

    async def change_cart_quantity(self, user_id: int, product_id: int, delta: int) -> None:
        async with await self._connect() as db:
            await db.execute(
                'UPDATE cart_items SET quantity = quantity + ? WHERE user_id = ? AND product_id = ?',
                (delta, user_id, product_id),
            )
            await db.execute('DELETE FROM cart_items WHERE user_id = ? AND product_id = ? AND quantity <= 0', (user_id, product_id))
            await db.commit()

    async def remove_cart_item(self, user_id: int, product_id: int) -> None:
        async with await self._connect() as db:
            await db.execute('DELETE FROM cart_items WHERE user_id = ? AND product_id = ?', (user_id, product_id))
            await db.commit()

    async def clear_cart(self, user_id: int) -> None:
        async with await self._connect() as db:
            await db.execute('DELETE FROM cart_items WHERE user_id = ?', (user_id,))
            await db.commit()

    async def get_cart(self, user_id: int) -> list[aiosqlite.Row]:
        async with await self._connect() as db:
            cur = await db.execute(
                'SELECT c.product_id, c.quantity, p.name, p.price '
                'FROM cart_items c JOIN products p ON p.id = c.product_id WHERE c.user_id = ?',
                (user_id,),
            )
            return await cur.fetchall()

    async def create_order(
        self,
        user_id: int,
        customer_name: str,
        phone: str,
        address: str,
        comment: str,
        items: Sequence[aiosqlite.Row],
    ) -> int:
        total = sum(item['price'] * item['quantity'] for item in items)
        async with await self._connect() as db:
            cur = await db.execute(
                'INSERT INTO orders(user_id, customer_name, phone, address, comment, total_amount, status) '
                'VALUES (?, ?, ?, ?, ?, ?, ?)',
                (user_id, customer_name, phone, address, comment, total, 'new'),
            )
            order_id = cur.lastrowid

            for item in items:
                await db.execute(
                    'INSERT INTO order_items(order_id, product_id, name, price, quantity) VALUES (?, ?, ?, ?, ?)',
                    (order_id, item['product_id'], item['name'], item['price'], item['quantity']),
                )

            await db.execute('DELETE FROM cart_items WHERE user_id = ?', (user_id,))
            await db.commit()
            return order_id

    async def get_order(self, order_id: int) -> aiosqlite.Row | None:
        async with await self._connect() as db:
            cur = await db.execute('SELECT * FROM orders WHERE id = ?', (order_id,))
            return await cur.fetchone()

    async def set_order_status(self, order_id: int, status: str) -> None:
        async with await self._connect() as db:
            await db.execute('UPDATE orders SET status = ? WHERE id = ?', (status, order_id))
            await db.commit()

    async def list_recent_orders(self, limit: int = 10) -> list[aiosqlite.Row]:
        async with await self._connect() as db:
            cur = await db.execute(
                'SELECT id, customer_name, phone, total_amount, status, created_at FROM orders ORDER BY id DESC LIMIT ?',
                (limit,),
            )
            return await cur.fetchall()
