with open("0022_names.txt", "r") as file:
    text = file.read()
names = [name.replace('"', '') for name in text.split(",")]
names.sort()
print(sum((i+1)*sum(ord(n.lower()) - 96 for n in names[i]) for i in range(len(names))))
