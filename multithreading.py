import argparse
import multiprocessing

parser = argparse.ArgumentParser()
parser.add_argument("numProcess", type=int, help="num of processes")
args = parser.parse_args()

def printDomains(domains):
    for entry in domains:
        print (entry)

if __name__ == '__main__':
    # 1 - 99 list
    someDomains = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25,26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99]

    processes = args.numProcess
    if processes > 10:
        processes = 10

    splitBy = int(len(someDomains)/processes)
    chunks = [someDomains[x:x+splitBy] for x in range(0, len(someDomains), splitBy)]
    print(chunks)

    threadList = []
    count = 0

    while True:
        try:
            threadList.append(multiprocessing.Process(target=printDomains, args=(chunks[count],)))
            threadList[count].start()
            print("Process {} starting\n".format(count))
            threadList[count].join()
            count += 1
        except:
            break
