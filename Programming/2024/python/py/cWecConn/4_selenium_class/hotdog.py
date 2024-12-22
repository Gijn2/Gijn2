from PIL import Image, ImageDraw, ImageFont

# Create an empty white image
image = Image.new('RGB', (800, 600), color='white')
draw = ImageDraw.Draw(image)

# Title text
title = "Mozzarella Cheese Hot Dog"
title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 40)
title_w, title_h = draw.textsize(title, font=title_font)
draw.text(((800 - title_w) / 2, 20), title, font=title_font, fill="black")

# Ingredients text
ingredients = [
    "Ingredients:",
    "- Hot dog bun",
    "- Mozzarella cheese stick",
    "- Sausage",
    "- 1 cup flour",
    "- 1 tsp baking powder",
    "- 2 tbsp sugar",
    "- A pinch of salt",
    "- 1 egg",
    "- 1 cup milk",
    "- Cooking oil (for frying)"
]
ingredients_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)

y_text = 80
for line in ingredients:
    draw.text((50, y_text), line, font=ingredients_font, fill="black")
    y_text += 30

# Cooking steps text
steps = [
    "Steps:",
    "1. Prepare the sausage and cheese sticks.",
    "2. Make the batter by mixing flour, baking powder, sugar, salt, egg, and milk.",
    "3. Insert sausage and cheese stick into the hot dog bun.",
    "4. Dip the bun in the batter and deep fry until golden brown.",
    "5. Drain the excess oil and serve with ketchup and mustard."
]
steps_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)

y_text += 20
for line in steps:
    draw.text((50, y_text), line, font=steps_font, fill="black")
    y_text += 30

# Save the image
image_path = "./img/mozzarella_cheese_hot_dog_recipe.png"
image.save(image_path)
image.show()