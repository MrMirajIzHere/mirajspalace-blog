import os
os.system("")
import re
import webbrowser
import textwrap
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
            <span style="background-color: #ffffff">&nbsp;{header_display}</span>
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

def show_preview(date_str, time_str, post_name, content_blocks, filename):
    print("\n" + "="*100)
    print(" " * 44 + "POST PREVIEW" + " " * 44)
    print("="*100)
    
    display_date = format_display_date(date_str, time_str)
    display_time = format_display_time(time_str, for_post=True)
    
    if time_str is None:
        print(f"Date: {display_date.strip()}")
    else:
        print(f"Date: {date_str}")
        print(f"Time: {time_str}")
    
    if post_name:
        print(f"Name: {post_name}")
    
    print("-"*100)
    
    if not content_blocks:
        print("(no content yet)")
    else:
        for i, block in enumerate(content_blocks, 1):
            if block['type'] == 'text':
                content = block['content']
                content = content.replace('<br>', '\n')
                
                prefix = f"{i}. [TEXT] "
                indent = ' ' * len(prefix)
                
                lines = content.split('\n')
                wrapped_lines = []
                
                for line in lines:
                    if not line.strip():
                        wrapped_lines.append('')
                    else:
                        wrapped = textwrap.wrap(line, width=96)
                        wrapped_lines.extend(wrapped)
                
                output_parts = []
                for idx, line in enumerate(wrapped_lines):
                    if idx == 0:
                        output_parts.append(f"{prefix}{line}")
                    else:
                        output_parts.append(f"{indent}{line}")
                
                print('\n'.join(output_parts))
                
            elif block['type'] == 'image':
                url_preview = block['url'][:96] + '...' if len(block['url']) > 96 else block['url']
                print(f"{i}. [IMAGE] {url_preview}")
                
            elif block['type'] == 'link':
                link_text = f"{i}. [LINK] {block['text']} -> {block['href']}"
                if len(link_text) <= 100:
                    print(link_text)
                else:
                    prefix = f"{i}. [LINK] "
                    indent = ' ' * len(prefix)
                    parts = link_text.split(' -> ')
                    if len(parts) == 2:
                        print(f"{prefix}{parts[0]} ->")
                        url_parts = textwrap.wrap(parts[1], width=96 - len(indent))
                        for idx, url_part in enumerate(url_parts):
                            if idx == 0:
                                print(f"{indent}{url_part}")
                            else:
                                print(f"{indent}{url_part}")
                    else:
                        wrapped = textwrap.wrap(link_text, width=100)
                        for idx, line in enumerate(wrapped):
                            if idx == 0:
                                print(line)
                            else:
                                print(f"{' ' * len(prefix)}{line}")
    
    print("="*100)

def edit_content_block(content_blocks, date_str, time_str, post_name, filename):
    if not content_blocks:
        vga("\nNo content to edit.", 11)
        return
    
    while True:
        os.system('cls')
        show_preview(date_str, time_str, post_name, content_blocks, filename)
        
        print("\nEnter block number to edit (Enter to finish):")
        choice = input("> ").strip()
        
        if not choice:
            vga("Exiting edit mode.", 11)
            break
        
        if not choice.isdigit():
            vga("Invalid choice. Please enter a number.", 11)
            continue
        
        block_num = int(choice) - 1
        if block_num < 0 or block_num >= len(content_blocks):
            vga(f"Invalid block number. Choose 1-{len(content_blocks)}.", 11)
            continue
        
        block = content_blocks[block_num]
        
        if block['type'] == 'text':
            edit_text_block(block)
        elif block['type'] == 'image':
            edit_image_block(block)
        elif block['type'] == 'link':
            edit_link_block(block)
        
        vga("\nBlock updated", 2)

def edit_text_block(block):
    print("\n--- Editing Text Block ---")
    vga("Current text:", 14)
    lines = block['content'].split('<br>')
    for i, line in enumerate(lines, 1):
        print(f"  {i:2d}: {line}")
    
    while True:
        print("\nEnter line number to edit (Enter to finish):")
        line_choice = input("> ").strip()
        
        if not line_choice:
            break
        
        if not line_choice.isdigit():
            vga("Invalid choice. Please enter a number.", 11)
            continue
        
        line_num = int(line_choice) - 1
        if line_num < 0 or line_num >= len(lines):
            vga(f"Invalid line number. Choose 1-{len(lines)}.", 11)
            continue
        
        current_line = lines[line_num]
        vga(f"Current line: {current_line}", 14)
        print("Enter new text (Enter to keep)")
        new_line = input("> ").strip()
        
        if new_line:
            lines[line_num] = new_line
            vga(f"Line {line_num + 1} updated.", 2)
        else:
            vga("Line unchanged.", 2)
        
        print("\nUpdated text:")
        for i, line in enumerate(lines, 1):
            print(f"  {i:2d}: {line}")
    
    block['content'] = '<br>'.join(lines)

def edit_image_block(block):
    print("\n--- Editing Image Block ---")
    vga(f"Current URL: {block['url']}", 14)
    print("Enter new URL (Enter to keep)")
    new_url = input("> ").strip()
    
    if new_url:
        converted_url = convert_drive_url(new_url, 1000)
        if converted_url and converted_url != new_url:
            bg_vga(f"  converted to: {converted_url[:96]}...", 6)
        elif not converted_url:
            converted_url = new_url
            vga("  using original URL", 2)
        block['url'] = converted_url
        vga(f"URL updated to: {block['url']}", 2)
    else:
        vga("URL unchanged.", 2)

def edit_link_block(block):
    print("\n--- Editing Link Block ---")
    print(f"Current text: {block['text']}")
    print("Enter new link text (or Enter to keep current):")
    new_text = input("> ").strip()
    if new_text:
        block['text'] = new_text
        vga(f"Text updated to: {block['text']}", 2)
    else:
        vga("Text unchanged.", 2)
    
    print(f"\nCurrent URL: {block['href']}")
    print("Enter new URL (or Enter to keep current):")
    new_url = input("> ").strip()
    if new_url:
        block['href'] = new_url
        vga(f"URL updated to: {block['href']}", 2)
    else:
        vga("URL unchanged.", 2)

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
        os.system('cls')
        show_preview(date_str, time_str, post_name, content_blocks, filename)
        bg_vga("\nnext step:", 6)
        print("1 - add text")
        print("2 - add image")
        print("3 - add link")
        print("4 - edit content")
        print("5 - finish post")
        print("\naction: ", end="")
        choice = input().strip()
        
        if choice == '1':
            print("Text:")
            
            lines = []
            empty_line_count = 0
            line_num = 1
            
            print(f"{line_num:2d}: ", end='', flush=True)
            
            while True:
                line = input()
                
                if line == '':
                    empty_line_count += 1
                    if empty_line_count >= 1:
                        break
                    
                    lines.append('')
                    line_num += 1
                    print(f"{line_num:2d}: ", end='', flush=True)
                else:
                    empty_line_count = 0
                    lines.append(line)
                    line_num += 1
                    print(f"{line_num:2d}: ", end='', flush=True)
            
            if lines:
                while lines and lines[-1] == '':
                    lines.pop()
            
                text = '<br>'.join(lines)
                content_blocks.append({'type': 'text', 'content': text})
                vga(f"  Added text block ({len(lines)} lines, {sum(len(l) for l in lines)} chars)", 2)
                
                show_preview(date_str, time_str, post_name, content_blocks, filename)
        
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
                
                show_preview(date_str, time_str, post_name, content_blocks, filename)
        
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
                
                show_preview(date_str, time_str, post_name, content_blocks, filename)
        
        elif choice == '4':
            edit_content_block(content_blocks, date_str, time_str, post_name, filename)
        
        elif choice == '5':
            if not content_blocks:
                bg_vga("Error: no content", 1)
                continue
            
            show_preview(date_str, time_str, post_name, content_blocks, filename)
            
            confirm = input("\ncreate post? (y/n, default y): ").strip().lower()
            if confirm == 'n' or confirm == 'no':
                print("Cancelled")
                continue
            
            html_content = generate_html(date_str, time_str, post_name, content_blocks)
            os.makedirs("blog", exist_ok=True)
            with open(f"blog/{filename}", 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"\nPost created: {filename}")
            print(f"Saved to: {os.path.abspath(f'blog/{filename}')}")
            
            update_index_page(filename, date_str, time_str, post_name)
            break
        
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()