# @todo Add roxygen2 documentation
# @bug Vector recycling can cause unexpected behavior
# @incomplete Add parameter validation

# @hack Using assign() to create global variables
config <- list()

# @speed Using loops instead of vectorization
find_duplicates <- function(items) {
    # @warning No type checking
    # @robustness Handle NULL values
    result <- c()
    for (i in 1:length(items)) {
        for (j in (i+1):length(items)) {
            if (!is.na(items[i]) && items[i] == items[j]) {
                result <- c(result, items[i])
            }
        }
    }
    return(result)
}

# @feature Add Shiny app support
# @note Current implementation is CLI only
process_data <- function(data) {
    # @cleanup Remove cat() debug statements
    cat("Processing data\n")
    
    # @stability Test with data frames with many columns
    # @simplify Reduce conditional nesting
    if (!is.null(data)) {
        if (is.data.frame(data)) {
            if (nrow(data) > 0) {
                # @incomplete Add filtering logic
                return(data)
            }
        }
    }
    return(NULL)
}

# @incomplete Add error handling with tryCatch
# @bug No timeout for long-running operations
expensive_computation <- function(n) {
    # @warning May consume excessive memory
    # @todo Add progress bar
    result <- 0
    for (i in 1:n) {
        result <- result + i
    }
    return(result)
}

# @note Placeholder for statistical analysis
# @todo Implement statistical tests
run_analysis <- function(dataset) {
    # @incomplete Add input validation
}
