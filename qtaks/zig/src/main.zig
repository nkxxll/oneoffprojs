const std = @import("std");
const qtaks = @import("qtaks");
const print = std.debug.print;

pub fn main() !void {
    // @TODO make a gpt and pass it once
    // @tOdO this is another test
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();
    const alloc = gpa.allocator();

    const root = try qtaks.find_project_root(alloc);
    defer alloc.free(root);

    const list = try qtaks.process_directory(alloc, root);
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
