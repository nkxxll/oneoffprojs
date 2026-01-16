FILE_EXTENSION :: enum {
    JAI;
    C;
    CPP;
    JAVA;
    JAVA_SCRIPT;
    TYPE_SCRIPT;
    TEXT;
    PYTHON;
    GO;
    RUST;
    RUBY;
    PHP;
    SWIFT;
    KOTLIN;
    SCALA;
    SHELL;
    BASH;
    LUA;
    R;
    SQL;
    DART;
    MARKDOWN;
    MDX;
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
        case .PYTHON;
            return "py";
        case .GO;
            return "go";
        case .RUST;
            return "rs";
        case .RUBY;
            return "rb";
        case .PHP;
            return "php";
        case .SWIFT;
            return "swift";
        case .KOTLIN;
            return "kt";
        case .SCALA;
            return "scala";
        case .SHELL;
            return "sh";
        case .BASH;
            return "bash";
        case .LUA;
            return "lua";
        case .R;
            return "r";
        case .SQL;
            return "sql";
        case .DART;
            return "dart";
        case .MARKDOWN;
            return "md";
        case .MDX;
            return "mdx";
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
        case "py";
            return .PYTHON;
        case "go";
            return .GO;
        case "rs";
            return .RUST;
        case "rb";
            return .RUBY;
        case "php";
            return .PHP;
        case "swift";
            return .SWIFT;
        case "kt";
            return .KOTLIN;
        case "scala";
            return .SCALA;
        case "sh";
            return .SHELL;
        case "bash";
            return .BASH;
        case "lua";
            return .LUA;
        case "r";
            return .R;
        case "sql";
            return .SQL;
        case "dart";
            return .DART;
        case "md";
            return .MARKDOWN;
        case "mdx";
            return .MDX;
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
        case .TYPE_SCRIPT; #through;
        case .GO; #through;
        case .RUST; #through;
        case .SWIFT; #through;
        case .KOTLIN; #through;
        case .SCALA; #through;
        case .DART;
            return "// ";
        case .PYTHON; #through;
        case .RUBY; #through;
        case .SHELL; #through;
        case .BASH; #through;
        case .R;
            return "# ";
        case .PHP;
            return "// ";
        case .LUA; #through;
        case .SQL;
            return "-- ";
        case .MARKDOWN; #through;
        case .MDX;
            return "<!-- ";
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

find_end_of_tag :: (line: string, start: int, comment_string_len: int) -> int {
    current := start + 1 + comment_string_len;
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

get_relative_path :: (cwd: string, full_path: string) -> string {
    if begins_with(full_path, cwd) {
        s: string;
        s.data = full_path.data + cwd.count;
        s.count = full_path.count - cwd.count;
        return s;
    }
    return full_path;
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
        case .TEXT; #through;
        case .PYTHON; #through;
        case .GO; #through;
        case .RUST; #through;
        case .RUBY; #through;
        case .PHP; #through;
        case .SWIFT; #through;
        case .KOTLIN; #through;
        case .SCALA; #through;
        case .SHELL; #through;
        case .BASH; #through;
        case .LUA; #through;
        case .R; #through;
        case .SQL; #through;
        case .DART; #through;
        case .MARKDOWN; #through;
        case .MDX;
            comment_string := file_extension_comment_string(file_extension);
            comment_string_len := comment_string.count;
            content, success := read_entire_file(filename);
            if !success {
                log_error("Warning: Could not open %!", filename);
                return;
            }
            defer free(content);
            lines := split(content, "\n");
            for *line, i: lines {
                index := find_index_from_left(line.*, tprint("%@", comment_string));
                if (index == -1) {
                    continue;
                }
                start := index;
                end := find_end_of_tag(line.*, start, comment_string_len);
                tag_string := slice(line.*, start + 1 + comment_string_len, end - start - 1 - comment_string_len);
                tag_type := tag_type_from_string(tag_string);
                comment: string;
                relative_path := get_relative_path(get_working_directory(), filename);
                if end + 1 < line.count {
                    if file_extension != .MDX && file_extension != .MARKDOWN {
                        comment = comment_after_tag(line.*, end);
                    } else {
                        line.count -= 4;
                        comment = comment_after_tag(line.*, end);
                    }
                    print_to_builder(builder, "%:%:% tag % '%'\n", relative_path, i + 1, start + 4, tag_type_to_string(tag_type), comment);
                } else {
                    print_to_builder(builder, "%:%:% tag %\n", relative_path, i + 1, start + 4, tag_type_to_string(tag_type));
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
