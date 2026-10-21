# Accessibility Statement

[繁體中文](/.github/ACCESSIBILITY.md) | **English** | [日本語](/.github/ACCESSIBILITY.ja.md) | [ไทย](/.github/ACCESSIBILITY.th.md) | [Bahasa Indonesia](/.github/ACCESSIBILITY.id.md) | [한국어](/.github/ACCESSIBILITY.ko.md)

## Our commitment

We want developers who use screen readers, screen magnification, keyboard-only or voice input, as well as developers who work in different languages, to be able to install, read and use this skill, and to contribute to it.

## What the project consists of

This project has no web pages or graphical interface. It consists of:

- Markdown docs: the README in six languages, `SKILL.md`, `references/`
- Three command-line Python scripts
- Eval material used for development

You use it through your own AI tools and terminal, so how accessible those tools are also affects your experience.

## What we do now

- The scripts output plain text only and don't use color, cursor control or animation to convey information; everything can be done from the command line with just a keyboard.
- The scripts set standard output to UTF-8, which reduces garbled Chinese, Japanese, Thai and Korean text in the Windows console.
- The docs are divided into sections with Markdown headings, so you can jump to the part you need with a screen reader's heading navigation.
- The README is available in six languages: 繁體中文, English, 日本語, ไทย, Bahasa Indonesia, 한국어.
- When helping you build a LINE bot, the skill reminds you to write `altText` for Flex Messages and other messages: it appears in notifications, the chat list and quote previews.

## Known limitations

- The README's "Skill folders by tool" table has 5 columns and 12 rows, which is hard to read with a screen reader or on a narrow screen.
- The README's "Contents" section draws the directory tree with box-drawing characters (`├──`, `└──`), which a screen reader may read out one by one.
- `SKILL.md` and `references/` are in English only (they're mainly for the AI to read); the scripts' messages and `-h` help are in English only as well.
- The READMEs other than the Traditional Chinese one are translations and may be updated later; where they differ, the [Traditional Chinese version](/README.md) prevails.
- The install interfaces of Claude, ChatGPT, Codex and other tools are provided by their vendors, and their accessibility is outside this project's control.
- We haven't yet done systematic testing with any particular screen reader.

## Supported environments

- macOS, Linux, Windows (PowerShell, Windows Terminal), with Python 3.8 or later.
- Any terminal that can display UTF-8 text.
- The docs can be read on the GitHub website or in any Markdown viewer, or opened directly in a plain text editor.

## Reporting barriers

[Open an "Accessibility barrier" issue](https://github.com/Scorpio-meow/LINE-skill/issues/new?template=accessibility.yml) describing where you ran into it, the assistive technology and environment you use, and what difficulty you had. If you'd rather not post publicly, you can email yao921024@gmail.com. This is a personally maintained project with no fixed response time, but every report will be read carefully.

Suggestions are also welcome for other accessibility points the skill should remind you about when it helps you build a LINE bot.

Last updated: 2026-10-21
