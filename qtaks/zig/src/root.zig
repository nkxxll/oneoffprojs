const std = @import("std");
const Allocator = std.mem.Allocator;
const ArrayList = std.ArrayList;

pub const Tag = enum {
    TODO,
    INCOMPLETE,
    BUG,
    SPEED,
    CLEANUP,
    ROBUSTNESS,
    WARNING,
    STABILITY,
    FEATURE,
    HACK,
    NOTE,
    SIMPLIFY,

    pub fn to_string(self: Tag) []const u8 {
        return switch (self) {
            .TODO => "TODO",
            .INCOMPLETE => "INCOMPLETE",
            .BUG => "BUG",
            .SPEED => "SPEED",
            .CLEANUP => "CLEANUP",
            .ROBUSTNESS => "ROBUSTNESS",
            .WARNING => "WARNING",
            .STABILITY => "STABILITY",
            .FEATURE => "FEATURE",
            .HACK => "HACK",
            .NOTE => "NOTE",
            .SIMPLIFY => "SIMPLIFY",
        };
    }

    pub fn from_string(str: []const u8) ?Tag {
        return if (std.mem.eql(u8, str, "TODO"))
            .TODO
        else if (std.mem.eql(u8, str, "INCOMPLETE"))
            .INCOMPLETE
        else if (std.mem.eql(u8, str, "BUG"))
            .BUG
        else if (std.mem.eql(u8, str, "SPEED"))
            .SPEED
        else if (std.mem.eql(u8, str, "CLEANUP"))
            .CLEANUP
        else if (std.mem.eql(u8, str, "ROBUSTNESS"))
            .ROBUSTNESS
        else if (std.mem.eql(u8, str, "WARNING"))
            .WARNING
        else if (std.mem.eql(u8, str, "STABILITY"))
            .STABILITY
        else if (std.mem.eql(u8, str, "FEATURE"))
            .FEATURE
        else if (std.mem.eql(u8, str, "HACK"))
            .HACK
        else if (std.mem.eql(u8, str, "NOTE"))
            .NOTE
        else if (std.mem.eql(u8, str, "SIMPLIFY"))
            .SIMPLIFY
        else
            null;
    }

    pub fn is_valid(str: []const u8) bool {
        return from_string(str) != null;
    }
};

pub const Range = struct {
    start: usize,
    end: usize,

    pub fn new(start: usize, end: usize) Range {
        return Range{ .start = start, .end = end };
    }
};

fn find_tag_end(line: []const u8, start: usize) usize {
    var current = start + 3;
    while (std.ascii.isAlphanumeric(line[current])) {
        if (current + 1 >= line.len) return current;
        current += 1;
    }
    return current;
}

pub const QuickfixItem = struct {
    tag_name: []const u8,
    file_path: []const u8,
    line: usize,
    col: usize,
};

fn find_project_root(allocator: Allocator) ![]const u8 {
    var cwd = try std.fs.cwd().openDir(".", .{});
    defer cwd.close();

    const markers = [_][]const u8{ ".git", ".jj", "build.zig", "Cargo.toml", "package.json" };

    var depth: usize = 0;
    const max_depth = 10;

    while (depth < max_depth) {
        for (markers) |marker| {
            _ = cwd.statFile(marker) catch continue;
            const cwd_path = try cwd.realpathAlloc(allocator, ".");
            return cwd_path;
        }

        if (cwd.openDir("..", .{})) |parent| {
            cwd.close();
            cwd = parent;
            depth += 1;
        } else |_| {
            break;
        }
    }

    cwd.close();
    return try std.fs.cwd().realpathAlloc(allocator, ".");
}

pub fn format_quickfix_item(allocator: Allocator, file_path: []const u8, content: []const u8, range: Range, line_num: usize) !QuickfixItem {
    const tag_start = range.start + 4; // skip "// @"
    const tag_name = content[tag_start..range.end];
    const tag_name_owned = try allocator.dupe(u8, tag_name);

    const tag_name_upper = try allocator.alloc(u8, tag_name_owned.len);
    for (tag_name_owned, 0..) |char, i| {
        tag_name_upper[i] = std.ascii.toUpper(char);
    }
    allocator.free(tag_name_owned);

    const file_path_owned = try allocator.dupe(u8, file_path);

    return QuickfixItem{
        .tag_name = tag_name_upper,
        .file_path = file_path_owned,
        .line = line_num,
        .col = range.start + 1,
    };
}

pub fn quickfix_item_to_string(allocator: Allocator, item: QuickfixItem) ![]u8 {
    return try std.fmt.allocPrint(allocator, "{s} {s}:{}:{}", .{
        item.tag_name,
        item.file_path,
        item.line,
        item.col,
    });
}

pub fn get_all_comments(allocator: Allocator, content: []const u8) ![]Range {
    var split_lines = std.mem.splitScalar(u8, content, '\n');
    var range_list = try ArrayList(Range).initCapacity(allocator, 64);
    defer range_list.deinit(allocator);
    while (split_lines.next()) |line| {
        const start = std.mem.indexOf(u8, line, "// @") orelse continue;
        const end = find_tag_end(line, start);
        try range_list.append(allocator, Range.new(start, end));
    }
    return try range_list.toOwnedSlice(allocator);
}

pub fn make_quickfix_item(allocator: Allocator, file_path: []const u8, content: []const u8, range: Range, line_num: usize) ![]const u8 {
    const item = try format_quickfix_item(allocator, file_path, content, range, line_num);
    defer allocator.free(item.tag_name);
    defer allocator.free(item.file_path);
    return try quickfix_item_to_string(allocator, item);
}

pub fn parse_file_content(allocator: Allocator, file_path: []const u8, content: []const u8) ![][]const u8 {
    var split_lines = std.mem.splitScalar(u8, content, '\n');
    var quickfix_list = try ArrayList([]const u8).initCapacity(allocator, 64);
    defer quickfix_list.deinit(allocator);

    var line_num: usize = 1;

    while (split_lines.next()) |line| {
        const start = std.mem.indexOf(u8, line, "// @") orelse {
            line_num += 1;
            continue;
        };

        const end = find_tag_end(line, start);
        const range = Range.new(start, end);

        const quickfix_item = try make_quickfix_item(allocator, file_path, line, range, line_num);
        try quickfix_list.append(allocator, quickfix_item);

        line_num += 1;
    }

    return try quickfix_list.toOwnedSlice(allocator);
}
