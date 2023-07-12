import sys

def main(a, b, c):
    try:
        print("計算結果: ", (float(a) + float(b)) * float(c))

    except ValueError:
        print("数字を入力してください")

if __name__ == "__main__":
    try:
        a = sys.argv[1]
        b = sys.argv[2]
        c = sys.argv[3]
        main(a, b, c)
    except IndexError:
        print("引数が足りません")