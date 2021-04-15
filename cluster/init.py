import os

if __name__ == "__main__" :
    for root, dirs, files in os.walk("tmp/test") :
        for file in files:
            os.remove(os.path.join(root, file))
            print(root + file + " has removed")
    for root, dirs, files in os.walk("tmp/split") :
        for file in files:
            os.remove(os.path.join(root, file))
            print(root + file + " has removed")
