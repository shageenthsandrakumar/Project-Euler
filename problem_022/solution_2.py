def name_value(name):
    return sum(ord(char) - 64 for char in name)

def count_names_before(target, names):
    return sum(1 for name in names if name < target)

with open("0022_names.txt", "r") as file:
    text = file.read()
names = [name.replace('"', '') for name in text.split(",")]
total_score = sum((count_names_before(name, names) + 1) * name_value(name) for name in names)
print(total_score)
