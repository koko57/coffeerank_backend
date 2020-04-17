ENTRIES_PER_PAGE = 10


def paginate_results(page, results):
    start = (page - 1) * ENTRIES_PER_PAGE
    end = start + ENTRIES_PER_PAGE

    coffees = [coffee.format() for coffee in results]
    displayed_coffees = coffees[start:end]

    return displayed_coffees