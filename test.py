from secretaryairin import SecretaryAirin

if __name__=='__main__':
    sa = SecretaryAirin()
    sa.args = ("baidu.com", )
    sa.run()
    print(sa.datas)
