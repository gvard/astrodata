"""Data generator from solarsystem/ page"""

import json
import textwrap
from collections import defaultdict
from decimal import Decimal
from urllib import request

from bs4 import BeautifulSoup


def clean_text(text: str) -> str:
    """Helper function to clear special characters."""
    if not text:
        return ""
    return (
        text.replace("\u0160", "S")
        .replace("\u2013", "-")
        .replace("á", "a")
        .replace("ʻ", "'")
        .replace("\xa0", "")
        .strip()
    )


class CompactJSONEncoder(json.JSONEncoder):
    """
    A JSON Encoder that puts small containers on single lines.

    Note:
        Original version taken from:
        https://gist.github.com/jannismain/e96666ca4f059c3e5bc28abb711b5c92
    """
    CONTAINER_TYPES = (list, tuple, dict)
    MAX_WIDTH = 490
    MAX_ITEMS = 20

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("indent", 0)
        super().__init__(*args, **kwargs)
        self.indentation_level = 0
        self.array_depth = 0

    def encode(self, o):
        """Encode JSON object *o* with respect to single line containers."""
        match o:
            case list() | tuple():
                return self._encode_list(o)
            case dict():
                return self._encode_object(o)
            case float():
                return format(Decimal(str(o)), "f")
            case _:
                return json.dumps(
                    o,
                    skipkeys=self.skipkeys,
                    ensure_ascii=self.ensure_ascii,
                    check_circular=self.check_circular,
                    allow_nan=self.allow_nan,
                    sort_keys=self.sort_keys,
                    indent=self.indent,
                    separators=(self.item_separator, self.key_separator),
                    default=getattr(self, "default", None),
                )

    def _encode_list(self, o):
        if self._put_on_single_line(o):
            return f"[{', '.join(self.encode(el) for el in o)}]"

        self.array_depth += 1
        self.indentation_level += 1

        if (
            self.array_depth == 1
            and len(o) > 1
            and isinstance(o[0], (list, tuple))
            and isinstance(o[-1], dict)
        ):
            line1 = f"{self.indent_str}{self.encode(o[0])}"
            line2 = f"{self.indent_str}{', '.join(self.encode(el) for el in o[1:-1])}"
            line3 = f"{self.indent_str}{self.encode(o[-1])}"
            closing_indent = (self.indentation_level - 1) * self.indent_str
            output = f"[\n{line1},\n{line2},\n{line3}\n{closing_indent}]"
        else:
            output_elements = [f"{self.indent_str}{self.encode(el)}" for el in o]
            closing_indent = (self.indentation_level - 1) * self.indent_str
            output = f"[\n{',\n'.join(output_elements)}\n{closing_indent}]"

        self.indentation_level -= 1
        self.array_depth -= 1
        return output

    def _encode_object(self, o):
        if not o:
            return "{}"

        if "desc" in o:
            other_parts = {k: v for k, v in o.items() if k != "desc"}
            first_line_content = ", ".join(
                f"{self.encode(k)}: {self.encode(el)}" for k, el in other_parts.items()
            )
            desc_content = f"{self.encode('desc')}: {self.encode(o['desc'])}"
            extra_indent = (
                " " * self.indent if isinstance(self.indent, int) else self.indent
            )
            return f"{{{first_line_content},\n{self.indent_str}{extra_indent}{desc_content}}}"

        if self._put_on_single_line(o):
            return f"{{{', '.join(f'{self.encode(k)}: {self.encode(el)}' for k, el in o.items())}}}"

        self.indentation_level += 1
        output = [
            f"{self.indent_str}{json.dumps(k)}: {self.encode(v)}" for k, v in o.items()
        ]
        self.indentation_level -= 1
        return "{\n" + ",\n".join(output) + "\n" + self.indent_str + "}"

    def iterencode(self, o, **kwargs):
        return self.encode(o)

    def _put_on_single_line(self, o):
        return (
            self._primitives_only(o)
            and len(o) <= self.MAX_ITEMS
            and len(str(o)) - 2 <= self.MAX_WIDTH
        )

    def _primitives_only(self, o):
        match o:
            case list() | tuple():
                return not any(isinstance(el, self.CONTAINER_TYPES) for el in o)
            case dict():
                return not any(
                    isinstance(el, self.CONTAINER_TYPES) for el in o.values()
                )
            case _:
                return True

    @property
    def indent_str(self) -> str:
        match self.indent:
            case int():
                return " " * (self.indentation_level * self.indent)
            case str():
                return self.indentation_level * self.indent
            case _:
                raise ValueError(
                    f"indent must either be of type int or str (is: {type(self.indent)})"
                )


def get_table(url: str, local: bool = False) -> list:
    """Read all rows from html table safely using context managers."""
    if local:
        with open(url, encoding="utf-8") as f:
            html = f.read()
    else:
        with request.urlopen(url) as response:
            html = response.read()

    soup = BeautifulSoup(html, "html.parser")
    table_div = soup.find("div", {"id": "tab"})
    return table_div.find_all("div", {"class": "obj"}) if table_div else []


GH_DIR = "../../../../"
HTML_TABLE_URL = f"{GH_DIR}gvard.github.io/solarsystem/index.html"
JSON_INFO_FILENAME = f"{GH_DIR}astrodata/data/solarsystem/resolved.json"

objs = get_table(HTML_TABLE_URL, local=True)

data = {}
unique_classes = set()
unique_types = set()
unique_types_dct = defaultdict(int)

for obj in objs:
    prms = {}
    all_data = []

    for typ in (obj.get("class") or []):
        unique_types.add(typ)
        unique_types_dct[typ] += 1

    for elm in obj.find_all(True):
        for cls in (elm.get("class") or []):
            unique_classes.add(cls)

    dimg = obj.find("div", {"class": "img"})
    img = dimg.find("img")
    a = obj.find("div", {"class": "name"}).find("a")

    num = obj.get("data-n")
    num = int(num) if num else None
    size = obj.find("div", {"class": "size"}).text.strip()

    mass_text = (
        mass.text.strip().replace("\xa0", "")
        if (mass := obj.find("div", {"class": "mass"}))
        else ""
    )
    date_text = (
        date.text.strip().replace("\xa0", "")
        if (date := obj.find("div", {"class": "date"}))
        else ""
    )
    rotd = obj.get("data-r")
    pre_text = (
        pre.text.strip().replace("\xa0", "")
        if (pre := obj.find("div", {"class": "pre"}))
        else ""
    )
    deltav = obj.find("div", {"class": "dv"}).text.strip()
    des = obj.find("div", {"class": "des"})
    imgdat = obj.find("div", {"class": "idat"})

    name = clean_text(img["alt"])
    all_data.append(obj.get("class", [])[1:])

    nmnam = img["alt"]
    if num:
        nmnam = f"{num} {nmnam}"
    if num and name == "Europa":
        name = f"{num} {name}"

    all_data.extend(
        [
            nmnam,
            a.text.strip(),
            img["src"].removeprefix("images/"),
            a["href"].removeprefix("https://en.wikipedia.org/wiki/"),
        ]
    )

    clean_nmnam = nmnam.replace("á", "a").replace("(", "").replace(")", "")
    parts = clean_nmnam.split(maxsplit=1)
    if len(parts) == 2 and parts[0].isdigit():
        first_match, second_match = parts
        if not (1940 < int(first_match) < 2023):
            prms["num"] = int(first_match)
        elif 1940 < int(first_match) < 2023:
            name = f"{first_match} {second_match}"
            prms["des"] = name

        if len(second_match) >= 4 and second_match[:4].isdigit() and (1940 < int(second_match[:4]) < 2023):
            prms["des"] = second_match

        if first_match != "52" and not (1940 < int(first_match) < 2023):
            name = clean_text(second_match)

    try:
        dsize = float(size)
    except ValueError:
        dsize = clean_text(size)
    all_data.append(dsize)
    all_data.append(date_text)

    try:
        all_data.append(float(deltav))
    except ValueError:
        all_data.append(deltav)

    if dlink := dimg.get("data-b"):
        prms["imurl"] = dlink
    if des:
        prms["des"] = des.text.strip()
    if mass_text:
        prms["mass"] = clean_text(mass_text)

    if rotd:
        try:
            prms["rot"] = int(rotd)
        except ValueError:
            prms["rot"] = float(rotd)

    if pre_text:
        prms["pre"] = pre_text
    if imgdat and imgdat.text:
        prms["idat"] = imgdat.text.strip()

    all_data.append(prms)
    data[name] = all_data

    if (dens := obj.find("div", {"class": "dens"})) and dens.text:
        try:
            prms["dens"] = float(dens.text.strip())
        except ValueError:
            prms["dens"] = clean_text(dens.text)

    if bib := obj.get("data-b"):
        prms["bib"] = bib

    if (desc := obj.find("div", {"class": "desc"})) and desc.text:
        prms["desc"] = desc.text.strip()

    if imgdist := obj.get("data-id"):
        prms["imdis"] = float(imgdist) if "." in imgdist else int(imgdist)

print("Number of objects:", len(data))

data = {
    "meta": ["tags", "nmnam", "runam", "imnam", "wurl", "size", "dat", "dv"],
    "data": data,
}

data_json = json.dumps(
    data, indent=0, cls=CompactJSONEncoder, ensure_ascii=False
).splitlines()

first_line = f"{data_json[0]}{data_json[1].strip()}"
last_line = f"{data_json[-2].strip()}{data_json[-1]}"
body_content = textwrap.dedent("\n".join(data_json[2:-2]))
data_json = f"{first_line}\n{body_content}\n{last_line}"

with open(JSON_INFO_FILENAME, "w", encoding="utf8", newline="") as json_file:
    json_file.write(data_json)

print("Unique classes:", unique_classes)
print()
print("Unique types sorted:", sorted(unique_types, key=len, reverse=True))
print()
print("Unique types dict sorted:",
    dict(sorted(unique_types_dct.items(), key=lambda item: item[1], reverse=True)),
)
