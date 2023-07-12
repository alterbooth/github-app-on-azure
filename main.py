import sys

def main(a, b, c):
    try:
        print("計算結果: ", (int(a) + int(b)) * int(c))

    except Exception as e:
        print("数字を入力してください")

if __name__ == "__main__":
    a = sys.argv[1]
    b = sys.argv[2]
    c = sys.argv[3]
    main(a, b, c)