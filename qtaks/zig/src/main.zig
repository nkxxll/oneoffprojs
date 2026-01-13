const std = @import("std");
const qtaks = @import("qtaks");
const basic = qtaks.basic;
const print = std.debug.print;

const FILENAME = "src/main.zig";
pub fn main() !void {
    // @TODO make a gpt and pass it once
    // @tOdO this is another test
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();
    const alloc = gpa.allocator();

    const content = try basic.read_entire_file(alloc, FILENAME);
    defer alloc.free(content);

    const list = try qtaks.parse_file_content(alloc, FILENAME, content);
    defer {
        for (list) |item| {
            alloc.free(item);
        }
        alloc.free(list);
    }

    const output = try std.mem.join(alloc, "\n", list);
    defer alloc.free(output);
    print("{s}\n", .{output});
}
