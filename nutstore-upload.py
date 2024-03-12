from webdav4.client import Client

# username 为坚果云账号，password 为刚刚创建的密码
client = Client(base_url='https://dav.jianguoyun.com/dav/',
                auth=('imybfu@outlook.com', 'axzyqd3a6brx99ei'))

# ls 列出目录
# client.ls(path='/Nutshare/glossaries', detail=False)

# 上传本地文件
client.upload_file(from_path='glossary.json', to_path='/Nutshare/glossaries/test.json', overwrite=True)
