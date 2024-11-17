import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    transModel = {}
    pageChance = (1 - damping_factor) / len(corpus)
    if len(corpus[page]) != 0:
        for i in corpus.keys():
            transModel[i] = pageChance
        for link in corpus[page]:
            transModel[link] += damping_factor / len(corpus[page])
    else:
        for i in corpus.keys():
            transModel[i] = damping_factor / len(corpus) + pageChance

    return transModel


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    samplePR = {page_name: 0 for page_name in corpus}
    page = random.choice(list(corpus.keys()))
    samplePR[page] += 1 / n
    totalProb = 0
    for i in range(1, n):
        transModel = transition_model(corpus, page, damping_factor)
        totalProb += transModel[page]
        page = random.choices(list(transModel.keys()), list(transModel.values()))[0]
        samplePR[page] += 1 / n
    return samplePR


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    newRanks = {page_name: 1/len(corpus) for page_name in corpus}  # each page with current rank values
    currentRanks = newRanks.copy()
    while True:
        for page in corpus.keys():
            linkPages = []  # pages that link to this page
            newRanks[page] = (1 - damping_factor) / len(corpus)
            for pageLink in corpus.keys():
                if page in corpus[pageLink]:
                    linkPages.append(pageLink)
            summationVal = 0
            for parPage in linkPages:
                summationVal += currentRanks[parPage] / len(corpus[parPage])
            newRanks[page] += damping_factor * summationVal
        if any(abs(currentRanks[page] - newRanks[page]) <= 0.001 for page in corpus.keys()):
            break
        currentRanks = newRanks.copy()
    # print('Sum of iterate page ranks: ', round(sum(newRanks.values()), 4))
    return newRanks


if __name__ == "__main__":
    main()
