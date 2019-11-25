import os
import sys
import re
import json


# Json field
# project_name
# roots
# database_loaded_time
# crates
# modules
# declarastions
# functions
# item_collection_time
# expressions
# unknown_types
# partial_unknown_types
# type_mismatches
# inferenece_time
# total_time

def get_next(content):
    line = next(content, None)
    # print(line)
    return line


def parse_stat(content):
    first = get_next(content)
    if first == None:
        return None

    name = re.search('run analysis-stats on (.*)', first).group(1)
    stat = dict()
    stat["project_name"] = name
    assert(get_next(content).startswith("====START"))
    try: 
        m = re.search(
            r"Database loaded, (\d+) roots, ([+-]?([0-9]*[.])?[0-9]+[m]?s)", get_next(content))
        stat["roots"] = int(m.group(1))
        stat["database_loaded_time"] = m.group(2)
        stat["crates"] = int(
            re.search(r"Crates in this dir: (.*)", get_next(content)).group(1))
        stat["modules"] = int(
            re.search(r"Total modules found: (.*)", get_next(content)).group(1))
        stat["declarations"] = int(
            re.search(r"Total declarations: (.*)", get_next(content)).group(1))
        stat["functions"] = int(
            re.search(r"Total functions: (.*)", get_next(content)).group(1))
        stat["item_collection_time"] = re.search(
            r"Item Collection: ([+-]?([0-9]*[.])?[0-9]+[m]?s)(.*)", get_next(content)).group(1)
        stat["expressions"] = int(
            re.search(r"Total expressions: (.*)", get_next(content)).group(1))
        stat["unknown_types"] = int(re.search(
            r"Expressions of unknown type: (\d+) (.*)", get_next(content)).group(1))
        stat["partial_unknown_types"] = int(re.search(
            r"Expressions of partially unknown type: (\d+) (.*)", get_next(content)).group(1))
        stat["type_mismatches"] = int(
            re.search(r"Type mismatches: (.*)", get_next(content)).group(1))
        stat["inferenece_time"] = re.search(
            r"Inference: ([+-]?([0-9]*[.])?[0-9]+[m]?s), (.*)", get_next(content)).group(1)
        stat["total_time"] = re.search(
            r"Total: ([+-]?([0-9]*[.])?[0-9]+[m]?s), (.*)", get_next(content)).group(1)    
        assert(get_next(content).startswith("====END"))
    except:
        stat["error"] = "fail to parse output"
        # skip to the end
        while True:
            if get_next(content).startswith("====END"):
                break

    return stat


def parser(content, last_commits):
    projects = []
    commit = get_next(content)
    commit_time = get_next(content)
    all_commits = last_commits["commits"]
    if not commit in all_commits:
        all_commits[commit] = commit_time
    while True:
        curr = parse_stat(content)
        if curr == None:
            break
        projects.append(curr)

    return (commit, projects)


txt_file = open(sys.argv[1])
commits_file = open(sys.argv[2])
content = iter(txt_file.read().splitlines())
commits = json.load(commits_file)
commits_file.close()
(commit, projects) = parser(content, commits)

output_json = "{}.json".format(commit)

projects_json = json.dumps(projects, indent=4, sort_keys=True)
commits_json = json.dumps(commits, indent=4, sort_keys=True)
output_path = os.path.join(sys.argv[3], os.path.basename(output_json))

open(output_path, "w").write(projects_json)
open(sys.argv[2], "w").write(commits_json)

print("done!")
