import os
import difflib
import sys

def compare_dirs(dir1, dir2):
    """
    Compare two directories recursively and collect differences.
    """
    changes = []
    # Walk through dir1 for modified and removed
    for root, dirs, files in os.walk(dir1):
        rel_path = os.path.relpath(root, dir1)
        dir2_root = os.path.join(dir2, rel_path)

        if not os.path.exists(dir2_root):
            changes.append((rel_path, "Directory removed"))
            continue

        for file in files:
            file1 = os.path.join(root, file)
            rel_file = os.path.join(rel_path, file)
            file2 = os.path.join(dir2_root, file)
            if not os.path.exists(file2):
                changes.append((rel_file, "File removed"))
            else:
                try:
                    with open(file1, 'r', encoding='utf-8') as f1, open(file2, 'r', encoding='utf-8') as f2:
                        lines1 = f1.readlines()
                        lines2 = f2.readlines()
                    diff = difflib.unified_diff(lines1, lines2, fromfile=rel_file, tofile=rel_file)
                    diff_output = ''.join(diff)
                    if diff_output:
                        changes.append((rel_file, diff_output))
                except UnicodeDecodeError:
                    with open(file1, 'rb') as f1b, open(file2, 'rb') as f2b:
                        content1 = f1b.read()
                        content2 = f2b.read()
                    if content1 != content2:
                        changes.append((rel_file, "Binary files differ"))

    # Walk through dir2 for added
    for root, dirs, files in os.walk(dir2):
        rel_path = os.path.relpath(root, dir2)
        dir1_root = os.path.join(dir1, rel_path)
        if not os.path.exists(dir1_root):
            changes.append((rel_path, "Directory added"))
        for file in files:
            file2 = os.path.join(root, file)
            rel_file = os.path.join(rel_path, file)
            file1 = os.path.join(dir1_root, file)
            if not os.path.exists(file1):
                changes.append((rel_file, "File added"))

    return changes

def process_hunk_lines(hunk_lines, start_old, start_new):
    res = []
    i = 0
    current_old = start_old
    current_new = start_new
    while i < len(hunk_lines):
        if hunk_lines[i].startswith(' '):
            current_old += 1
            current_new += 1
            i += 1
            continue

        change_start_old = current_old
        change_start_new = current_new

        removes = []
        while i < len(hunk_lines) and hunk_lines[i].startswith('-'):
            removes.append(hunk_lines[i][1:])
            i += 1
            current_old += 1

        adds = []
        while i < len(hunk_lines) and hunk_lines[i].startswith('+'):
            adds.append(hunk_lines[i][1:])
            i += 1
            current_new += 1

        if removes and adds:
            res.append(f"  Modified at line {change_start_old} (original) / {change_start_new} (updated):")
            if len(removes) == len(adds) == 1:
                res.append(f"    From: {removes[0].rstrip()}")
                res.append(f"    To:   {adds[0].rstrip()}")
            else:
                res.append("    Removed:")
                for r in removes:
                    res.append(f"      {r.rstrip()}")
                res.append("    Added:")
                for a in adds:
                    res.append(f"      {a.rstrip()}")
        elif removes:
            res.append(f"  Removed at line {change_start_old}:")
            for r in removes:
                res.append(f"    {r.rstrip()}")
        elif adds:
            res.append(f"  Added at line {change_start_new}:")
            for a in adds:
                res.append(f"    {a.rstrip()}")

    return res

def summarize_diff(diff_output):
    lines = diff_output.splitlines()
    if not lines:
        return []

    # Skip --- and +++ lines
    summary = []
    hunk_lines = []
    for line in lines[2:]:
        if line.startswith('@@'):
            if hunk_lines:
                summary.extend(process_hunk_lines(hunk_lines, current_old, current_new))
            # Parse @@ 
            parts = line.split()
            old_info = parts[1].lstrip('-').split(',')
            new_info = parts[2].lstrip('+').split(',')
            current_old = int(old_info[0])
            current_new = int(new_info[0])
            hunk_lines = []
        else:
            hunk_lines.append(line)

    if hunk_lines:
        summary.extend(process_hunk_lines(hunk_lines, current_old, current_new))

    return summary

def generate_pr_template(project_name, changes):
    summary_sections = []
    for file, change in changes:
        section = f"- {file}:"
        if change == "File added":
            section += "\n  New file added. <ENTER DETAILS HERE>"
        elif change == "File removed":
            section += "\n  File removed. <ENTER REASON HERE>"
        elif change == "Directory added":
            section += "\n  New directory added. <ENTER DETAILS HERE>"
        elif change == "Directory removed":
            section += "\n  Directory removed. <ENTER REASON HERE>"
        elif change == "Binary files differ":
            section += "\n  Binary content updated. <ENTER DETAILS HERE>"
        else:
            diff_summary = summarize_diff(change)
            if diff_summary:
                section += "\n" + "\n".join(diff_summary)
            else:
                section += "\n  No detailed changes detected."
        summary_sections.append(section)

    changes_summary = "\n".join(summary_sections) if summary_sections else "No changes detected."

    pr_template = f"""<!--
Thank you for contributing to {project_name}!
Please replace the bracketed sections with the relevant information.
-->
# Description
Please include a summary of the change and which issue or bug is fixed. Also, include relevant motivation and context.
Summary of changes:
{changes_summary}

* Fixes #<ENTER ISSUE NUMBER>
* Related to #<ENTER ISSUE NUMBER> (if applicable)
## Type of change
Please delete options that are not relevant.
- [x] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update
- [ ] Refactor (code change that neither fixes a bug nor adds a feature)
# How Has This Been Tested?
Please describe the tests that you ran to verify your changes. Provide instructions so we can reproduce.
<ENTER INFO HERE>
- [ ] Unit Tests
- [ ] Integration Tests
- [ ] Manual Testing (provide steps below)
**Test Configuration**:
* <ENTER CONFIGURATION DETAILS, e.g., environment, OS, browser, etc.>
# Checklist:
- [ ] My code follows the project's code style, guidelines, and best practices.
- [ ] I have performed a self-review of my own code.
- [ ] I have commented my code, particularly in hard-to-understand areas.
- [ ] I have made corresponding changes to the documentation (if applicable).
- [ ] My changes generate no new warnings or errors.
- [ ] I have added tests that prove my fix is effective or my feature works.
- [ ] New and existing tests pass locally with my changes.
- [ ] I have included screenshots or recordings for UI changes (if applicable).
# Additional Information (Optional)
* Any performance or accessibility concerns? <ENTER INFO HERE>
* Screenshots/GIFs: [Add them here if applicable]
* @mentions of the person or team responsible for reviewing proposed changes. <ENTER INFO HERE>
* Any post-deployment tasks? <ENTER INFO HERE>
"""
    return pr_template

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python compare_repos.py <dirA> <dirB>")
        sys.exit(1)
    dirA = sys.argv[1]
    dirB = sys.argv[2]
    print(f"Comparing {dirA} (base) to {dirB} (updated)\n")
    changes = compare_dirs(dirA, dirB)
    
    project_name = os.path.basename(os.path.normpath(dirA))
    pr_content = generate_pr_template(project_name, changes)
    print(pr_content)