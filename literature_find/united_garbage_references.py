import re

ref = """[1]
APPEL, A. W. Simple generational garbage collection and fast allocation. Software - Practice and Experience 19, 2 (1989), 171--183.
Digital Library
Google Scholar
[2]
APPEL,A.W.,ELLIS, J. R., AND LI, K. Real-time concurrent collection on stock multiprocessors. In Proceedings of the SIGPLAN'88 Conference on Programming Language Design and Implementation (Atlanta, Georgia, June 1988). SIGPLAN Notices, 23, 7 (July), 11--20.
Digital Library
Google Scholar
[3]
BACON,D.F.,ATTANASIO, C. R., LEE, H. B., RAJAN,V.T., AND SMITH, S. Java without the coffee breaks: A nonintrusive mul-tiprocessor garbage collector. In Proc. of the SIGPLAN Conference on Programming Language Design and Implementation (Snowbird, Utah, June 2001). SIGPLAN Notices, 36, 5 (May), 92--103.
Digital Library
Google Scholar
[4]
BACON,D.F.,CHENG,P.,AND RAJAN, V. T. Controlling fragmentation and space consumption in the Metronome, a real-time garbage collector for Java. In Proceedings of the Conference on Languages, Compilers, and Tools for Embedded Systems (San Diego, California, June 2003). SIGPLAN Notices, 38, 7, 81--92.
Digital Library
Google Scholar
[5]
BACON,D.F.,CHENG,P.,AND RAJAN, V. T. A real-time garbage collector with low overhead and consistent utilization. In Proceedings of the 30th Annual ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages (New Orleans, Louisiana, Jan. 2003). SIGPLAN Notices, 38, 1, 285--298.
Digital Library
Google Scholar
[6]
BACON,D.F.,AND RAJAN, V. T. Concurrent cycle collection in reference counted systems. In European Conference on Object-Oriented Programming (Budapest, Hungary, June 2001), J. L. Knudsen, Ed., vol. 2072 of Lecture Notes in Computer Science, Springer-Verlag, pp. 207--235.
Digital Library
Google Scholar
[7]
BAKER, H. G. List processing in real-time on a serial computer. Commun. ACM 21, 4 (Apr. 1978), 280--294.
Digital Library
Google Scholar
[8]
BAKER, H. G. The Treadmill, real-time garbage collection without motion sickness. SIGPLAN Notices 27, 3 (Mar. 1992), 66--70.
Digital Library
Google Scholar
[9]
BARTH, J. M. Shifting garbage collection overhead to compile time. Commun. ACM 20, 7 (July 1977), 513--518.
Digital Library
Google Scholar
[10]
BISHOP,P.B.Computer Systems with a Very Large Address Space and Garbage Collection. PhD thesis, Laboratory for Computer Science, Massachussets Institute of Technology, May 1977. MIT/LCS/TR-178.
Google Scholar
[11]
BLACKBURN, S. M., JONES, R., MCKINLEY, K. S., AND MOSS,J. E. B. Beltway: getting around garbage collection gridlock. In Proc. of the SIGPLAN Conference on Programming Language Design and Implementation (Berlin, Germany, June 2002). SIGPLAN Notices, 37, 5, 153--164.
Digital Library
Google Scholar
[12]
BLACKBURN, S. M., AND MCKINLEY, K. S. Ulterior reference counting: Fast garbage collection without a long wait. In Proceedings of the Conference on Object-oriented Programing, Systems, Languages, and Applications (Anaheim, California, Oct. 2003). SIG-PLAN Notices, 38, 11, 344--358.
Digital Library
Google Scholar
[13]
BROOKS, R. A. Trading data space for reduced time and code space in real-time garbage collection on stock hardware. In Conference Record of the 1984 ACM Symposium on Lisp and Functional Programming (Austin, Texas, Aug. 1984), G. L. Steele, Ed., pp. 256--262.
Digital Library
Google Scholar
[14]
CHEADLE, A. M., FIELD,A.J.,MARLOW, S., PEYTON JONES, S. L., AND WHILE, R. L. Non-stop Haskell. In Proc. of the Fifth International Conference on Functional Programming (Montreal, Quebec, Sept. 2000). SIGPLAN Notices, 35, 9, 257--267.
Digital Library
Google Scholar
[15]
CHENEY, C. J. A nonrecursive list compacting algorithm. Commun. ACM 13, 11 (1970), 677--678.
Digital Library
Google Scholar
[16]
CHENG,P.,AND BLELLOCH, G. A parallel, real-time garbage collector. In Proc. of the SIGPLAN Conference on Programming Language Design and Implementation (Snowbird, Utah, June 2001). SIGPLAN Notices, 36, 5 (May), 125--136.
Digital Library
Google Scholar
[17]
CHRISTOPHER, T. W. Reference count garbage collection. Software - Practice and Experience 14, 6 (June 1984), 503--507.
Crossref
Google Scholar
[18]
COLLINS, G. E. A method for overlapping and erasure of lists. Commun. ACM 3, 12 (Dec. 1960), 655--657.
Digital Library
Google Scholar
[19]
DETREVILLE, J. Experience with concurrent garbage collectors for Modula-2+. Tech. Rep. 64, DEC Systems Research Center, Aug. 1990.
Google Scholar
[20]
DEUTSCH,L.P.,AND BOBROW, D. G. An efficient incremental automatic garbage collector. Commun. ACM 19, 7 (July 1976), 522--526.
Digital Library
Google Scholar
[21]
DIJKSTRA,E.W.,LAMPORT, L., MARTIN, A. J., SCHOLTEN, C. S., AND STEFFENS, E. F. M. On-the-fly garbage collection: An exercise in cooperation. In Hierarchies and Interfaces, F. L. Bauer et al., Eds., vol. 46 of Lecture Notes in Computer Science. Springer-Verlag, 1976, pp. 43--56.
Digital Library
Google Scholar
[22]
DOLIGEZ, D., AND LEROY, X. A concurrent generational garbage collector for a multi-threaded implementation of ML. In Conf. Record of the Twentieth ACM Symposium on Principles of Programming Languages (Jan. 1993), pp. 113--123.
Digital Library
Google Scholar
[23]
HENRIKSSON,R.Scheduling Garbage Collection in Embedded Systems. PhD thesis, Lund Institute of Technology, July 1998.
Google Scholar
[24]
HIRZEL, M., DIWAN, A., AND HERTZ, M. Connectivity-based garbage collection. In Proceedings of the Conference on Object-oriented Programing, Systems, Languages, and Applications (Anaheim, California, Oct. 2003). SIGPLAN Notices, 38, 11, 359--373.
Digital Library
Google Scholar
[25]
HUDSON, R. L., AND MOSS, J. E. B. Incremental collection of mature objects. In Proc. of the International Workshop on Memory Management (St. Malo, France, Sept. 1992), Y. Bekkers and J. Cohen, Eds., vol. 637 of Lecture Notes in Computer Science, pp. 388--403.
Digital Library
Google Scholar
[26]
JOHNSTONE,M.S.Non-Compacting Memory Allocation and Real-Time Garbage Collection. PhD thesis, University of Texas at Austin, Dec. 1997.
Digital Library
Google Scholar
[27]
KUNG,H.T.,AND SONG, S. W. An efficient parallel garbage collection system and its correctness proof. In IEEE Symposium on Foundations of Computer Science (1977), pp. 120--131.
Digital Library
Google Scholar
[28]
LAMPORT, L. Garbage collection with multiple processes: an exercise in parallelism. In Proc. of the 1976 International Conference on Parallel Processing (1976), pp. 50--54.
Google Scholar
[29]
LANG, B., QUENNIAC, C., AND PIQUER, J. Garbage collecting the world. In Conference Record of the Nineteenth Annual ACM Symposium on Principles of Programming Languages (Jan. 1992), SIG-PLAN Notices, pp. 39--50.
Digital Library
Google Scholar
[30]
LAROSE, M., AND FEELEY, M. A compacting incremental collector and its performance in a production quality compiler. In Proc. of the First International Symposium on Memory Management (Vancouver, B.C., Oct. 1998). SIGPLAN Notices, 34, 3 (Mar., 1999), 1--9.
Digital Library
Google Scholar
[31]
LEVANONI,Y.,AND PETRANK, E. An on-the-fly reference counting garbage collector for java. In Proceedings of the 16th ACM SIGPLAN conference on Object Oriented Programming, Systems, Languages, and Applications (Tampa Bay, Florida, Oct. 2001), pp. 367--380.
Digital Library
Google Scholar
[32]
MARTÍNEZ, A. D., WACHENCHAUZER, R., AND LINS, R. D. Cyclic reference counting with local mark-scan. Inf. Process. Lett. 34,1 (1990), 31--35.
Digital Library
Google Scholar
[33]
MCCARTHY, J. Recursive functions of symbolic expressions and their computation by machine. Commun. ACM 3, 4 (1960), 184--195.
Digital Library
Google Scholar
[34]
NETTLES, S., AND O'TOOLE, J. Real-time garbage collection. In Proc. of the SIGPLAN Conference on Programming Language Design and Implementation (June 1993). SIGPLAN Notices, 28, 6, 217--226.
Digital Library
Google Scholar
[35]
ROSENBLUM, M., AND OUSTERHOUT, J. K. The design and implementation of a log-structured file system. In Proc. of the Thirteenth ACM symposium on Operating Systems Principles (Pacific Grove, California, Oct. 1991). SIGOPS Operating Systems Review, 25,5,1--15.
Digital Library
Google Scholar
[36]
SCHORR, H., AND WAITE, W. M. An efficient machine-independent procedure for garbage collection in various list structures. Commun. ACM 10, 8 (1967), 501--506.
Digital Library
Google Scholar
[37]
SELIGMANN, J., AND GRARUP, S. Incremental mature garbage collection using the Train algorithm. In Ninth European Conference on Object-Oriented Programming (Åarhus, Denmark, 1995), W. G. Olthoff, Ed., vol. 952 of Lecture Notes in Computer Science, pp. 235--252.
Digital Library
Google Scholar
[38]
SHUF,Y.,GUPTA, M., BORDAWEKAR, R., AND SINGH, J. P. Exploiting prolific types for memory management and optimizations. In Proceedings of the 29th ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages (Portland, Oregon, Jan. 2002). SIGPLAN Notices, 37, 1, 295--306.
Digital Library
Google Scholar
[39]
STEELE, G. L. Multiprocessing compactifying garbage collection. Commun. ACM 18, 9 (Sept. 1975), 495--508.
Digital Library
Google Scholar
[40]
STEFANOVIC, D., MCKINLEY,K.S.,AND MOSS, J. E. B. Age-based garbage collection. In Proc. of the Conference on Object-Oriented Programming, Systems, Languages, and Applications (Denver, Colorado, Oct. 1999). SIGPLAN Notices, 34, 10, 370--381.
Digital Library
Google Scholar
[41]
UNGAR, D. M. Generation scavenging: A non-disruptive high performance storage reclamation algorithm. In Proceedings of the ACM SIGSOFT/SIGPLAN Software Engineering Symposium on Practical Software Development Environments (Pittsburgh, Pennsylvania, 1984), P. Henderson, Ed. SIGPLAN Notices, 19, 5, 157--167.
Digital Library
Google Scholar
[42]
WEIZENBAUM, J. Symmetric list processor. Commun. ACM 6,9 (Sept. 1963), 524--536.
Digital Library
Google Scholar
[43]
WEIZENBAUM, J. Recovery of reentrant list structures in SLIP. Commun. ACM 12, 7 (July 1969), 370--372.
Digital Library
Google Scholar
[44]
YUASA, T. Real-time garbage collection on general-purpose machines. Journal of Systems and Software 11, 3 (Mar. 1990), 181--198.
Digital Library
Google Scholar
[45]
ZEE, K., AND RINARD, M. Write barrier removal by static analysis. In Proc. of the Conference on Object-Oriented Programming, Systems, Languages, and Applications (Seattle, Washington, Oct. 2002), ACM Press. SIGPLAN Notices, 37, 11 (Nov.), 191--210.
Digital Library
Google Scholar
[46]
ZORN, B. Barrier methods for garbage collection. Tech. Rep. CU-CS-494-90, University of Colorado at Boulder, 1990.
Google Scholar"""


def main():
    entries = re.split(r"\[(\d+)\]\n", ref)

    print("[")
    for i in range(1, len(entries), 2):
        num = entries[i]
        text = entries[i + 1].strip()
        lines = [
            l
            for l in text.split("\n")
            if l.strip() not in ("Digital Library", "Google Scholar", "Crossref", "")
        ]
        text = " ".join(lines)

        # Title starts after last author initial (X.) where next word has lowercase
        match = re.search(r"[A-Z]\.\s*(?=[A-Z][a-z]|[A-Z]\s+[a-z])", text)
        if match:
            title_start = match.end()
            period_pos = text.index(".", title_start)
            title = text[title_start : period_pos + 1].strip()
            print(f"\"{title}\",")
    print("]")


if __name__ == "__main__":
    main()
