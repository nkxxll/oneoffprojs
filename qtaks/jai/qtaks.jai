FILE_EXTENSION :: enum {
    JAI;
    C;
    CPP;
    JAVA;
    JAVA_SCRIPT;
    TYPE_SCRIPT;
    TEXT;
    UNKOWN;
}

file_extension_to_string :: (file_extension: FILE_EXTENSION) -> string {
    if #complete file_extension == {
        case .JAI;
            return "jai";
        case .C;
            return "c";
        case .CPP;
            return "cpp";
        case .JAVA;
            return "java";
        case .JAVA_SCRIPT;
            return "js";
        case .TYPE_SCRIPT;
            return "ts";
        case .TEXT;
            return "txt";
        case FILE_EXTENSION.UNKOWN;
            return "unknown";
    }
}

file_extension_from_string :: (s: string) -> FILE_EXTENSION {
    if s == {
        case "jai";
            return .JAI;
        case "js";
            return .JAVA_SCRIPT;
        case "ts";
            return .TYPE_SCRIPT;
        case "java";
            return .JAVA;
        case "c";
            return .C;
        case "cpp";
            return .CPP;
        case "txt";
            return .TEXT;
        case;
            return FILE_EXTENSION.UNKOWN;

    }
}

file_extension_comment_string :: (file_extension: FILE_EXTENSION) -> string {
    if #complete file_extension == {
        case .JAI; #through;
        case .C; #through;
        case .CPP; #through;
        case .JAVA; #through;
        case .JAVA_SCRIPT; #through;
        case .TYPE_SCRIPT;
            return "// ";
        case .TEXT; #through;
        case FILE_EXTENSION.UNKOWN;
            return "";

    }
}

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

tag_type_to_string :: (tag_type: TAG_TYPE) -> string {
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
        case TAG_TYPE.UNKOWN;
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
            return TAG_TYPE.UNKOWN;
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
    file_extension := file_extension_from_string(extension);
    if #complete file_extension == {
        case .JAI; #through;
        case .C; #through;
        case .JAVA; #through;
        case .JAVA_SCRIPT; #through;
        case .TYPE_SCRIPT; #through;
        case .CPP; #through;
        case .TEXT;
        comment_string := file_extension_comment_string(file_extension);
        content, success := read_entire_file(filename);
            if !success {
                log_error("Warning: Could not open %!", filename);
                return;
            }
            defer free(content);
            lines := split(content, "\n");
            for line, i: lines {
                index := find_index_from_left(line, tprint("%@", comment_string));
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
                    print_to_builder(builder, "% tag at %:%:% '%'\n", tag_type_to_string(tag_type), filename, i + 1, start + 4, comment);
                } else {
                    print_to_builder(builder, "% tag at %:%:%\n", tag_type_to_string(tag_type), filename, i + 1, start + 4);
                }
            }
        case FILE_EXTENSION.UNKOWN;
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
