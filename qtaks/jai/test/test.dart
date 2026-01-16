// @todo Add null safety throughout
// @bug This will throw if data is null
// @incomplete Add error handling

// @hack Using dynamic types
dynamic globalConfig = {};

// @speed This is O(n^2), use a Set
List<int> findDuplicates(List<int> items) {
    // @warning No bounds checking
    List<int> result = [];
    for (int i = 0; i < items.length; i++) {
        for (int j = i + 1; j < items.length; j++) {
            if (items[i] == items[j]) {
                result.add(items[i]);
            }
        }
    }
    return result;
}

class DataService {
    // @cleanup Remove debug print statements
    void process(String data) {
        print('Processing: $data');
    }
    
    // @feature Add async/await for all async operations
    // @note Current implementation uses Futures
    void handleRequest(Map<String, dynamic>? request) {
        // @stability Test with large collections
        // @simplify Reduce nested conditionals
        if (request != null) {
            if (request['data'] is Map) {
                Map<String, dynamic> data = request['data'] as Map<String, dynamic>;
                if (data['key'] != null) {
                    process(data['key'].toString());
                }
            }
        }
    }
    
    // @incomplete Add timeout parameter
    // @bug No exception handling
    Future<String> fetchData(String url) async {
        // @warning May timeout indefinitely
        return '';
    }
    
    // @robustness Add input validation
    Future<void> saveData(dynamic data) async {
        // @todo Add logging
    }
}

// @note Placeholder for widget implementation
// @incomplete Add State management
class DataWidget {}
