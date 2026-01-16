// @todo Implement Serializable interface
public class DataService {
    
    // @hack Quick fix for testing, refactor later
    private static String staticBuffer = "";
    
    // @speed This uses regex which is slow for large strings
    public String parseData(String input) {
        // @incomplete Add validation for null inputs
        return input.replaceAll("\\s+", "");
    }
    
    // @bug Memory leak if connection not closed
    public void connectToDatabase() {
        // @warning Make sure to close the connection
        // @robustness Add retry logic here
        // Connection conn = DriverManager.getConnection(...);
    }
    
    // @feature Support for async operations needed
    // @note Current implementation is synchronous
    public void processRequest() {
        // @cleanup Remove unused variables
        int unused = 0;
    }
    
    // @stability Add unit tests for edge cases
    // @simplify Reduce method complexity from 25 to < 10
    public int complexCalculation(int[] numbers) {
        // @incomplete Handle empty arrays
        int result = 0;
        for (int i = 0; i < numbers.length; i++) {
            for (int j = i + 1; j < numbers.length; j++) {
                result += numbers[i] + numbers[j];
            }
        }
        return result;
    }
}
