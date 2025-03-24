def xpath_soup(element):
    # type: (typing.Union[bs4.element.Tag, bs4.element.NavigableString]) -> str
    """
    Generate xpath from BeautifulSoup4 element.
    :param element: BeautifulSoup4 element.
    :type element: bs4.element.Tag or bs4.element.NavigableString
    :return: xpath as string
    :rtype: str
    Usage
    -----
    >>> import bs4
    >>> html = (
    ...     '<html><head><title>title</title></head>'
    ...     '<body><p>p <i>1</i></p><p>p <i>2</i></p></body></html>'
    ...     )
    >>> soup = bs4.BeautifulSoup(html, 'html.parser')
    >>> xpath_soup(soup.html.body.p.i)
    '/html/body/p[1]/i'
    >>> import bs4
    >>> xml = (
    ...     '<?xml version="1.0" encoding="UTF-8"?>'
    ...     '<doc xmlns:ns1="http://localhost/ns1"'
    ...     '     xmlns:ns2="http://localhost/ns2">'
    ...     '<ns1:elm/><ns2:elm/><ns2:elm/></doc>'
    ...     )
    >>> soup = bs4.BeautifulSoup(xml, 'lxml-xml')
    >>> xpath_soup(soup.doc.find('ns2:elm').next_sibling)
    '/doc/ns2:elm[2]'
    """
    components = []
    target = element if element.name else element.parent
    for node in (target, *target.parents)[-2::-1]:  # type: bs4.element.Tag
        tag = '%s:%s' % (node.prefix, node.name) if node.prefix else node.name
        siblings = node.parent.find_all(tag, recursive=False)
        components.append(tag if len(siblings) == 1 else '%s[%d]' % (tag, next(
            index
            for index, sibling in enumerate(siblings, 1)
            if sibling is node
        )))
    return '/%s' % '/'.join(components)


def nth_of_type(elem):
    count, curr = 0, 0
    for i, e in enumerate(elem.find_parent().find_all(recursive=False), 1):
        if e.name == elem.name:
            count += 1
        if e == elem:
            curr = i
    return '' if count == 1 else ':nth-of-type({})'.format(curr)


def get_css_selector(elem):
    rv = [elem.name + nth_of_type(elem)]
    while True:
        elem = elem.find_parent()
        if not elem or elem.name == '[document]':
            return ' > '.join(rv[::-1])
        rv.append(elem.name + nth_of_type(elem))
