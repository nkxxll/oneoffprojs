FILENAME :: "qtaks.jai";

TAG_TYPE :: enum {
    BUG;
    CLEANUP;
    FEATURE;
    HACK;
    INCOMPLETE;
    NOTE;
    ROBUSTNESS;
    SIMPLIFY;
    SPEED;
    STABILITY;
    TODO;
    WARNING;
    UNKOWN;
}

string_from_tag_type :: (tag_type: TAG_TYPE) -> string {
    if #complete tag_type == {
        case .BUG;
            return "BUG";
        case .CLEANUP;
            return "CLEANUP";
        case .FEATURE;
            return "FEATURE";
        case .HACK;
            return "HACK";
        case .INCOMPLETE;
            return "INCOMPLETE";
        case .NOTE;
            return "NOTE";
        case .ROBUSTNESS;
            return "ROBUSTNESS";
        case .SIMPLIFY;
            return "SIMPLIFY";
        case .SPEED;
            return "SPEED";
        case .STABILITY;
            return "STABILITY";
        case .TODO;
            return "TODO";
        case .WARNING;
            return "WARNING";
        case .UNKOWN;
            return "UNKOWN";
    }

}

tag_type_from_string :: (tag_name: string) -> TAG_TYPE {
    to_lower_in_place(tag_name);
    if tag_name == {
        case "bug";
            return .BUG;
        case "cleanup";
            return .CLEANUP;
        case "feature";
            return .FEATURE;
        case "hack";
            return .HACK;
        case "incomplete";
            return .INCOMPLETE;
        case "note";
            return .NOTE;
        case "robustness";
            return .ROBUSTNESS;
        case "simplify";
            return .SIMPLIFY;
        case "speed";
            return .SPEED;
        case "stability";
            return .STABILITY;
        case "todo";
            return .TODO;
        case "warning";
            return .WARNING;
        case;
            return .UNKOWN;
    }
}

find_end_of_tag :: (line: string, start: int) -> int {
    current := start + 4;
    while is_alpha(line[current]) {
        if current + 1 >= line.count return line.count;
        current += 1;
    }
    return current;
}

// @todo use the tag type type
main :: () {
    content, success := read_entire_file(FILENAME);
    defer free(content);
    lines := split(content, "\n");
    builder : String_Builder;
    init_string_builder(*builder);
    for line, i: lines {
        index := find_index_from_left(line, "// @");
        if (index == -1) {
            continue;
        }
        start := index;
        end := find_end_of_tag(line, start);
        tag_string := slice(line, start + 4, end - start - 4);
        print_to_builder(*builder, "% tag at %:%:%\n", tag_string, FILENAME, i + 1, start + 4);
    }
    if !success {
        log_error("could not read the file");
        exit(1);
    }
    output := builder_to_string(*builder);
    print(output);
}

#import "Basic";
#import "File";
#import "String";
