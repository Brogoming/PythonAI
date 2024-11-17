PROBS = {
    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },
    "trait": {
        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },
        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },
        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },
    # Mutation probability
    "mutation": 0.01
}

def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """

    jointProb = 1
    for person in people.keys():
        personProb = 1
        if person in two_genes:
            genes = 2
        elif person in one_gene:
            genes = 1
        else:
            genes = 0
        trait = person in have_trait

        if people[person]['father'] is None and people[person]['mother'] is None:
            personProb *= PROBS['gene'][genes]
        else:
            dadProb = parentProbability(people[person]['father'], one_gene, two_genes)
            momProb = parentProbability(people[person]['mother'], one_gene, two_genes)

            if genes == 2:
                personProb *= momProb * dadProb
            elif genes == 1:
                personProb *= (1 - momProb) * dadProb + (1 - dadProb) * momProb
            else:
                personProb *= (1 - momProb) * (1 - dadProb)

        personProb *= PROBS['trait'][genes][trait]
        jointProb *= personProb
    return jointProb


def parentProbability(parent, one_gene, two_genes):
    if parent in two_genes:
        parentProb = 1 - PROBS['mutation']
    elif parent in one_gene:
        parentProb = 0.5
    else:
        parentProb = PROBS['mutation']
    return parentProb


print(joint_probability({'Harry': {'name': 'Harry', 'mother': 'Lily', 'father': 'James', 'trait': None},
                         'James': {'name': 'James', 'mother': None, 'father': None, 'trait': True},
                         'Lily': {'name': 'Lily', 'mother': None, 'father': None, 'trait': False}},
                        {"Harry"}, {"James"}, {"Harry", "James"}))


def update(probabilities, one_gene, two_genes, have_trait, p):
    for person in probabilities.keys():
        if person in two_genes:
            probabilities[person]["gene"][2] += p
        elif person in one_gene:
            probabilities[person]["gene"][1] += p
        else:
            probabilities[person]["gene"][0] += p

        if person in have_trait:
            probabilities[person]["trait"][True] += p
        else:
            probabilities[person]["trait"][False] += p

    return probabilities


print(update({'Harry': {'gene': {2: 0, 1: 0, 0: 0}, 'trait': {True: 0, False: 0}},
              'James': {'gene': {2: 0, 1: 0, 0: 0}, 'trait': {True: 0, False: 0}},
              'Lily': {'gene': {2: 0, 1: 0, 0: 0}, 'trait': {True: 0, False: 0}}}, {"Harry"}, {"James"},
             {"Harry", "James"}, 0.008852852828159997))
