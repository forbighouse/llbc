import leveldb

db = leveldb.LevelDB("chaindata")

# single put
keys = db.RangeIter()
for s in keys:
    print(s)
# print(db.Get().decode('utf-8'))




# multiple put/delete applied atomically, and committed to disk

# batch = leveldb.WriteBatch()
# batch.Put(b'hello', b'world')
# batch.Put(b'hello again', b'world')
# batch.Delete(b'hello')
# #
# db.Write(batch, sync = True)