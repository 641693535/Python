import hashlib
while True:
    st=str(input('Please Write:'))
    if len(st)>0:
        mid = hashlib.sha256(st.encode('utf-8'))
        result=mid.hexdigest
        print(result())
