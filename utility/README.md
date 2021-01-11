
1.  All triples are stored in the bsddb3 database.
    Before running rdf_test.py
    Install bsddb3 on MacOS with home brew:

    ! brew install berkeley-db@4
    ! BERKELEYDB_DIR=$(brew --prefix berkeley-db@4) pip install bsddb3


    On M1 CPU：
    

2. rdflib, plugin function: serialize, print the entire graph into Specified human readable format e.g. xml, n3, ttl


3. Namespace: 把数据库划分为多个空间。 e.g. Namespace: Person1, Namespace: Person2. 可以用于KG个性化存储，实现 KG personalization.


4. 换 namespace: select Jason/ select Lindsay