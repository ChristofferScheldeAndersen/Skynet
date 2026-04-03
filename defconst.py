import re

input_fil = "anti_overkill.per"
output_fil = "anti_overkill_ny.per"

with open(input_fil, "r", encoding="utf-8") as f:
    text = f.read()

goal_pattern = r"gl-[A-Za-z0-9?-]+"


def get_pair(goal):
    if "-x-" in goal:
        return goal, goal.replace("-x-", "-y-")
    if "-y-" in goal:
        return goal.replace("-y-", "-x-"), goal
    if goal.endswith("-x"):
        return goal, goal[:-2] + "-y"
    if goal.endswith("-y"):
        return goal[:-2] + "-x", goal
    return None


# Find eksisterende defconsts
existing_defs = re.findall(
    r"^\(defconst\s+(gl-[A-Za-z0-9?-]+)\s+(\d+)\)\s*$",
    text,
    flags=re.M,
)

existing_order = [goal for goal, _ in existing_defs]
existing_numbers = {goal: int(number) for goal, number in existing_defs}

# Fjern gamle defconst-linjer fra body
body = re.sub(
    r"^\(defconst\s+gl-[A-Za-z0-9?-]+\s+\d+\)\s*\n?",
    "",
    text,
    flags=re.M,
)

# Find alle goals i body i første-forekomst-rækkefølge
body_goals = []
seen = set()

for match in re.finditer(goal_pattern, body):
    goal = match.group(0)
    if goal not in seen:
        body_goals.append(goal)
        seen.add(goal)

# Samlet rækkefølge: først gamle defconst-goals, derefter nye fra body
all_goals = []
seen = set()

for goal in existing_order + body_goals:
    if goal not in seen:
        all_goals.append(goal)
        seen.add(goal)

# Goals som skal have nye tal:
# - helt nye goals
# - x/y-par hvor den ene mangler, så begge i parret flyttes sammen
to_reassign = set()

for goal in all_goals:
    pair = get_pair(goal)

    if pair is None:
        if goal not in existing_numbers:
            to_reassign.add(goal)
    else:
        x_goal, y_goal = pair
        x_exists = x_goal in existing_numbers
        y_exists = y_goal in existing_numbers

        if not x_exists or not y_exists:
            to_reassign.add(x_goal)
            to_reassign.add(y_goal)

# Lav rækkefølgen for de goals der skal have nye tal
reassign_order = []
placed = set()

for goal in all_goals:
    pair = get_pair(goal)

    if pair is None:
        if goal in to_reassign and goal not in placed:
            reassign_order.append(goal)
            placed.add(goal)
    else:
        x_goal, y_goal = pair
        if x_goal in to_reassign or y_goal in to_reassign:
            if x_goal not in placed:
                reassign_order.append(x_goal)
                placed.add(x_goal)
            if y_goal not in placed:
                reassign_order.append(y_goal)
                placed.add(y_goal)

# Sikkerhed: hvis et partner-goal blev tilføjet men ikke set i all_goals
for goal in to_reassign:
    if goal not in placed:
        reassign_order.append(goal)
        placed.add(goal)

# Start nye tal efter største eksisterende tal
next_number = max(existing_numbers.values(), default=999) + 1

new_numbers = {}
for goal in reassign_order:
    new_numbers[goal] = next_number
    next_number += 1

# Uændrede defconsts bevarer tal og rækkefølge
unchanged_goals = [goal for goal in existing_order if goal not in to_reassign]

# Skriv ny fil
with open(output_fil, "w", encoding="utf-8") as f:
    for goal in reassign_order:
        f.write(f"(defconst {goal} {new_numbers[goal]})\n")

    if unchanged_goals:
        f.write("\n")
        for goal in unchanged_goals:
            f.write(f"(defconst {goal} {existing_numbers[goal]})\n")

    f.write("\n")
    f.write(body.lstrip("\n"))

# Print resultat
print("Ny-/omnummererede goals:")
for goal in reassign_order:
    print(f"(defconst {goal} {new_numbers[goal]})")

print("\nUændrede goals:")
for goal in unchanged_goals:
    print(f"(defconst {goal} {existing_numbers[goal]})")
