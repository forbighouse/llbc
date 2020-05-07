import leveldb

db = leveldb.LevelDB('./db')
db.Put(b'hello', b'word')
a = db.Get(b'hello')
print(str(a))
