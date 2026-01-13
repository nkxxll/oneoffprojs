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

// this does only pointer magic to make a view into the line that holds the rest of the comment
// no need to free anything
comment_after_tag :: (line: string, tag_end: int) -> string {
    comment : string;
    comment.data = line.data + tag_end + 1;
    comment.count = line.count - tag_end - 1;

    comment = trim_right(comment);
    return comment;
}

visitor :: (info: *File_Visit_Info, builder: *String_Builder) {
    extension := path_extension(info.full_name);
    filename := info.full_name;
    if extension == {
        case "jai";
            content, success := read_entire_file(filename);
            if !success {
                log_error("Warning: Could not open %!", filename);
                return;
            }
            defer free(content);
            lines := split(content, "\n");
            for line, i: lines {
                index := find_index_from_left(line, "// @");
                if (index == -1) {
                    continue;
                }
                start := index;
                end := find_end_of_tag(line, start);
                tag_string := slice(line, start + 4, end - start - 4);
                tag_type := tag_type_from_string(tag_string);
                comment: string;
                if end + 1 < line.count {
                    comment = comment_after_tag(line, end);
                    print_to_builder(builder, "% tag at %:%:% '%'\n", string_from_tag_type(tag_type), filename, i + 1, start + 4, comment);
                } else {
                    print_to_builder(builder, "% tag at %:%:%\n", string_from_tag_type(tag_type), filename, i + 1, start + 4);
                }
            }
    }
}

Args :: struct {
    path := ".";
}

// @todo use the tag type type
main :: () {
    args : Args;
    builder : String_Builder;

    success, args=, is_set, free_args := parse_arguments(Args);
    if !success || free_args {
        log_error("Usage: % [-path <path>]", get_command_line_arguments()[0]);
        exit(1);
    }
    init_string_builder(*builder);

    visit_files(args.path, recursive=true, *builder, visitor);

    output := builder_to_string(*builder);
    print(output);
}

#import "Basic";
#import "File";
#import "String";
#import "Command_Line";
#import "File_Utilities";
