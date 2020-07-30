from score.simulator import *


def main():
    b = file_location("location_test.txt")
    for i in b:
        print(i[0], i[1])


if __name__ == "__main__":
    main()
