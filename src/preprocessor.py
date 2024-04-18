import os
import shutil
from functools import reduce


valid_chars = "abcdefghijklmnopqrstuvwxyz"
pseudo_chars = " ,./?!;:'\"&()-"


def flatten_series(input: str, c: str) -> str:
    """Flatten any repeats of the given char in the string."""
    remove_list = set()
    for i in range(1, len(input)):
        if input[i] == c and input[i-1] == c:
            remove_list.add(i)

    filtered = map(lambda x: x[1], filter(lambda x: x[0] not in remove_list, enumerate(input)))
    return "".join(filtered)


def flatten_series_map(input: str, c_from: str, c_to: str, threshold: int) -> str:
    """Flatten any repeats of the given char in the string into a new char."""
    collected: list[str] = []
    count = 0
    for ci in input:
        if ci == c_from: #continue the chain
            count += 1
        elif count == 0: #no chain
            collected.append(ci)
        elif count <= threshold: #chain was threshold or less long
            collected.append(c_from)
            collected.append(ci)
            count = 0
        else: #chain was more than threshold long
            collected.append(c_to)
            collected.append(ci)
            count = 0

    #return reduce(lambda a, x: a + x, collected)
    return "".join(collected)


def validize(input: str) -> str:
    """Remove all invalid characters."""
    fst = "".join(map(lambda x: x if x in valid_chars else ("-" if x in pseudo_chars else "_"), input.lower())) #remap all non-valid characters
    #note: dashes mean an empty character (space matters), underscores mean reset
    dash_flattened = flatten_series_map(fst, "-", "+", 1) #flatten all dashes
    return dash_flattened


def chunkify(input: str, min_length: int) -> list[str]:
    """Take a validized string and turn it into chunks."""
    #replaced = input.replace("+", "\n") #replace repeats with newlines
    #splitted = replaced.split("_") #split on underscores
    splitted = input.split("_") #split on underscores
    splitted_more = reduce(lambda a, x: a + x, list(map(lambda x: x.split("+"), splitted))) #split on plus
    cleansed = map(lambda x: x.strip("-").strip("+"), splitted_more) #remove all starting and ending dashes
    no_shorts = filter(lambda x: len(x) > min_length - 1, cleansed) #remove all short lines
    return list(no_shorts)


def main():
    """Main entry point."""
    processed_dir = "../data/processed"
    raw_dir = "../data"

    # setup
    if os.path.isdir(processed_dir):
        shutil.rmtree(processed_dir)
    os.mkdir(processed_dir)

    # get all files, map to input and output directories
    file_dirs = (
        map(lambda x: (raw_dir + "/" + x, processed_dir + "/" + x),
            filter(lambda x: x.endswith(".txt"), 
                os.listdir("../data")
            )
        )
    )

    # iterate through all inputs
    for pre_dir, post_dir in file_dirs:
        with open(pre_dir, "r") as file: #read input
            text = file.read()
        validized = validize(text) #remove all invalid characters
        chunked = chunkify(validized, 60) #turn into valid chunks
        with open(post_dir, "w") as file: #output processed
            file.write("\n".join(chunked))


if __name__ == "__main__":
    main()


