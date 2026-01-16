# @todo Add proper error handling
require 'json'

# @hack Using global config
$config = {}

# @bug This will crash on nil input
def process_data(data)
    # @incomplete Validate input
    # @warning No timeout handling
    puts "Processing: #{data}"
end

# @speed Using regex repeatedly, should compile pattern
def extract_emails(text)
    # @robustness Check for malformed emails
    text.scan(/\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b/)
end

class DataService
    # @cleanup Remove debug statements
    def initialize
        puts "DataService initialized"
        # @incomplete Add logging setup
    end
    
    # @feature Support async operations with Fiber
    # @note Current implementation is blocking
    def handle_request(request)
        # @stability Test with concurrent threads
        # @simplify Reduce if/else nesting
        if request
            if request[:data]
                if request[:data].is_a?(Hash)
                    if request[:data][:key]
                        process_data(request[:data][:key])
                    end
                end
            end
        end
    end
    
    # @incomplete Add validation for email format
    def send_email(to, subject, body)
        # @bug No retry on failure
        # @warning May exceed rate limits
    end
end

# @note Placeholder for future implementation
module Utilities
    # @todo Implement this utility function
end
