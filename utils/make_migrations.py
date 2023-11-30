import glob
import os


def make_migrations():
    list_of_files = glob.glob("database/migrations/*")
    latest_file = max(list_of_files, key=os.path.getctime)
    exec(open(latest_file).read())
