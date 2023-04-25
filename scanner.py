def scan(tokens, headers_and_trailers):
    with open('result.py', 'w') as f:
        headers_and_trailers['headers'] = headers_and_trailers['headers'].split('*)')
        for header in headers_and_trailers['headers']:
            header = header.replace('(*', '')
            header = header.replace('*)', '').strip()
            if not (header.startswith('print') or header.startswith('return') or header.startswith('if') \
            or header.startswith('else') or header.startswith('def')):
                f.write('#' + header + '\n')
            else:
                f.write(header + '\n')
    
        for token in tokens:
            token = token.strip()
            f.write(token + '\n')

        headers_and_trailers['trailers'] = headers_and_trailers['trailers'].split('*)')

        for trailer in headers_and_trailers['trailers']:
            trailer = trailer.replace('(*', '')
            trailer = trailer.replace('*)', '').strip()
            if not (trailer.startswith('print') or trailer.startswith('return') or trailer.startswith('if') \
            or trailer.startswith('else') or trailer.startswith('def')):
                f.write('#' + trailer + '\n')
            else:
                f.write(trailer + '\n')

        
