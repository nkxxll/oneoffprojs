// @todo Add coroutines support
package com.example.app

// @hack Using nullable types everywhere
var globalCache: MutableMap<String, Any>? = null

// @bug This will throw NPE if list is null
fun processList(items: List<Int>?) {
    // @incomplete Handle empty lists
    // @warning No bounds checking
    items?.forEach { item ->
        println(item)
    }
}

// @speed This algorithm is O(n^2)
fun findDuplicates(items: List<Int>): List<Int> {
    // @robustness Validate input
    val result = mutableListOf<Int>()
    for (i in items.indices) {
        for (j in (i + 1) until items.size) {
            if (items[i] == items[j]) {
                result.add(items[i])
            }
        }
    }
    return result
}

class DataProcessor {
    // @cleanup Remove debug log statements
    fun process(data: String) {
        println("Processing: $data")
    }
    
    // @feature Add Flow support for reactive streams
    // @note Current implementation is blocking
    fun handleRequest(request: Map<String, Any>?) {
        // @stability Test with large collections
        // @simplify Reduce nested conditionals
        request?.let { req ->
            (req["data"] as? Map<String, Any>)?.let { data ->
                data["key"]?.let { key ->
                    process(key.toString())
                }
            }
        }
    }
    
    // @incomplete Add retry policy
    // @bug No exception handling
    suspend fun fetchData(url: String): String {
        // @warning Timeout may occur
        return ""
    }
}

// @note Placeholder for future async work
interface DataRepository {
    // @todo Implement with database access
    suspend fun getData(id: Int): Any
}
