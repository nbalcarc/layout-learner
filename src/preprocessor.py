import os
import shutil
from functools import reduce


valid_chars = "abcdefghijklmnopqrstuvwxyz "


def validize(input: str) -> str:
    """Remove all invalid characters."""
    adjusted = map(lambda x: x if x in valid_chars else "_" , input.lower())
    #collapsed = reduce(lambda a, x: a if x == "_" and a.endswith("_") else (a + x), adjusted)
    #print(collapsed)
    return "".join(list(adjusted))


def chunkify(input: str) -> list[str]:
    """Take a validized string and turn it into chunks."""
    return list(filter(lambda x: len(x) > 1, input.split("_")))


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


