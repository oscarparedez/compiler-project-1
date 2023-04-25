def scan(tokens, headers_and_trailers):
    print("---------HEADERS---------")
    print(headers_and_trailers['headers'])
    print("---------HEADERS---------")
    print("---------TOKENS---------")
    for token in tokens:
        token = token.strip()
        exec(token)
    print("---------TOKENS---------")
    print("---------TRAILERS---------")
    print(headers_and_trailers['trailers'])
    print("---------TRAILERS---------")