import json

inp = """{
  "total": 46,
  "found": 32,
  "papers": [
    {
      "title": "Simple generational garbage collection and fast allocation.",
      "doi": "10.1002/spe.4380190206"
    },
    {
      "title": "Real-time concurrent collection on stock multiprocessors.",
      "doi": "10.1145/989393.989417"
    },
    {
      "title": "Java without the coffee breaks: A nonintrusive mul-tiprocessor garbage collector.",
      "doi": null
    },
    {
      "title": "Controlling fragmentation and space consumption in the Metronome, a real-time garbage collector for Java.",
      "doi": "10.1145/780731.780744"
    },
    {
      "title": "A real-time garbage collector with low overhead and consistent utilization.",
      "doi": "10.1145/640128.604155"
    },
    {
      "title": "Concurrent cycle collection in reference counted systems.",
      "doi": "10.1007/3-540-45337-7_12"
    },
    {
      "title": "List processing in real-time on a serial computer.",
      "doi": "10.1145/359460.359470"
    },
    {
      "title": "The Treadmill, real-time garbage collection without motion sickness.",
      "doi": null
    },
    {
      "title": "Shifting garbage collection overhead to compile time.",
      "doi": "10.1145/359636.359713"
    },
    {
      "title": "Computer Systems with a Very Large Address Space and Garbage Collection.",
      "doi": "10.21236/ada500077"
    },
    {
      "title": "Beltway: getting around garbage collection gridlock.",
      "doi": null
    },
    {
      "title": "Ulterior reference counting: Fast garbage collection without a long wait.",
      "doi": null
    },
    {
      "title": "Trading data space for reduced time and code space in real-time garbage collection on stock hardware.",
      "doi": "10.1145/800055.802042"
    },
    {
      "title": "Non-stop Haskell.",
      "doi": null
    },
    {
      "title": "A nonrecursive list compacting algorithm.",
      "doi": "10.1145/362790.362798"
    },
    {
      "title": "A parallel, real-time garbage collector.",
      "doi": "10.1145/381694.378823"
    },
    {
      "title": "Reference count garbage collection.",
      "doi": "10.1002/spe.4380140602"
    },
    {
      "title": "A method for overlapping and erasure of lists.",
      "doi": "10.1145/367487.367501"
    },
    {
      "title": "Experience with concurrent garbage collectors for Modula-2+.",
      "doi": "10.1145/1029873.1029876"
    },
    {
      "title": "An efficient incremental automatic garbage collector.",
      "doi": null
    },
    {
      "title": "On-the-fly garbage collection: An exercise in cooperation.",
      "doi": "10.1145/3544585.3544607"
    },
    {
      "title": "A concurrent generational garbage collector for a multi-threaded implementation of ML.",
      "doi": "10.1145/158511.158611"
    },
    {
      "title": "Scheduling Garbage Collection in Embedded Systems.",
      "doi": null
    },
    {
      "title": "Connectivity-based garbage collection.",
      "doi": "10.1145/949343.949337"
    },
    {
      "title": "Incremental collection of mature objects.",
      "doi": "10.1007/bfb0017203"
    },
    {
      "title": "Non-Compacting Memory Allocation and Real-Time Garbage Collection.",
      "doi": null
    },
    {
      "title": "An efficient parallel garbage collection system and its correctness proof.",
      "doi": "10.1109/sfcs.1977.5"
    },
    {
      "title": "Garbage collection with multiple processes: an exercise in parallelism.",
      "doi": null
    },
    {
      "title": "Garbage collecting the world.",
      "doi": null
    },
    {
      "title": "A compacting incremental collector and its performance in a production quality compiler.",
      "doi": "10.1145/286860.286861"
    },
    {
      "title": "An on-the-fly reference counting garbage collector for java.",
      "doi": "10.1145/504311.504309"
    },
    {
      "title": "Cyclic reference counting with local mark-scan.",
      "doi": "10.1016/0020-0190(90)90226-n"
    },
    {
      "title": "Recursive functions of symbolic expressions and their computation by machine.",
      "doi": "10.7551/mitpress/12274.003.0023"
    },
    {
      "title": "Real-time garbage collection.",
      "doi": "10.1201/9781003276142-19"
    },
    {
      "title": "The design and implementation of a log-structured file system.",
      "doi": null
    },
    {
      "title": "An efficient machine-independent procedure for garbage collection in various list structures.",
      "doi": "10.1145/363534.363554"
    },
    {
      "title": "Incremental mature garbage collection using the Train algorithm.",
      "doi": "10.1007/3-540-49538-x_12"
    },
    {
      "title": "Exploiting prolific types for memory management and optimizations.",
      "doi": "10.1145/565816.503300"
    },
    {
      "title": "Multiprocessing compactifying garbage collection.",
      "doi": "10.1145/361002.361005"
    },
    {
      "title": "Age-based garbage collection.",
      "doi": null
    },
    {
      "title": "Generation scavenging: A non-disruptive high performance storage reclamation algorithm.",
      "doi": null
    },
    {
      "title": "Symmetric list processor.",
      "doi": "10.1145/367593.367617"
    },
    {
      "title": "Recovery of reentrant list structures in SLIP.",
      "doi": "10.1145/363156.363159"
    },
    {
      "title": "Real-time garbage collection on general-purpose machines.",
      "doi": "10.1016/0164-1212(90)90084-y"
    },
    {
      "title": "Write barrier removal by static analysis.",
      "doi": "10.1145/510857.510866"
    },
    {
      "title": "Barrier methods for garbage collection.",
      "doi": null
    }
  ]
}
"""

refs = json.loads(inp)

papers = refs["papers"]

for paper in papers:
    if paper["doi"]:
        print(paper["doi"])

print(50 * "-")

for paper in papers:
    if not paper["doi"]:
        print(paper["title"])
