import os
import django
from decimal import Decimal

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecommerce.settings")
django.setup()

from django.contrib.auth.models import User
from shop.models import Category, Item, Cart

def run():
    # Create demo user
    if not User.objects.filter(username="demo").exists():
        user = User.objects.create_user("demo", password="demo1234")
        Cart.objects.get_or_create(user=user)
        print("Created user: demo / demo1234")

    cat_names = ["Electronics", "Books", "Clothing", "Home"]
    cats = []
    for name in cat_names:
        c, _ = Category.objects.get_or_create(name=name, slug=name.lower())
        cats.append(c)

    sample_items = [
        ("Wireless Headphones", "Noise-cancelling over-ear", Decimal("99.99"), "electronics", 25,
         "https://images.unsplash.com/photo-1518442530544-07a7d61a59a7?q=80&w=800&auto=format&fit=crop"),
        ("Smart Watch", "Fitness tracking and notifications", Decimal("149.00"), "electronics", 40,
         "https://m.media-amazon.com/images/I/61pIzNaNRWL.jpg"),
        ("Sci-Fi Novel", "A thrilling space adventure", Decimal("12.50"), "books", 100,
         "https://images.unsplash.com/photo-1521587760476-6c12a4b040da?q=80&w=800&auto=format&fit=crop"),
        ("Denim Jacket", "Classic fit", Decimal("59.00"), "clothing", 15,
         "https://images.unsplash.com/photo-1512436991641-6745cdb1723f?q=80&w=800&auto=format&fit=crop"),
        ("Ceramic Mug", "Matte finish 350ml", Decimal("9.99"), "home", 80,
         "https://images.unsplash.com/photo-1511920170033-f8396924c348?q=80&w=800&auto=format&fit=crop"),
    ]

    for title, desc, price, slug, stock, img in sample_items:
        cat = Category.objects.get(slug=slug)
        Item.objects.get_or_create(
            title=title,
            description=desc,
            price=price,
            category=cat,
            stock=stock,
            image_url=img
        )
    print("Seeded categories and items.")

if __name__ == "__main__":
    run()
