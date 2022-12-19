import pandas as pd


# simulate
def simulate(type_rn, demand_rn, order_quantity, sell_price, cost_price,
             scrap_value, news_values, news_probs, demand_values, good_demand_probs,
             fair_demand_probs, poor_demand_probs, days=10):
    table = {'day': [],
             'rnnt': [],
             'news_type': [],
             'rnd': [],
             'demand': [],
             'revenue': [],
             'cost': [],
             'lost_profit': [],
             'scrape': [],
             'daily_profit': []}
    cost = order_quantity * cost_price
    news_type_table = assign_rn(news_values, news_probs)
    good_demand_table = assign_rn(demand_values, good_demand_probs)
    fair_demand_table = assign_rn(demand_values[:-1], fair_demand_probs)
    poor_demand_table = assign_rn(demand_values[:-2], poor_demand_probs)

    for i in range(days):
        table['day'].append(i + 1)
        table['rnnt'].append(type_rn[i])
        table['news_type'].append(get_news_type(type_rn[i], news_type_table))
        table['rnd'].append(demand_rn[i])
        table['demand'].append(get_demand_value(demand_rn[i], get_demand_table(table['news_type'][i],
                                                                               good_demand_table, fair_demand_table, poor_demand_table)))
        table['revenue'].append(calc_revenue(
            order_quantity, table['demand'][i]) * sell_price)
        table['cost'].append(cost)
        table['lost_profit'].append(calc_lost_profit(
            order_quantity, table['demand'][i], sell_price, cost_price))
        table['scrape'].append(calc_scrape(
            order_quantity, table['demand'][i], scrap_value))
        table['daily_profit'].append(calc_daily_profit(
            table['revenue'][i], cost, table['lost_profit'][i], table['scrape'][i]))

    data = pd.DataFrame(table).reset_index(drop=True, inplace=True)
    data.head()
    return data

# assign random digits from cumulative probabilities


def assign_rn(values, probablities):
    dist_table = {}
    for v, i in zip(values, range(len(values))):
        dist_table[v] = [*range(int((sum(probablities[:i+1])-probablities[i])
                                * 100) + 1, int(sum(probablities[:i+1]) * 100) + 1)]
    return dist_table


def get_news_type(rn, rn_news_table):
    for i in range(len(rn_news_table)):
        if rn in rn_news_table[list(rn_news_table.keys())[i]]:
            return list(rn_news_table.keys())[i]


def get_demand_value(rn, demand_table):
    for i in range(len(demand_table)):
        if rn in demand_table[list(demand_table.keys())[i]]:
            return list(demand_table.keys())[i]

# returns whether the good table, fair table, or poor table


def get_demand_table(news, g, f, p):
    if news == "good":
        return g
    elif news == "fair":
        return f
    else:
        return p


def calc_revenue(q, d):
    return q if q <= d else d


def calc_lost_profit(q, d, s, c):
    return (d - q) * (s - c) if q < d else 0


def calc_scrape(q, d, scrape):
    return (q - d) * scrape if q > d else 0


def calc_daily_profit(r, c, lp, sr):
    return r - c - lp if sr == 0 else r - c + sr


def write_to_csv(df, path):
    df.to_csv(path)
