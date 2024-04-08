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


def validize(input: str) -> str:
    """Remove all invalid characters."""
    fst = "".join(map(lambda x: x if x in valid_chars else ("-" if x in pseudo_chars else "_"), input.lower())) #remap all non-valid characters
    #note: dashes mean an empty character (space matters), underscores mean reset
    dash_flattened = flatten_series(fst, "-") #flatten all dashes
    return dash_flattened


def chunkify(input: str) -> list[str]:
    """Take a validized string and turn it into chunks."""
    splitted = input.split("_") #split on underscores
    cleansed = map(lambda x: x.strip("-"), splitted) #remove all starting and ending dashes
    no_shorts = filter(lambda x: len(x) > 4, cleansed) #remove all short lines
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
        chunked = chunkify(validized) #turn into valid chunks
        with open(post_dir, "w") as file: #output processed
            file.write("\n".join(chunked))


if __name__ == "__main__":
    main()


