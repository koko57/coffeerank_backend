from math import ceil

ENTRIES_PER_PAGE = 10

def paginate_results(page, results):
    start = (page - 1) * ENTRIES_PER_PAGE
    end = start + ENTRIES_PER_PAGE

    results_count = len(results)
    pages = ceil(results_count / ENTRIES_PER_PAGE)
    
    data = {
        "coffees": results[start:end],
        "pages": pages,
        "results_count": results_count
    }

    return data
