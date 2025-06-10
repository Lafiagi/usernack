from django.core.management.base import BaseCommand
from pizza.models import Pizza, Extra, Ingridient  # Import Ingridient


class Command(BaseCommand):
    help = "Populate database with sample pizza, extra, and ingredient data"

    def handle(self, *args, **options):
        self.stdout.write("--- Populating Ingridients ---")
        # Create ingredients
        ingredients_data = [
            {"name": "Dough"},
            {"name": "Tomato Sauce"},
            {"name": "Mozzarella Cheese"},
            {"name": "Fresh Basil"},
            {"name": "Pepperoni Slices"},
            {"name": "Mushrooms"},
            {"name": "Cooked Ham"},
            {"name": "Artichoke Hearts"},
            {"name": "Black Olives"},
            {"name": "Pineapple Chunks"},
            {"name": "Onions"},
            {"name": "Bell Peppers"},
        ]

        # Store created ingredient objects to link them to pizzas later
        created_ingredients = {}
        for ing_data in ingredients_data:
            ing, created = Ingridient.objects.get_or_create(
                name=ing_data["name"], defaults=ing_data
            )
            created_ingredients[ing.name] = ing  # Store the object
            if created:
                self.stdout.write(f"Created ingredient: {ing.name}")
            else:
                self.stdout.write(f"Ingredient '{ing.name}' already exists.")

        self.stdout.write("\n--- Populating Pizzas ---")
        # Create pizzas with ingredients
        pizzas_data = [
            {
                "name": "Margherita",
                "description": "Classic pizza with tomato sauce, mozzarella, and fresh basil",
                "base_price": 12.99,
                "image_url": "https://example.com/margherita.jpg",
                "ingredients": [
                    "Dough",
                    "Tomato Sauce",
                    "Mozzarella Cheese",
                    "Fresh Basil",
                ],
            },
            {
                "name": "Pepperoni",
                "description": "Delicious pepperoni with mozzarella cheese and tomato sauce",
                "base_price": 15.99,
                "image_url": "https://example.com/pepperoni.jpg",
                "ingredients": [
                    "Dough",
                    "Tomato Sauce",
                    "Mozzarella Cheese",
                    "Pepperoni Slices",
                ],
            },
            {
                "name": "Quattro Stagioni",
                "description": "Four seasons pizza with mushrooms, ham, artichokes, and olives",
                "base_price": 18.99,
                "image_url": "https://example.com/quattro.jpg",
                "ingredients": [
                    "Dough",
                    "Tomato Sauce",
                    "Mozzarella Cheese",
                    "Mushrooms",
                    "Cooked Ham",
                    "Artichoke Hearts",
                    "Black Olives",
                ],
            },
            {
                "name": "Hawaiian",
                "description": "Tropical pizza with ham, pineapple, and mozzarella",
                "base_price": 16.99,
                "image_url": "https://example.com/hawaiian.jpg",
                "ingredients": [
                    "Dough",
                    "Tomato Sauce",
                    "Mozzarella Cheese",
                    "Cooked Ham",
                    "Pineapple Chunks",
                ],
            },
        ]

        for pizza_data in pizzas_data:
            # Extract ingredients list before creating/getting the pizza
            ingredient_names = pizza_data.pop("ingredients", [])

            pizza, created = Pizza.objects.get_or_create(
                name=pizza_data["name"], defaults=pizza_data
            )

            # Add ingredients to the pizza
            if created:
                self.stdout.write(f"Created pizza: {pizza.name}")
            else:
                self.stdout.write(
                    f"Pizza '{pizza.name}' already exists. Updating ingredients."
                )

            # Clear existing ingredients if the pizza wasn't just created, to avoid duplicates
            # and ensure the command is idempotent.
            if not created:
                pizza.ingredients.clear()

            for ing_name in ingredient_names:
                ingredient_obj = created_ingredients.get(ing_name)
                if ingredient_obj:
                    pizza.ingredients.add(ingredient_obj)
                else:
                    self.stdout.write(
                        self.style.WARNING(
                            f"Ingredient '{ing_name}' not found for pizza '{pizza.name}'. Skipping."
                        )
                    )
            pizza.save()  # Save the pizza after adding ingredients

        self.stdout.write("\n--- Populating Extras ---")
        # Create extras
        extras_data = [
            {"name": "Extra Cheese", "price": 2.50},
            {"name": "Pepperoni", "price": 3.00},
            {"name": "Mushrooms", "price": 2.00},
            {"name": "Olives", "price": 1.50},
            {"name": "Bell Peppers", "price": 2.00},
            {"name": "Onions", "price": 1.50},
            {"name": "Ham", "price": 3.50},
            {"name": "Sausage", "price": 3.00},
            {"name": "Bacon", "price": 3.50},
            {"name": "Anchovies", "price": 2.50},
        ]

        for extra_data in extras_data:
            extra, created = Extra.objects.get_or_create(
                name=extra_data["name"], defaults=extra_data
            )
            if created:
                self.stdout.write(f"Created extra: {extra.name}")
            else:
                self.stdout.write(f"Extra '{extra.name}' already exists.")

        self.stdout.write(
            self.style.SUCCESS("\nSuccessfully populated database with sample data!")
        )
