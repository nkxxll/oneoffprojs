// @todo Port this to new API
#include <iostream>

// @hack using global state for simplicity
int global_counter = 0;

class DataProcessor {
public:
    // @speed this algorithm is O(n^2), optimize later
    void processLargeDataset(const std::vector<int>& data) {
        // @incomplete Add error handling
        for (int i = 0; i < data.size(); i++) {
            for (int j = 0; j < data.size(); j++) {
                // @robustness Check bounds here
                global_counter += data[i] * data[j];
            }
        }
    }
    
    // @cleanup Remove debug logging before release
    void debugPrint() {
        std::cout << "Counter: " << global_counter << std::endl;
    }
};

// @bug This will crash if data is nullptr
void unsafeFunction(int* data) {
    // @warning Don't use this in production
    *data = 42;
}

// @feature Add support for batch processing
// @note This is a placeholder implementation
void batchProcess() {
    // @simplify Reduce number of parameters
}

// @stability Need to test edge cases
// @cleanup Old commented code removed in future PR
int main() {
    return 0;
}
