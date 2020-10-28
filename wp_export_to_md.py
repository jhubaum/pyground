import xml.etree.ElementTree as xml
import sys
import os

def post_to_file(post):
    filename = post.find("link").text.split("/")
    filename = filename[-2] if len(filename[-1]) == 0 else filename[-1]

    with open(os.path.join("output", filename + ".md"), "w+") as f:
        def write_header_element(name, title=None):
            if title is None:
                title = name
            f.write(f"{title}: \"{post.find(name).text}\"\n")
        f.write("---\n")
        write_header_element("title")
        write_header_element("pubDate", "date")
        f.write("---\n\n")

        content = post.find("{http://purl.org/rss/1.0/modules/content/}encoded").text

        content = content.replace("<!-- wp:paragraph -->\n", "")\
                         .replace("<!-- /wp:paragraph -->\n", "")\
                         .replace("<!-- /wp:paragraph -->", "")\
                         .replace("<p>", "")\
                         .replace("</p>", "")\
                         .replace("<br>", "\n")

        f.write(content)

        f.write("\n")

def inspect(post):
    print([i.tag for i in post])
    print(post.find("{http://purl.org/rss/1.0/modules/content/}encoded").text)

if len(sys.argv) == 1:
    print(f"usage: {sys.argv[0]} <wp_xml_export_file>")
else:
    tree = xml.ElementTree(file=sys.argv[1])
    os.mkdir('output')
    for it in tree.find("channel"):
        if (it.tag == "item"):
            post_to_file(it)
