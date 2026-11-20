# Blueprint v1

- `version`: exactly 1
- `name`: display name
- `size`: x/y/z integer dimensions (1–64 each)
- `blocks`: list of records with integer local x/y/z and namespaced block ID
- Origin: bottom corner; coordinates are zero-based
- Maximum blocks: 2,000
- Duplicate coordinates prohibited
- Only IDs listed in backend validator and behavior-pack allow-list are accepted

Example:
```json
{"version":1,"name":"Tiny Tower","size":{"x":3,"y":4,"z":3},"blocks":[{"x":1,"y":0,"z":1,"block":"minecraft:stone"}]}
```
