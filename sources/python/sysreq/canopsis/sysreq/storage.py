from b3j0f.requester import FuncName

REQ2MON = {
    FuncName.EQ.value: '$eq',
    FuncName.GT.value: '$gt',
    FuncName.GTE.value: '$gte',
    FuncName.LT.value: '$lt',
    FuncName.LTE.value: '$lte',
    FuncName.NE.value: '$ne',
    FuncName.IN.value: '$in',
    FuncName.NIN.value: '$nin',
    FuncName.OR.value: '$or',
    FuncName.AND.value: '$and',
    FuncName.NOT.value: '$not',
    FuncName.NOR.value: '$nor',
    FuncName.EXISTS.value: '$exists',
    FuncName.MOD.value: '$mod',
    FuncName.REGEX.value: '$regex',
    FuncName.ALL.value: '$all',
}


def storagetranslator(pname, val, ctx):
    """Translator for mongo expressions."""
    if isinstance(val, dict):
        for key in list(val):
            item = val[key][0]

            if key in REQ2MON:
                val[REQ2MON[key]] = val.pop(key)

            if isinstance(item, dict):
                storagetranslator(pname, item, ctx)

    return val
