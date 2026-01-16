// @todo Add Codable conformance
import Foundation

// @hack Using force unwrap for testing
var globalConfig: [String: Any]!

// @bug This will crash on nil
func processData(_ data: String?) {
    // @incomplete Handle empty strings
    // @warning No error handling
    print("Processing: \(data!)")
}

// @speed This is O(n^2), use a Set instead
func findDuplicates(_ items: [Int]) -> [Int] {
    // @robustness Check for empty arrays
    var result: [Int] = []
    for i in 0..<items.count {
        for j in (i+1)..<items.count {
            if items[i] == items[j] {
                result.append(items[i])
            }
        }
    }
    return result
}

class DataService {
    // @cleanup Remove debug print statements
    init() {
        print("DataService initialized")
        // @incomplete Add proper initialization
    }
    
    // @feature Add async/await support
    // @note Current implementation is synchronous
    func handleRequest(_ request: [String: Any]?) -> Void {
        // @stability Test with concurrent operations
        // @simplify Reduce optional chaining
        if let req = request,
           let data = req["data"] as? [String: Any],
           let key = data["key"] {
            processData(key as? String)
        }
    }
    
    // @incomplete Add validation
    // @bug No error handling for file operations
    func readLargeFile(_ path: String) throws -> String {
        // @warning May exceed memory limits
        return try String(contentsOfFile: path)
    }
    
    // @note Placeholder for observer pattern
    func observeChanges() {
        // @todo Implement observer pattern
    }
}

// @warning Thread-unsafe
class NotificationManager {
    // @bug Race condition with shared state
    private var notifications: [String] = []
}
