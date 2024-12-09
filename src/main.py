from export import *
from markdown_helper_functions import *

content_path = "src/content"
public_path = "./public"
static_path = "./static"


copy_static_to_public()
generate_pages_recursive(content_path, "src/template.html", public_path)

