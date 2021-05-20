from sqlalchemy import event
from models.frog import Frog

from datetime import datetime, timezone

from core import db
from constants import (TIME_INTERVAL, FOOD_DECREASE, CLEANLINESS_DECREASE, MAX_MONEY,
                       MAX_FOOD, MAX_CLEANLINESS, PRIMARY_INCOME, SECONDARY_INCOME)


def _count_periods(current, secondary_bound, decrease, maxsumperiods):
    '''
    Count periods before secondary_bound (primary)
    and between secondary_bound and 0 (secondary)
    from the given value.

    Params:
    current: int - value before the first period
    secondary_bound: int - value marks the boundary between primary and secondary periods
    decrease: int - value reduce after each period
    maxsumperiods: int - maximal number of periods allowed

    Returns:
    (primary_periods, secondary_periods): (int, int)
    '''
    secondary_periods = 0
    primary_periods = 0

    if current > secondary_bound:
        max_periods = int((current - secondary_bound) / decrease)
        primary_periods = min(max_periods, maxsumperiods)
        if primary_periods < maxsumperiods:
            max_periods = int(secondary_bound / decrease)
            secondary_periods = min(max_periods, maxsumperiods-primary_periods)
    else:  # only secondary income
        max_periods = int(current / decrease)
        secondary_periods = min(max_periods, maxsumperiods)
    return primary_periods, secondary_periods


@event.listens_for(Frog, 'load')
def on_frog_load(target, context):
    periods = int((datetime.now(timezone.utc) - target.last_request)/TIME_INTERVAL)

    # count income
    food_primary, food_secondary = _count_periods(
        target.food, int(MAX_FOOD/2), FOOD_DECREASE, periods
        )

    clean_primary, clean_secondary = _count_periods(
        target.cleanliness, int(MAX_CLEANLINESS/2), CLEANLINESS_DECREASE, periods
        )

    if food_primary > clean_primary:
        primary = clean_primary
        secondary = clean_secondary
    elif food_primary < clean_primary:
        primary = food_primary
        secondary = food_secondary
    else:
        primary = food_primary
        secondary = min(clean_secondary, food_secondary)

    income = PRIMARY_INCOME*primary + SECONDARY_INCOME*secondary

    target.money = min(MAX_MONEY, income + target.money)
    target.food -= min(target.food, periods*FOOD_DECREASE)
    target.cleanliness -= min(target.cleanliness, periods*CLEANLINESS_DECREASE)

    target.last_request = target.last_request + periods*TIME_INTERVAL
    db.session.merge(target)
    db.session.commit()
