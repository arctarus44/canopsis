from canopsis.middleware.core import Middleware
from b3j0f.requester import (
    Expression as E, Function as F,
    Create as C, Read as R, Update as U, Delete as D, Join as J
)

sysreq = Middleware.get_middleware_by_uri('sysreq://')

# first scenario: alarm stat

sysreq.driver.read(
    select=(E.Alarms.state, E.count(E.Alarms.id)),
    query=F.between(
        E.Alarms.ts, [F.now() - 24 * 3600, F.now()]
    ) & F.in_('hg1', E.Context.hostgroups) & (E.Context.active == True),
    groupby=E.Alarms.state,
    join=J(
        scope=[E.Alarms, E.Context],
        query=E.Alarms.id == E.Context.id
    )
)


with sysreq.open() as transaction:

    transaction.read(
        select=E.count(E.Alarms),
        alias='alarmcount'
    )

    transaction.read(
        select=E.count(E.Alarms.id),
        query=E.Alarms.ack.ts > (E.Alarms.ts + (30 * 60)),
        alias='alarmnotsla'
    )

    transaction.read(
        select=E.alarmnotsla / E.alarmcount * 100,
        alias='alarmstat'
    )

# publish metric from alarm stat

with sysreq.open() as transaction:

    transaction.read(
        select=(
            E.count(
                E.Alarms.ack.ts > (E.Alarms.ts + (30 * 60))
            ) / E.count(E.Alarms) * 100
        ),
        alias='alarmstat'
    )

    transaction.create(
        E.Context,
        values={'type': 'metric', 'connector': 'canopsis'}
    )

    transaction.create(
        E.Perfdata,
        values={'value': E.alarmstat, 'name': 'alarmstat'}
    )


# with pbehavior (not downtime)
with sysreq.open() as transaction:

    transaction.read(
        select=(E.Alarms.state, E.count(E.Alarms.id)),
        query=(
            (E.now() - 24 * 3600).as_('dtstart') &
            E.Pbehavior.whois(
                None, E.dtstart, E.now(), {'pbehavior': {'$neq': 'downtime'}}
            ) &
            E.between(E.Alarms.ts, [E.now() - 24 * 3600, E.now()]) &
            E.in_('hg1', E.Context.hostgroups) &
            E.Context.active == True
        ),
        groupby=E.Alarms.state,
        join=J(
            query=E.Alarms.data_id == E.Context.id,
            scope=(E.Alarms, E.Context)
        )
    )

    ctx = transaction.open().read(
        select=(
            E.Context.component.as_('metric'),
            E.avg(E.Perfdata.value).as_('value')
        ),
        query=E.Perfdata.metric == 'sessionduration' &
        E.between(E.dtstart, E.now()),
        groupby=E.Context.component,
        alias='averages',
        join=J(
            query=E.Context.id == E.Perfdata.data_id,
            scope=(E.Context, E.Perfdata)
        )
    ).commit().ctx

    for perfdata in ctx['averages']:

        transaction.create(
            E.Perfdata,
            values=perfdata
        )
