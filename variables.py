allitemstem = """
<form id="id{}" class="itemform tr">
        <div class="td"><input size="3" type="text" name="id" value="{}" disabled="true"></div>
        <div class="td"><input type="text" name="brand" size="10" value="{}"></div>
        <div class="td"><input type="text" name="model" size="10" value="{}"></div>
        <div class="td"><input type="text" name="type" size="10" value="{}"></div>
        <div class="td"><input type="number" class="price" step="10" name="price" value="{}"></div>
        <div class="td"><input type="number" class="count" name="count" value="{}"></div>
        <div class="td"><button type="button" class="delete">Delete</button></div>
        <div class="td"><input type="submit" name="submit" value="Save"></div>
</form>"""

dueformtem = """
<form id="id{}" class="dueform tr">
        <div class="td" nowrap>{}</div>
        <div class="td">{}</div>
        <div class="td"><input type="number" name="amount" class="rm-due-amount" size="10" value="{}"></div>
        <div class="td"><button type="button" class="delete">Remove</button></div>
        <div class="td"><input type="submit" name="submit" value="Save"></div>
</form>"""

duestem = """
<div class="htr">
    <div class="htd4">{}</div>
    <div class="htd2">{}</div>
    <div class="htd4">{}</div>
</div>
"""

cashtem = """
<div class="htr">
<div class="htd2">Start</div>
    <div class="htd2"><span id="start">{}</span></div>
</div>
<div class="htr">
    <div class="htd2">In</div>
    <div class="htd2"><span id="in">{}</span></div>
</div>
<div class="htr">
    <div class="htd2">Out</div>
       <div class="htd2"><span id="out">{}</span></div>
</div>
<div class="htr">
    <div class="htd2">Last</div>
    <div class="htd2"><span id="current">{}</span></div>
</div>"""

salestem = """
<div class="htr">
    <div class="htd4">{}</div>
    <div class="htd4">{}</div>
    <div class="htd4">{}</div>
    <div class="htd4">{}</div>
</div>"""
salestotaltem = """
<div class="htr">
    <div class="htd4"></div>
    <div class="htd4"></div>
    <div class="htd4">Total</div>
    <div class="htd4">{}</div>
</div>"""

exptem = """
<div class="htr">
    <div class="htd2">{}</div>
    <div class="htd2">{}</span></div>
</div>"""


exptotaltem = """
<div class="htr">
    <div class="htd2">Total</div>
    <div class="htd2">{}</span></div>
</div>"""
