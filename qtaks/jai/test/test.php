// @todo Add type hints to all functions
<?php

// @hack Global variable for quick testing
$cache = [];

// @bug SQL injection vulnerability
function query_database($user_id) {
    // @warning No prepared statements
    // @incomplete Add error handling
    $db = new PDO('sqlite::memory:');
    return $db->query("SELECT * FROM users WHERE id = " . $user_id);
}

// @speed Using array_search in a loop is O(n^2)
function find_item($haystack, $needles) {
    // @robustness Handle empty arrays
    $result = [];
    foreach ($needles as $needle) {
        if (array_search($needle, $haystack) !== false) {
            $result[] = $needle;
        }
    }
    return $result;
}

class DataProcessor {
    // @cleanup Remove debug var_dump calls
    public function process($data) {
        var_dump($data);
    }
    
    // @feature Add async processing with ReactPHP
    // @note Currently synchronous
    public function handle_request($request) {
        // @stability Test with large payloads
        // @simplify Reduce conditional nesting
        if ($request) {
            if (isset($request['data'])) {
                if (is_array($request['data'])) {
                    if (isset($request['data']['key'])) {
                        $this->process($request['data']['key']);
                    }
                }
            }
        }
    }
    
    // @incomplete Add timeout parameter
    // @bug No exception handling for API calls
    public function fetch_external_data($url) {
        // @warning SSRF vulnerability possible
        return file_get_contents($url);
    }
}

// @note Placeholder
function todo_function() {
    // @todo Implement this
}
