import os
import re
import webbrowser
from datetime import datetime

def extract_file_id(url):
    if not url:
        return None
    
    match = re.search(r'/file/d/([a-zA-Z0-9_-]+)', url)
    if match:
        return match.group(1)
    
    match = re.search(r'[?&]id=([a-zA-Z0-9_-]+)', url)
    if match:
        return match.group(1)
    
    match = re.search(r'/d/([a-zA-Z0-9_-]+)', url)
    if match:
        return match.group(1)
    
    match = re.search(r'/d/([a-zA-Z0-9_-]+)=', url)
    if match:
        return match.group(1)
    
    return None

def convert_drive_url(url, width=1000):
    if not url:
        return url
    
    file_id = extract_file_id(url)
    if file_id:
        return f"https://drive.google.com/thumbnail?id={file_id}&sz=w{width}"
    return url

def get_datetime():
    print("\ndate and time (e.g., 24 jul 2026 21:25):")
    datetime_str = input("> ").strip()
    
    parts = datetime_str.split()
    if len(parts) < 5:
        print("error: invalid format")
        return get_datetime()
    
    date_str = " ".join(parts[:3])
    time_str = parts[3] + " " + parts[4] if len(parts) > 4 else parts[3]
    time_str = time_str.replace(':', ' ')
    
    return date_str, time_str

def get_post_name():
    print("\npost name (optional, press Enter to skip):")
    name = input("> ").strip()
    
    drive_url = "https://drive.google.com/drive/u/1/folders/1B49ekUuLaClK84bJ-IOBNTMkVpxNIl7M"
    
    print(f"\nopen Google Drive folder? (y/n):")
    choice = input("> ").strip().lower()
    
    if choice == 'y' or choice == 'yes':
        print(f"opening...")
        webbrowser.open(drive_url)
    else:
        print("skipping")
    
    return name

def generate_filename(date_str, time_str):
    parts = date_str.lower().split()
    day = parts[0].zfill(2)
    month_map = {
        'jan': 'jan', 'feb': 'feb', 'mar': 'mar', 'apr': 'apr',
        'may': 'may', 'jun': 'jun', 'jul': 'jul', 'aug': 'aug',
        'sep': 'sep', 'oct': 'oct', 'nov': 'nov', 'dec': 'dec'
    }
    month = month_map.get(parts[1][:3], parts[1][:3])
    year = parts[2]
    
    time_parts = time_str.split()
    hour = time_parts[0].zfill(2)
    minute = time_parts[1].zfill(2) if len(time_parts) > 1 else '00'
    
    return f"{day}{month}{year}_{hour}_{minute}.htm"

def generate_html(date_str, time_str, content_blocks):
    display_date = f"{date_str} {time_str.replace(' ', '/')}"
    
    html = f'''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2//EN">
<html>
<head>
    <title>blog</title>
    <link href="/images/favicon1.png" rel="icon" type="image/png" />
    <meta content="text/html; charset=iso-8859-1" http-equiv="Content-Type" />
</head>
<body style="background-color: #242448;">
<p>&nbsp;</p>

<table border="0" cellpadding="0" cellspacing="0" width="100%">
    <tbody>
        <tr>
            <td valign="top" width="1%">
            <div class="header">
            
            <h2>
            <span style="background-color: #ffffff">&nbsp;{display_date}&nbsp;</span>
            &nbsp;
            </h2>

            <a href="../index.htm"><span style="color: #00ffff; background-color: #000000">&nbsp;&lt; BACK &nbsp;</span></a>
'''
    
    for block in content_blocks:
        if block['type'] == 'text':
            html += f'''
            <p>
            <span style="color: #ffffff">{block['content']}</span>
            </p>
'''
        elif block['type'] == 'image':
            html += f'''
            <h2>
            <img border="0" hspace="0" src="{block['url']}" 
            style="width: 1000px; height: auto;" />
            </h2>
'''
    
    html += '''            
            </div>
            </td>
        </tr>
    </tbody>
</table>
</body>
</html>'''
    
    return html

def preview_post(date_str, time_str, post_name, content_blocks, filename):
    print("\n" + "="*50)
    print(f"Filename: {filename}")
    print(f"Date: {date_str}")
    print(f"Time: {time_str}")
    print(f"Post name: {post_name if post_name else '(none)'}")
    print("-"*50)
    
    for i, block in enumerate(content_blocks, 1):
        if block['type'] == 'text':
            print(f"{i}. [TEXT] {block['content'][:60]}...")
        elif block['type'] == 'image':
            display_url = block['url'][:40] + "..." if len(block['url']) > 40 else block['url']
            print(f"{i}. [IMAGE] {display_url}")
    
    print("="*50)
    confirm = input("\ncreate post? (y/n): ").strip().lower()
    return confirm == 'y' or confirm == ''

def update_index_page(filename, date_str, time_str, post_name):
    index_path = "index.htm"
    
    if not os.path.exists(index_path):
        print(f"Warning: {index_path} not found - index not updated")
        return
    
    display_date = date_str.replace(' ', '/')
    display_time = time_str.replace(' ', '/')
    
    name_display = f"&nbsp;- {post_name}&nbsp; " if post_name else "&nbsp; "
    
    new_entry = f'''&nbsp; <a  href="blog/{filename}" style="text-decoration:none">{display_date}&nbsp; {display_time}</a>{name_display}<br>'''
    
    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    pattern = r'(<span style="line-height:2; font-family: Sharp; background-color: #ffffff; padding:18px;">)'
    match = re.search(pattern, content)
    
    if match:
        insert_pos = match.end()
        content = content[:insert_pos] + '\n\t\t\t' + new_entry + content[insert_pos:]
        
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  Updated {index_path} with new entry")
    else:
        print(f"  Warning: Could not find entries section in {index_path}")

def main():
    date_str, time_str = get_datetime()
    post_name = get_post_name()
    
    filename = generate_filename(date_str, time_str)
    while os.path.exists(filename):
        print(f"\nWarning: {filename} already exists!")
        change = input("enter new date or press Enter to overwrite: ").strip()
        if not change:
            break
        date_str, time_str = get_datetime()
        filename = generate_filename(date_str, time_str)
    
    content_blocks = []
    
    while True:
        print("\nnext step:")
        print("1 - add text")
        print("2 - add image")
        print("3 - finish post")
        print("\naction: ", end="")
        choice = input().strip()
        
        if choice == '1':
            print("Text: ", end="")
            text = input().strip()
            if text:
                content_blocks.append({'type': 'text', 'content': text})
                print(f"  Added text block ({len(text)} chars)")
        
        elif choice == '2':
            print("image URL: ", end="")
            url = input().strip()
            if url:
                converted_url = convert_drive_url(url, 1000)
                
                if converted_url and converted_url != url:
                    print(f"  converted to: {converted_url[:60]}...")
                elif not converted_url:
                    converted_url = url
                    print("  using original URL")
                
                content_blocks.append({
                    'type': 'image',
                    'url': converted_url
                })
                print(f"added image")
        
        elif choice == '3':
            if not content_blocks:
                print("Error: no content")
                continue
            break
        
        else:
            print("Invalid choice")
    
    if preview_post(date_str, time_str, post_name, content_blocks, filename):
        html_content = generate_html(date_str, time_str, content_blocks)
        with open(f"blog/{filename}", 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"\nPost created: {filename}")
        print(f"Saved to: {os.path.abspath(filename)}")
        
        update_index_page(filename, date_str, time_str, post_name)
    else:
        print("Cancelled")

if __name__ == "__main__":
    main()