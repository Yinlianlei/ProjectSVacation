import re

if __name__ == "__main__":
    a = ["房事头疼症","龟头疼","受凉头疼","肺部转移"]

    for i in a:
        print(re.findall("[头疼]+",i))