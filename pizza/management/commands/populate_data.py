import json
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from pizza.models import Pizza, Extra, Ingredient


class Command(BaseCommand):
    help = "Populate database with sample pizza, extra, and ingredient data from JSON fixtures"

    def handle(self, *args, **options):
        # Load JSON data
        fixtures_path = os.path.join(
            settings.BASE_DIR, "fixtures", "pizza_fixtures.json"
        )

        try:
            with open(fixtures_path, "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR(f"Fixtures file not found at {fixtures_path}")
            )
            return
        except json.JSONDecodeError as e:
            self.stdout.write(self.style.ERROR(f"Invalid JSON in fixtures file: {e}"))
            return

        self.stdout.write("--- Populating Ingredients ---")
        # Create ingredients
        created_ingredients = {}
        for ing_data in data.get("ingredients", []):
            ing, created = Ingredient.objects.get_or_create(
                name=ing_data["name"], defaults=ing_data
            )
            created_ingredients[ing.name] = ing
            if created:
                self.stdout.write(f"Created ingredient: {ing.name}")
            else:
                self.stdout.write(f"Ingredient '{ing.name}' already exists.")

        self.stdout.write("\n--- Populating Pizzas ---")
        # Create pizzas with ingredients
        for pizza_data in data.get("pizzas", []):
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

            # Clear existing ingredients if the pizza wasn't just created
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
            pizza.save()

        self.stdout.write("\n--- Populating Extras ---")
        # Create extras
        for extra_data in data.get("extras", []):
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
