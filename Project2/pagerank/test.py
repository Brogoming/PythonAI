import random

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
    linkChance = damping_factor/len(corpus[page])
    if len(corpus[page]) != 0:
        for i in corpus.keys():
            transModel[i] = pageChance
            if i in corpus[page]:
                transModel[i] += linkChance
    else:
        for i in corpus.keys():
            transModel[i] = damping_factor / len(corpus) + pageChance

    return transModel


# print(transition_model({"1.html": {"2.html", "3.html"}, "2.html": {"3.html"}, "3.html": {"2.html"}},"1.html", 0.85))

def sample_pagerank(corpus, damping_factor, n):
    samplePR = {page_name: 0 for page_name in corpus}
    page = random.choice(list(corpus.keys()))
    samplePR[page] += 1/n
    totalProb = 0
    for i in range(1, n):
        transModel = transition_model(corpus, page, damping_factor)
        totalProb += transModel[page]
        page = random.choices(list(transModel.keys()), list(transModel.values()))[0]
        samplePR[page] += 1/n

    print('Sum of sample page ranks: ', round(sum(samplePR.values()), 4))
    return samplePR


# print(sample_pagerank({"1.html": {"2.html", "3.html"}, "2.html": {"3.html"}, "3.html": {"2.html"}}, 0.85, 1000))


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


print(iterate_pagerank({"1.html": {"2.html", "3.html"}, "2.html": {"3.html"}, "3.html": {"2.html"}}, 0.85))

# , "4.html": {}
