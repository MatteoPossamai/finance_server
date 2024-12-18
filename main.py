from logic.dropbox import dowload_dropbox_file, read_from_file, write_to_file
from utils.from_json_to_csv import from_json_to_csv
# dowload_dropbox_file("/personal_data/expenses.json")
# from_json_to_csv("./data/expenses.json", "./data/expenses.csv")
vals = read_from_file("./data/expenses.csv")

for i in range(100):
    vals.pop()
    
write_to_file("./data/random.csv", vals)