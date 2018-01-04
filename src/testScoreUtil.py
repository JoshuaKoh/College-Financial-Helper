def normalizeSAT(score):
    low = 200
    high = 800
    normalized = (score - low) / (high - low)
    return normalized


def normalizeCMSAT(score):
    low = 400
    high = 1600
    normalized = (score - low) / (high - low)
    return normalized


def normalizeACT(score):
    low = 1
    high = 36
    normalized = (score - low) / (high - low)
    return normalized
