const std = @import("std");
const Allocator = std.mem.Allocator;
const ArrayList = std.ArrayList;

const SKIP_DIRS = [_][]const u8{ ".git", "node_modules", ".zig-cache", "zig-out", ".jj" };
const EXTENSIONS = [_][]const u8{ ".zig", ".ts", ".js", ".rs", ".py", ".java", ".c", ".h", ".cpp", ".hpp" };

pub fn should_skip_dir(name: []const u8) bool {
    for (SKIP_DIRS) |skip| {
        if (std.mem.eql(u8, name, skip)) {
            return true;
        }
    }
    return false;
}

pub fn should_scan_file(name: []const u8) bool {
    for (EXTENSIONS) |ext| {
        if (std.mem.endsWith(u8, name, ext)) {
            return true;
        }
    }
    return false;
}

pub fn walk_directory(allocator: Allocator, root_path: []const u8, file_list: *ArrayList([]const u8)) !void {
    var dir = try std.fs.cwd().openDir(root_path, .{ .iterate = true });
    defer dir.close();

    var iter = dir.iterate();

    while (try iter.next()) |entry| {
        if (should_skip_dir(entry.name)) {
            continue;
        }

        switch (entry.kind) {
            .file => {
                if (should_scan_file(entry.name)) {
                    const full_path = try std.fmt.allocPrint(allocator, "{s}/{s}", .{ root_path, entry.name });
                    try file_list.append(allocator, full_path);
                }
            },
            .directory => {
                const sub_path = try std.fmt.allocPrint(allocator, "{s}/{s}", .{ root_path, entry.name });
                try walk_directory(allocator, sub_path, file_list);
                allocator.free(sub_path);
            },
            else => {},
        }
    }
}
