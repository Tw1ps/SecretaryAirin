from secretaryairin import SecretaryAirin

if __name__=='__main__':
    sa = SecretaryAirin()
    sa.args = ("github.com", "./test.txt")
    sa.run()
    print(sa.datas)
