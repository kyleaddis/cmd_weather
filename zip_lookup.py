import argparse

file_path = "US.txt"


def find_zip(zip, details=False):
    with open(file_path, "r") as file:
        for line in file:
            row = line.strip().split("\t")
            if row[1] == zip:
                if details:
                    return row
                else:
                    return row[9], row[10]
        raise ValueError("Zip code not found")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Lookup latitude and longitude by zip code."
    )
    parser.add_argument("zip_code", type=str, help="Zip code for the location")
    parser.add_argument(
        "-d", "--details", action="store_true", help="Return all details"
    )
    args = parser.parse_args()

    print(find_zip(args.zip_code, args.details))
