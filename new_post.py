import os
os.system("")
import re
import webbrowser
from datetime import datetime
from colorist import vga, bg_vga

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

from datetime import datetime

def get_datetime():
    vga("\ndate and time (e.g., 24 jul 2026 21:25 or freeform, leave empty for current):", 6)
    datetime_str = input("> ").strip()
    
    if not datetime_str:
        now = datetime.now()
        datetime_str = now.strftime("%d %b %Y %H:%M")
        print(f"\nParsed: {datetime_str}")
        parts = datetime_str.split()
        if len(parts) >= 5:
            date_str = " ".join(parts[:3])
            time_str = parts[3] + " " + parts[4]
            return date_str, time_str
        elif len(parts) == 4:
            date_str = " ".join(parts[:3])
            time_parts = parts[3].split(':')
            if len(time_parts) == 2:
                time_str = time_parts[0] + " " + time_parts[1]
                return date_str, time_str
        return datetime_str, None
    
    parts = datetime_str.split()
    if len(parts) < 5:
        if len(parts) == 4:
            time_parts = parts[3].split(':')
            if len(time_parts) == 2:
                date_str = " ".join(parts[:3])
                time_str = time_parts[0] + " " + time_parts[1]
                return date_str, time_str
        return datetime_str, None
    
    date_str = " ".join(parts[:3])
    time_str = parts[3] + " " + parts[4] if len(parts) > 4 else parts[3]
    time_str = time_str.replace(':', ' ')
    
    print(f"\nParsed: {date_str} {time_str}")
    
    return date_str, time_str

def get_post_name():
    vga("\npost name (optional, press Enter to skip):", 6)
    name = input("> ").strip()
    
    drive_url = "https://drive.google.com/drive/u/1/folders/1B49ekUuLaClK84bJ-IOBNTMkVpxNIl7M"
    
    vga(f"\nopen Google Drive folder? (y/n):", 3)
    choice = input("> ").strip().lower()
    
    if choice == 'y' or choice == 'yes':
        print(f"opening...")
        webbrowser.open(drive_url)
    else:
        print("skipping")
    
    return name

def generate_filename(date_str, time_str):
    if time_str is None:
        filename = date_str.lower().replace(' ', '_').replace('/', '_').replace('\\', '_')
        filename = re.sub(r'[^a-z0-9_-]', '_', filename)
        return f"{filename}.htm"
    
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

def format_display_date(date_str, time_str):
    if time_str is None:
        return f"&nbsp;{date_str}&nbsp;"
    
    parts = date_str.lower().split()
    day = parts[0]
    month = parts[1][:3]
    year = parts[2]
    
    if len(day) == 1:
        return f"&nbsp;{day}/{month}/{year}"
    return f"{day}/{month}/{year}"

def format_display_time(time_str, for_post=False):
    if time_str is None:
        return "&nbsp;"
    
    time_parts = time_str.split()
    hour = time_parts[0]
    minute = time_parts[1] if len(time_parts) > 1 else '0'
    
    if len(minute) == 1:
        minute = '0' + minute
    
    if for_post:
        return f"{hour}/{minute}"
    else:
        if len(hour) == 1:
            return f"&nbsp;{hour}/{minute}"
        return f"{hour}/{minute}"

def generate_html(date_str, time_str, post_name, content_blocks):
    display_date = format_display_date(date_str, time_str)
    display_time = format_display_time(time_str, for_post=False)
    
    if time_str is None:
        name_display = f"&nbsp;- {post_name}&nbsp; " if post_name else "&nbsp; "
        header_display = f"{display_date}{name_display}"
    else:
        name_display = f"&nbsp;- {post_name}&nbsp; " if post_name else "&nbsp; "
        header_display = f"{display_date} {display_time}{name_display}"
    
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
            <span style="background-color: #ffffff">{header_display}</span>
            &nbsp;
            </h2>

            <a href="../index.htm"><span style="color: #00ffff; background-color: #000000">&nbsp;&lt; BACK &nbsp;</span></a>
'''
    
    for block in content_blocks:
        if block['type'] == 'text':
            html += f'''
            <br><p>
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
        elif block['type'] == 'link':
            html += f'''
            <p>
            <a style="color: #ffffff; background-color: #000; padding: 5px 86px;" href="{block['href']}">&nbsp;{block['text']}&nbsp;</a>
            </p>
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
    print("\n" + "="*100)
    print(f"Filename: {filename}")
    display_date = format_display_date(date_str, time_str)
    display_time = format_display_time(time_str, for_post=True)
    if time_str is None:
        print(f"Date/Time: {display_date.strip()}")
    else:
        print(f"Date: {date_str}")
        print(f"Time: {time_str}")
    print(f"Post name: {post_name if post_name else '(none)'}")
    print("-"*100)
    
    for i, block in enumerate(content_blocks, 1):
        if block['type'] == 'text':
            print(f"{i}. [TEXT] {block['content']}")
        elif block['type'] == 'image':
            print(f"{i}. [IMAGE] {block['url']}")
        elif block['type'] == 'link':
            print(f"{i}. [LINK] {block['text']} -> {block['href']}")
    
    print("="*100)
    confirm = input("\ncreate post? (y/n): ").strip().lower()
    return confirm == 'y' or confirm == ''

def update_index_page(filename, date_str, time_str, post_name):
    index_path = "index.htm"
    
    vga(f"\nupdate index.htm? (y/n):", 3)
    choice = input("> ").strip().lower()
    
    if choice == 'y' or choice == 'yes':
        print(f"updating...")
        
        if not os.path.exists(index_path):
            bg_vga(f"Warning: {index_path} not found - index not updated", 11)
            return
        
        if time_str is None:
            display_date = f"&nbsp;{date_str}&nbsp;"
            name_display = f"&nbsp;- {post_name}&nbsp; " if post_name else "&nbsp; "
            new_entry = f'''&nbsp; <a  href="blog/{filename}" style="text-decoration:none">{display_date}</a>{name_display}<br>'''
        else:
            display_date = format_display_date(date_str, time_str)
            display_time = format_display_time(time_str, for_post=False)
            name_display = f"&nbsp;- {post_name}&nbsp; " if post_name else "&nbsp; "
            new_entry = f'''&nbsp; <a  href="blog/{filename}" style="text-decoration:none">{display_date} {display_time}</a>{name_display}<br>'''
        
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
            bg_vga(f"  Warning: Could not find entries section in {index_path}", 11)
    else:
        print("skipping")

def main():
    date_str, time_str = get_datetime()
    post_name = get_post_name()
    
    filename = generate_filename(date_str, time_str)
    while os.path.exists(f"blog/{filename}"):
        print(f"\nWarning: {filename} already exists!")
        change = input("enter new date or press Enter to overwrite: ").strip()
        if not change:
            break
        date_str, time_str = get_datetime()
        filename = generate_filename(date_str, time_str)
    
    content_blocks = []
    
    while True:
        bg_vga("\nnext step:", 6)
        print("1 - add text")
        print("2 - add image")
        print("3 - add link")
        print("4 - finish post")
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
                    bg_vga(f"  converted to: {converted_url[:60]}...", 6)
                elif not converted_url:
                    converted_url = url
                    bg_vga("  using original URL", 6)
                
                content_blocks.append({
                    'type': 'image',
                    'url': converted_url
                })
                print(f"added image")
        
        elif choice == '3':
            print("Link text: ", end="")
            link_text = input().strip()
            print("URL: ", end="")
            link_url = input().strip()
            if link_text and link_url:
                content_blocks.append({
                    'type': 'link',
                    'text': link_text,
                    'href': link_url
                })
                print(f"  Added link: {link_text} -> {link_url}")
        
        elif choice == '4':
            if not content_blocks:
                bg_vga("Error: no content", 1)
                continue
            break
        
        else:
            print("Invalid choice")
    
    if preview_post(date_str, time_str, post_name, content_blocks, filename):
        html_content = generate_html(date_str, time_str, post_name, content_blocks)
        os.makedirs("blog", exist_ok=True)
        with open(f"blog/{filename}", 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"\nPost created: {filename}")
        print(f"Saved to: {os.path.abspath(f'blog/{filename}')}")
        
        update_index_page(filename, date_str, time_str, post_name)
    else:
        print("Cancelled")

if __name__ == "__main__":
    main()