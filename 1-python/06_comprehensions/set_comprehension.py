favourite_chais = [
    "Masala Chai",
    "Green Chai",
    "Masala Chai",
    "Lemon Tea",
    "Green Tea",
    "Elaichi Chai",
]

unique_chai = {chai for chai in favourite_chais}
print(unique_chai)


recipes = {
    "Masala Chai": ["ginger", "cardamom", "clove"],
    "Elaichi": ["cardamom", "milk", "clove"],
    "Spicy Chai": ["ginger", "black pepper", "clove"],
}

unique_spices = {spice for ingredients in recipes.values() for spice in ingredients}
print(unique_spices)
