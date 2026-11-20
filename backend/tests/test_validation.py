from app import validate_blueprint
import pytest

def good():
    return {"version":1,"name":"test","size":{"x":2,"y":2,"z":2},"blocks":[{"x":0,"y":0,"z":0,"block":"minecraft:stone"}]}

def test_valid(): assert validate_blueprint(good())["name"] == "test"
def test_duplicate():
    b=good(); b["blocks"].append(b["blocks"][0]);
    with pytest.raises(ValueError): validate_blueprint(b)
def test_bounds():
    b=good(); b["blocks"][0]["x"]=2
    with pytest.raises(ValueError): validate_blueprint(b)
def test_unknown_block():
    b=good(); b["blocks"][0]["block"]="minecraft:tnt"
    with pytest.raises(ValueError): validate_blueprint(b)
