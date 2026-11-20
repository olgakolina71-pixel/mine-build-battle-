from exporter import to_mcfunction
from app import validate_blueprint


def blueprint():
    return {"version":1,"name":"Demo","size":{"x":2,"y":2,"z":2},"blocks":[
        {"x":0,"y":0,"z":0,"block":"minecraft:stone"},
        {"x":1,"y":1,"z":1,"block":"minecraft:glass"}]}


def test_export_relative_commands():
    out=to_mcfunction(blueprint())
    assert "setblock ~0 ~0 ~0 minecraft:stone replace" in out
    assert "setblock ~1 ~1 ~1 minecraft:glass replace" in out

def test_export_validates_before_export():
    b=blueprint(); b["blocks"][0]["block"]="minecraft:tnt"
    try: to_mcfunction(b)
    except ValueError: return
    assert False, "Expected validation to reject TNT"
