# Custom-skills-agy

My `max` skills packaged as an Antigravity plugin. Apart from this README and `.github/`, nothing here is written by hand. Each Release in [Custom-skills](https://github.com/Maxastrand04/Custom-skills) builds the plugin there and pushes it here with a matching `vX.Y.Z` tag.

## Install

Install with the Antigravity CLI, `agy`, since the App can't install from a GitHub link.

```bash
agy plugin install https://github.com/Maxastrand04/Custom-skills-agy
```

The plugin lands in `~/.gemini/config/plugins/max/`, where both the CLI and the App find it.

### Pick a version

To stay on one version, pick a tag from the [tags page](https://github.com/Maxastrand04/Custom-skills-agy/tags) and put it in place of `vX.Y.Z`:

```bash
agy plugin install https://github.com/Maxastrand04/Custom-skills-agy/tree/vX.Y.Z
```

## Update

```bash
agy plugin install https://github.com/Maxastrand04/Custom-skills-agy
```

## Add AGENTS.md

The plugin ships an `AGENTS.md` with the rules the skills expect, but Antigravity doesn't load an `AGENTS.md` from a plugin. Add it to your global rules in one of two ways.

### Override your global AGENTS.md

> [!WARNING]
> Overriding removes every instruction currently in `~/.gemini/config/AGENTS.md`.

```bash
cp ~/.gemini/config/plugins/max/AGENTS.md ~/.gemini/config/AGENTS.md
```

### Copy the contents into your global AGENTS.md

This keeps your current instructions and adds the plugin's rules at the end.

```bash
cat ~/.gemini/config/plugins/max/AGENTS.md >> ~/.gemini/config/AGENTS.md
```

## Coming from `./install.sh --agy`

If you set up skills with `./install.sh --agy` from Custom-skills, delete the links it made in `~/.gemini/config/skills/`, because a skill there beats a plugin skill with the same name.

## Issues and changes

The source lives in [Custom-skills](https://github.com/Maxastrand04/Custom-skills). Open issues and pull requests there, not here. A change to the skills made here gets overwritten by the next Release.
