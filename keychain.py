import os
import csv
import uuid
import random
from strb64 import b64_decode, b64_encode

class KeyChainItem:
    uuid=None
    weburl=""
    username=""
    password=""
    comment=""

    def __init__(self, uid, weburl, username, password, comment):
        self.uuid=uid
        self.weburl=weburl
        self.username=username
        self.password=password
        self.comment=comment

    def raw_unpack(self):
        return (self.uuid, self.weburl, self.username, self.password, self.comment)

    def unpack(self):
        import strb64
        a=b64_decode(self.weburl)
        b=b64_decode(self.comment)
        return (self.uuid, a, self.username, self.password, b)

def format_keychain(uid, weburl, username, password, comment):
    if uid==None:
        uid=str(uuid.uuid4())
    weburl=b64_encode(weburl)
    comment=b64_encode(comment)
    return KeyChainItem(uid, weburl, username, password, comment)
    

class UserKeyChainStorage:
    _workdir="storage/"

    def __init__(self, workdir=None):
        if workdir!=None:
            self._workdir=workdir
        if not os.path.exists(self._workdir):
            os.mkdir(self._workdir)

    def create_new_keychain(self, designated_name=None):
        if designated_name==None:
            while True:
                designated_name="%08x"%random.getrandbits(32)+".csv"
                if not os.path.exists(self._workdir+designated_name):
                    break
        f=open(self._workdir+designated_name, "w")
        f.close()
        return designated_name

    def _csv_get_item_list(self, designated_name):
        if not os.path.exists(self._workdir+designated_name):
            return list()
        li=list()
        csvfile=open(self._workdir+designated_name, "r")
        csvreader=csv.reader(csvfile)
        for row in csvreader:
            li.append(KeyChainItem(*row))
        csvfile.close()
        return li

    def _csv_write_item_list(self, designated_name, item_list):
        csvfile=open(self._workdir+designated_name, "w", newline='')
        csvwriter=csv.writer(csvfile)
        for item in item_list:
            csvwriter.writerow(item.raw_unpack())
        csvfile.close()

    def add_keychain_item(self, designated_name, weburl, username, password, comment, flush=True):
        item=format_keychain(None, weburl, username, password, comment)
        if not flush:
            return item
        li=self._csv_get_item_list(designated_name)
        li.append(item)
        self._csv_write_item_list(designated_name, li)

    def delete_keychain_item(self, designated_name, uid):
        li=self._csv_get_item_list(designated_name)
        for i in range(0, len(li)):
            if li[i].uuid==uid:
                li.pop(i)
                break
        self._csv_write_item_list(designated_name, li)

    def update_keychain_item(self, designated_name, uid, weburl, username, password, comment):
        li=self._csv_get_item_list(designated_name)
        for i in range(0, len(li)):
            if li[i].uuid==uid:
                li[i]=format_keychain(uid, weburl, username, password, comment)
                break
        self._csv_write_item_list(designated_name, li)

    #def batch_operation(self, designated_name, operations)

    def get_keychain_item_list(self, designated_name):
        li=self._csv_get_item_list(designated_name)
        li2=[x.unpack() for x in li]
        return li2
    


KeyChainStorage=UserKeyChainStorage("storage/")



if __name__=="__main__":
    csvfile=open("b64test.csv", "w", newline='')
    csvwriter=csv.writer(csvfile)
    csvwriter.writerow((b64_encode("啥"),2,3))
    csvwriter.writerow((b64_encode("http://example.com/s?kw=a%20b+c&d=e"),2,3))
    csvfile.close()
    csvfile=open("b64test.csv", "r")
    csvreader=csv.reader(csvfile)
    for row in csvreader:
        print(row)
        a,b,c=row
        print(b64_decode(a))
    csvfile.close()
    print("====================")
    dname="_test.csv"
    KeyChainStorage.create_new_keychain(dname)
    KeyChainStorage.add_keychain_item(dname,"000.com","user1","pass1","")
    KeyChainStorage.add_keychain_item(dname,"123.com","user","pass","")
    KeyChainStorage.add_keychain_item(dname,"456.com","user2","pass2","comments")
    KeyChainStorage.add_keychain_item(dname,"789.com","user3","pass3","备注")
    item_list=KeyChainStorage.get_keychain_item_list(dname)
    print(item_list)
    uid,a,b,c,d=item_list[1]
    KeyChainStorage.delete_keychain_item(dname, uid)
    uid,a,b,c,d=item_list[0]
    KeyChainStorage.update_keychain_item(dname,uid,"newwebsite.com","user1","pass1","")
    item_list=KeyChainStorage.get_keychain_item_list(dname)
    print(item_list)
    
