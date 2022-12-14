class Personal:

    def __init__(self):
        pass

    @classmethod
    def code(cls):
        try:
            from urllib.request import urlopen
            url = str(input("What page would you like to explore? "))
            page = urlopen(url)
            html_bytes = page.read()
            html = html_bytes.decode("utf-8")
            print(html)
        except Exception as e:
            print(e)

    @classmethod
    def to_int(cls):
        no = str(input("Enter the bit-string to convert(1s and 0s): "))
        lot = [2, 3, 4, 5, 6, 7, 8, 9]
        for a in lot:
            while str(a) in list(no):
                no = str(input("Enter a string with 1s and 0s: "))
        else:
            try:
                if "." not in list(no):
                    print("Commencing computation")
                    y = list(no)
                    y.reverse()
                    q = []
                    for x in range(0, len(y)):
                        m = int(y[x]) * (2 ** x)
                        q.append(m)
                    print(f"-----{sum(q)}-----\nComputation complete!")
                elif "." in list(no):
                    print("Commencing computation")
                    z = list(no.split(".")[0])
                    z.reverse()
                    ones = []
                    for x in range(0, len(z)):
                        r = int(z[x]) * (2 ** x)
                        ones.append(r)
                    p = list(no.split(".")[1])
                    tens = []
                    for b in range(1, len(p)+1):
                        for g in range(0, len(p)):
                            w = int(p[g]) * (2 ** (-b))
                            tens.append(w)
                    print(f'-----{sum(ones) + sum(sorted(set(tens)))}-----\nComputation complete')
            except Exception as err:
                print(err)


v = Personal()
v.to_int()
