import os
import io

def generate_pdf_bytes(title, subtitle, meta_line, sections):
    """
    Generates a valid PDF-1.4 binary stream with title, subtitle, metadata, and sections.
    Zero external dependencies required.
    """
    def escape_pdf(text):
        if text is None:
            text = ""
        return str(text).replace('\\', '\\\\').replace('(', '\\(').replace(')', '\\)')
        
    content_lines = [
        'BT',
        '/F1 18 Tf',
        '50 740 Td',
        f'({escape_pdf(title)}) Tj',
        '/F1 12 Tf',
        '0 -24 Td',
        f'({escape_pdf(subtitle)}) Tj',
        '/F2 10 Tf',
        '0 -20 Td',
        f'({escape_pdf(meta_line)}) Tj',
        '/F1 10 Tf',
        '0 -14 Td',
        '(---------------------------------------------------------------------------------------------------------------------------------) Tj',
    ]
    
    for header, rows in sections:
        content_lines.extend([
            '/F1 12 Tf',
            '0 -22 Td',
            f'({escape_pdf(header)}) Tj',
            '/F2 10 Tf',
            '0 -16 Td'
        ])
        for r in rows:
            content_lines.extend([
                f'({escape_pdf(r)}) Tj',
                '0 -14 Td'
            ])
            
    content_lines.append('ET')
    stream_data = '\n'.join(content_lines).encode('latin1', errors='replace')
    stream_len = len(stream_data)
    
    objects = [
        b'1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n',
        b'2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n',
        b'3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R /F2 6 0 R >> >> >>\nendobj\n',
        f'4 0 obj\n<< /Length {stream_len} >>\nstream\n'.encode('latin1') + stream_data + b'\nendstream\nendobj\n',
        b'5 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>\nendobj\n',
        b'6 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n'
    ]
    
    out = io.BytesIO()
    out.write(b'%PDF-1.4\n')
    offsets = [0]
    curr = len(b'%PDF-1.4\n')
    for obj in objects:
        offsets.append(curr)
        out.write(obj)
        curr += len(obj)
        
    xref_offset = curr
    out.write(f'xref\n0 {len(objects)+1}\n0000000000 65535 f \n'.encode('latin1'))
    for off in offsets[1:]:
        out.write(f'{off:010d} 00000 n \n'.encode('latin1'))
        
    out.write(f'trailer\n<< /Size {len(objects)+1} /Root 1 0 R >>\nstartxref\n{xref_offset}\n%%EOF\n'.encode('latin1'))
    return out.getvalue()
