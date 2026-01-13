const std = @import("std");
const Allocator = std.mem.Allocator;

pub fn to_upper_copy(allocator: Allocator, string: []const u8) ![]const u8 {
    const tag_name_upper = try allocator.alloc(u8, string.len);
    defer allocator.free(tag_name_upper);
    for (string, 0..) |char, i| {
        tag_name_upper[i] = std.ascii.toUpper(char);
    }
    return try allocator.dupe(u8, tag_name_upper);
}

/// read an entire file with the file name
pub fn read_entire_file(allocator: Allocator, filename: []const u8) ![]const u8 {
    const file = try std.fs.cwd().openFile(filename, .{});
    const end = try file.getEndPos();
    const buffer = try allocator.alloc(u8, end);
    var reader = file.reader(buffer);
    const reader_interface = &reader.interface;

    try reader_interface.readSliceAll(buffer);
    return buffer;
}
