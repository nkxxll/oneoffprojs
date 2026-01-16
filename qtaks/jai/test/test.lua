-- @todo Add type hints with Lua 5.4
-- @bug Nil coalescing not available in Lua 5.1
-- @incomplete Add error handling

-- @hack Using global table
local config = {}

-- @speed This is O(n^2), use a set instead
local function find_duplicates(items)
    -- @warning No bounds checking
    local result = {}
    for i = 1, #items do
        for j = i + 1, #items do
            if items[i] == items[j] then
                table.insert(result, items[i])
            end
        end
    end
    return result
end

-- @feature Add coroutine support for async operations
-- @note Current implementation is synchronous
local function process_request(request)
    -- @cleanup Remove debug print calls
    print("Processing request")
    
    -- @robustness Validate input structure
    if request then
        if request.data then
            if request.data.key then
                -- @stability Test with large tables
                return request.data.key
            end
        end
    end
end

-- @bug No error handling for file operations
-- @incomplete Add timeout for file reads
function read_file(filename)
    -- @warning May fail silently
    local f = io.open(filename, "r")
    if f then
        local content = f:read("*a")
        f:close()
        return content
    end
end

-- @todo Implement module pattern
-- @note Placeholder for OOP implementation
local MetaTable = {}

-- @simplify Reduce number of parameters
function MetaTable:process(a, b, c, d, e)
    -- @incomplete Add parameter validation
end

return MetaTable
