from operator import is_not_none

refs = """Flatt M and Findler R. Safe-for-Space Linked Environments. Proceedings of the Workshop Dedicated to Olivier Danvy on the Occasion of His 64th Birthday. (194-206).
https://doi.org/10.1145/3759427.3760379

Hughes J and Tratt L. (2025). Garbage Collection for Rust: The Finalizer Frontier. Proceedings of the ACM on Programming Languages. 9:OOPSLA2. (3588-3614). Online publication date: 9-Oct-2025.
https://doi.org/10.1145/3763179

Sotoudeh M. (2025). Pathological Cases for a Class of Reachability-Based Garbage Collectors. Proceedings of the ACM on Programming Languages. 9:OOPSLA1. (449-476). Online publication date: 9-Apr-2025.
https://doi.org/10.1145/3720430

Zhao H. (2020). Analysis of Big Data Cleaning Algorithm Research and System Platform Construction 2020 2nd International Conference on Applied Machine Learning (ICAML). 10.1109/ICAML51583.2020.00045. 978-1-7281-9264-2. (187-190).
https://ieeexplore.ieee.org/document/9607195/

Shri V and Reshma K. (2019). The Transactional Memory. International Journal of Scientific Research in Computer Science, Engineering and Information Technology. 10.32628/CSEIT1951117. (13-20). Online publication date: 4-Mar-2019.
http://ijsrcseit.com/paper/CSEIT1951117.pdf

Gnana Jeevan A and Maluk Mohamed M. (2018). SOGC: Implementing surrogate object garbage collector management for a Mobile Cloud Environment. Concurrency and Computation: Practice and Experience. 10.1002/cpe.4943. 31:4. Online publication date: 25-Feb-2019.
https://onlinelibrary.wiley.com/doi/10.1002/cpe.4943

Shidal J, Spilo A, Scheid P, Cytron R and Kavi K. (2015). Recycling trash in cache. ACM SIGPLAN Notices. 50:11. (118-130). Online publication date: 28-Jan-2016.
https://doi.org/10.1145/2887746.2754183

Shidal J, Spilo A, Scheid P, Cytron R and Kavi K. Recycling trash in cache. Proceedings of the 2015 International Symposium on Memory Management. (118-130).
https://doi.org/10.1145/2754169.2754183

Li P, Ding C and Luo H. (2014). Modeling heap data growth using average liveness. ACM SIGPLAN Notices. 49:11. (71-82). Online publication date: 11-May-2015.
https://doi.org/10.1145/2775049.2602997

Terei D, Aiken A and Vitek J. (2014). M3. ACM SIGPLAN Notices. 49:11. (3-13). Online publication date: 11-May-2015.
https://doi.org/10.1145/2775049.2602995

Chisnall D. (2014). Smalltalk in a C world. Science of Computer Programming. 96:P1. (4-16). Online publication date: 15-Dec-2014.
https://doi.org/10.1016/j.scico.2013.10.013

Li P, Ding C and Luo H. Modeling heap data growth using average liveness. Proceedings of the 2014 international symposium on Memory management. (71-82).
https://doi.org/10.1145/2602988.2602997

Terei D, Aiken A and Vitek J. M3. Proceedings of the 2014 international symposium on Memory management. (3-13).
https://doi.org/10.1145/2602988.2602995

Xu G. (2013). Resurrector. ACM SIGPLAN Notices. 48:10. (111-130). Online publication date: 12-Nov-2013.
https://doi.org/10.1145/2544173.2509512

Xu G. Resurrector. Proceedings of the 2013 ACM SIGPLAN international conference on Object oriented programming systems languages & applications. (111-130).
https://doi.org/10.1145/2509136.2509512

Tong L and Lau F. (2013). Skew-space garbage collection. Science of Computer Programming. 78:5. (445-457). Online publication date: 1-May-2013.
https://doi.org/10.1016/j.scico.2011.06.003

Kejariwal A. A Tool for Practical Garbage Collection Analysis in the Cloud. Proceedings of the 2013 IEEE International Conference on Cloud Engineering. (46-53).
https://doi.org/10.1109/IC2E.2013.13

Chisnall D. Smalltalk in a C world. Proceedings of the International Workshop on Smalltalk Technologies. (1-12).
https://doi.org/10.1145/2448963.2448967

Bhattacharya S, Rajamani K, Gopinath K and Gupta M. Does lean imply green?. Proceedings of the 12th ACM SIGMETRICS/PERFORMANCE joint international conference on Measurement and Modeling of Computer Systems. (259-270).
https://doi.org/10.1145/2254756.2254789

Bhattacharya S, Rajamani K, Gopinath K and Gupta M. (2012). Does lean imply green?. ACM SIGMETRICS Performance Evaluation Review. 40:1. (259-270). Online publication date: 7-Jun-2012.
https://doi.org/10.1145/2318857.2254789

Aigner M, Haas A, Kirsch C, Lippautz M, Sokolova A, Stroka S and Unterweger A. (2011). Short-term memory for self-collecting mutators. ACM SIGPLAN Notices. 46:11. (99-108). Online publication date: 18-Nov-2011.
https://doi.org/10.1145/2076022.1993493

Aigner M, Haas A, Kirsch C, Lippautz M, Sokolova A, Stroka S and Unterweger A. Short-term memory for self-collecting mutators. Proceedings of the international symposium on Memory management. (99-108).
https://doi.org/10.1145/1993478.1993493

Tan G. JNI light. Proceedings of the 8th Asian conference on Programming languages and systems. (114-130).
/doi/10.5555/1947873.1947885

Tong L and Lau F. Exploiting memory usage patterns to improve garbage collections in Java. Proceedings of the 8th International Conference on the Principles and Practice of Programming in Java. (39-48).
https://doi.org/10.1145/1852761.1852768

Tan G. (2010). JNI Light: An Operational Model for the Core JNI. Programming Languages and Systems. 10.1007/978-3-642-17164-2_9. (114-130).
http://link.springer.com/10.1007/978-3-642-17164-2_9

Sockut G and Iyer B. (2009). Online reorganization of databases. ACM Computing Surveys. 41:3. (1-136). Online publication date: 1-Jul-2009.
https://doi.org/10.1145/1541880.1541881

Trancón y Widemann B. A reference-counting garbage collection algorithmfor cyclical functional programming. Proceedings of the 7th international symposium on Memory management. (71-80).
https://doi.org/10.1145/1375634.1375645

Joisha P. A principled approach to nondeferred reference-counting garbage collection. Proceedings of the fourth ACM SIGPLAN/SIGOPS international conference on Virtual execution environments. (131-140).
https://doi.org/10.1145/1346256.1346275

Grossman D. (2007). The transactional memory / garbage collection analogy. ACM SIGPLAN Notices. 42:10. (695-706). Online publication date: 21-Oct-2007.
https://doi.org/10.1145/1297105.1297080

Grossman D. The transactional memory / garbage collection analogy. Proceedings of the 22nd annual ACM SIGPLAN conference on Object-oriented programming systems, languages and applications. (695-706).
https://doi.org/10.1145/1297027.1297080

Vechev M, Bacon D, Cheng P and Grove D. Derivation and evaluation of concurrent collectors. Proceedings of the 19th European conference on Object-Oriented Programming. (577-601).
https://doi.org/10.1007/11531142_25

Ramsay C and Stewart R. Cloaca: A Concurrent Hardware Garbage Collector for Non-strict Functional Languages. Proceedings of the 17th ACM SIGPLAN International Haskell Symposium. (41-54).
https://doi.org/10.1145/3677999.3678277

Muneeswari G and Shunmuganathan K. Time based agent garbage collection algorithm for multicore architectures. Proceedings of the International Conference on Advances in Computing, Communications and Informatics. (215-219).
https://doi.org/10.1145/2345396.2345432

Bhattacharya S, Nanda M, Gopinath K and Gupta M. Reuse, recycle to de-bloat software. Proceedings of the 25th European conference on Object-oriented programming. (408-432).
/doi/10.5555/2032497.2032524

Bhattacharya S, Nanda M, Gopinath K and Gupta M. (2011). Reuse, Recycle to De-bloat Software. ECOOP 2011 – Object-Oriented Programming. 10.1007/978-3-642-22655-7_19. (408-432).
http://link.springer.com/10.1007/978-3-642-22655-7_19"""

res = list(set(filter(is_not_none, [ref if "doi" in ref else None for ref in refs.split()])))

print("\n".join(res))
