"""Convert validated blueprint JSON into a Bedrock .mcfunction export."""


def to_mcfunction(bp: dict, *, prefix: str = "~") -> str:
    """Generate relative setblock commands; coordinates are relative to function execution."""
    from app import validate_blueprint
    validate_blueprint(bp)
    lines = [f"# Mine Build Battle: {bp.get('name', 'Blueprint')}", "# Execute at the desired build origin."]
    for b in bp["blocks"]:
        lines.append(f"setblock {prefix}{b['x']} {prefix}{b['y']} {prefix}{b['z']} {b['block']} replace")
    return "\n".join(lines) + "\n"
