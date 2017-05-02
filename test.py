from enum import Enum

class Fruit(Enum):
    apple = 1 
    banana = 2 
    orange = 3 

def main():
    print Fruit.apple
    
if __name__ == "__main__":
    main()