const std = @import("std");
const Allocator = std.mem.Allocator;

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
