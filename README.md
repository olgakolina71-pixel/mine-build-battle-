# Mine Build Battle

Minecraft Bedrock AI build-battle project. The goal is an AI architect that creates detailed voxel designs, a validator, and a builder that places them in a separate plot. The YouTube audience judges the final reveal.

## Repository status

### Implemented
- [x] Blueprint v1 JSON format
- [x] Bedrock behavior-pack prototype with batched placement
- [x] In-game `!build` trigger for starter house
- [x] Python FastAPI architect/validation service
- [x] OpenAI-compatible model endpoint support (provider-agnostic)
- [x] Server-side validation and limits
- [x] Unit tests + GitHub Actions test workflow
- [x] Dockerfile for backend
- [x] Blueprint-to-`.mcfunction` export endpoint
- [x] Exporter unit tests
- [x] Mobile-friendly standalone web UI (`frontend/index.html`)
- [x] Architecture and schema documentation

### Not yet integrated
- [x] Export blueprint into relative Bedrock `setblock` function (manual import step remains)
- [ ] Send generated blueprint from backend to Minecraft executor
- [ ] Automated build-command / transfer bridge
- [ ] Visual screenshot QA and iterative repair
- [ ] AI build battle timer and plot isolation
- [ ] Minecraft pack packaging/download release

## Bedrock prototype
Copy `bedrock-pack` into your development behavior packs folder, activate it in a test world, and type `!build`. The current game script places its embedded sample blueprint; generated blueprints are not yet connected to the in-game script. Use a backup world.

## Mobile UI

The repository includes a GitHub Pages deployment workflow (`.github/workflows/deploy-frontend.yml`). After enabling Pages in repository Settings → Pages → Build and deployment → GitHub Actions, the site should publish at `https://olgakolina71-pixel.github.io/mine-build-battle-/`. You can also open `frontend/index.html` locally. Enter the backend API URL, theme and limits, then generate. The page displays the validated JSON and can export a `.mcfunction` file. Browser-to-backend requests require CORS to be configured on the server if the UI is hosted on a different origin. The UI is not a direct Minecraft connection yet.

## Architect API
See [backend/README.md](backend/README.md). API:
- `GET /health`
- `POST /validate`
- `POST /generate`

It can use a compatible chat-completions endpoint configured with environment variables. **Never commit API keys.** Do not put provider credentials in the behavior pack or share them with other players.

## Test
```bash
cd backend
pip install -r requirements.txt pytest
pytest
```

## Docs
- [Architecture](docs/architecture.md)
- [Blueprint schema](docs/blueprint-schema.md)
- [Backend setup](backend/README.md)

## Next milestones
1. Add blueprint transport/import into Bedrock (safe and local-first).
2. Create larger themed sample blueprints and improve architecture prompt.
3. Add screenshot-based review with explicit user approval before repair.
4. Build the fair competition mode: equal plots, timer, same constraints, simultaneous reveal.
