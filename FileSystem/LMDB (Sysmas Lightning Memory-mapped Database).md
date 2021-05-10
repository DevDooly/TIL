# Editing LMDB (Sysmas Lightning Memory mapped Database)

Key-Value 형식의 데이터베이스 라이브러리다.

다른 키-값 데이터베이스와 달리 쓰기 트랜잭션을 보장하지 않는다.

AN ULTRA-FAST, ULTRA-COMPACT, CRASH-PROOF KEY-VALUE EMBEDDED DATA STORE.
Symas LMDB is an extraordinarily fast, memory-efficient database we developed for the OpenLDAP Project. With memory-mapped files, it has the read performance of a pure in-memory database while retaining the persistence of standard disk-based databases.
Bottom line, with only 32KB of object code, LMDB may seem tiny. But it’s the right 32KB. Compact and efficient are two sides of a coin; that’s part of what makes LMDB so powerful.

EXPLORE CAPABILITIES
Ordered-map interface
keys are always sorted; range lookups are supported
Fully-transactional
full ACID semantics with MVCC
Reader/writer transactions
readers don’t block writers; writers don’t block readers
Fully serialized writers
writes are always deadlock-free
Extremely cheap read transactions
can be performed using no mallocs or any other blocking calls
Multi-thread and multi-process concurrency supported
Environments may be opened by multiple processes on the same host
Multiple sub-databases may be created
transactions cover all sub-databases
Memory-mapped
allows for zero-copy lookup and iteration
Maintenance-free
no external process or background cleanup or compaction required
Crash-proof
no logs or crash recovery procedures required
No application-level caching
LMDB fully exploits the operating system’s buffer cache
32KB of object code and 6KLOC of C
fits in CPU L1 cache for maximum performance

https://symas.com/lmdb/

