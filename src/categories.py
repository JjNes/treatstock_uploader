categories = {
    "All things": 4462,

    "3D Printing": 999,
    "3D Printer Accessories ": 999,
    "3D Printer Extruders": 1000,
    "3D Printer Parts": 999,
    "3D Printers": 999,
    "3D Printing Tests": 999,

    "Art": 307,
    "2D Art": 307,
    "Art Tools": 307,
    "Coins & Badges": 4462,
    "Interactive Art": 307,
    "Math Art": 307,
    "Scans & Replicas": 4462,
    "Sculptures": 4278,
    "Signs & Logos": 4462,

    "Fashion": 2622,
    "Accessories": 2622,
    "Bracelets": 2503,
    "Costume": 2622,
    "Earrings": 2506,
    "Glasses": 2491,
    "Jewelry": 520,
    "Keychains": 520,
    "Rings": 2519,

    "Gadgets": 1873,
    "Audio": 1873,
    "Camera": 813,
    "Computer": 1873,
    "Mobile Phone": 1644,
    "Tablet": 1873,
    "Video Games": 1873,

    "Automotive": 1418,
    "DIY": 4462,
    "Electronics": 1873,
    "Music": 4462,
    "R/C Vehicles": 1873,
    "Robotics": 1873,
    "Sport & Outdoors": 927,

    "Household": 2375,
    "Bathroom": 2347,
    "Containers": 2375,
    "Decor": 2375,
    "Household Supplies": 2375,
    "Kitchen & Dining": 2446,
    "Office Organization": 2375,
    "Outdoor & Garden": 2361,
    "Pets": 2459,

    "Learning": 3157,
    "Biology": 3157,
    "Engineering": 3157,
    "Math": 3157,
    "Physics & Astronomy": 3157,

    "Models": 4462,
    "Animals": 4462,
    "Buildings & Structures": 4462,
    "Creatures": 4462,
    "Food & Drink": 4462,
    "Model Furniture": 4462,
    "Model Robots": 4462,
    "People": 4462,
    "Props": 4462,
    "Vehicles": 4462,

    "Tools": 2210,
    "Hand Tools ": 2210,
    "Machine Tools ": 2210,
    "Tool Holders & boxes": 2210,

    "Toys & Games": 340,
    "Chess": 340,
    "Construction Toys": 340,
    "Dice": 340,
    "Games": 340,
    "Mechanical Toys": 340,
    "Playsets": 340,
    "Puzzles": 340,
    "Toy & Game Accessories": 340,
    "Other": 340,
}


def get(name: str) -> int:
    id = categories.get(name)
    if not id:
        return categories["All things"]
    return id