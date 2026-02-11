import argparse
import os


def write_missing_files_report(custom_ident, path, files):
    report = []
    report.append(f"# Report for {custom_ident}")
    report.append("# Missing files report")
    report.append(f"There are {len(files)} missing in this comparison")
    report.append("The files are named:")
    for file in files:
        report.append(f"- {file}")
    with open(path) as f:
        f.write("\n".join(report))


def parse_all_args():
    p = argparse.ArgumentParser()
    p.add_argument("-first", type=str, required=True)
    p.add_argument("-second", type=str, required=True)
    return p.parse_args()


def main():
    same = 0
    missing = 0
    missing_files = []
    args = parse_all_args()
    all_files = []
    all_files2 = []
    for _, _, files in os.walk(args.first):
        for file in files:
            all_files.append(file)
    for _, _, files in os.walk(args.second):
        for file in files:
            all_files2.append(file)
    for file in all_files2:
        if file in all_files:
            same += 1
        else:
            missing += 1
            missing_files.append(file)
        print(
            f"\r{args.first}: ✅ file not missing: {same}; ❌ file missing: {missing}",
            end="",
        )
    print()
    write_missing_files_report(all_files, "first_path_report.txt", missing_files)
    # reset the counters
    same = 0
    missing = 0
    missing_files = []
    for file in all_files:
        if file in all_files2:
            same += 1
        else:
            missing += 1
            missing_files.append(file)
        print(
            f"\r{args.second}: ✅ file not missing: {same}; ❌ file missing: {missing}",
            end="",
        )
    print()
    write_missing_files_report(all_files2, "second_path_report.txt", missing_files)


if __name__ == "__main__":
    main()
