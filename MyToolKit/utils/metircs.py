from scipy.stats import kendalltau, spearmanr, pearsonr


def kendall(ar1, ar2):
    return kendalltau(ar1, ar2)

def spearman(ar1, ar2):
    return spearmanr(ar1, ar2)

def pearson(ar1, ar2):
    return pearsonr(ar1, ar2)