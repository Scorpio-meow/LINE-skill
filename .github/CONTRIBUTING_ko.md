# 기여 가이드

[繁體中文](/.github/CONTRIBUTING.md) | [English](/.github/CONTRIBUTING_en.md) | [日本語](/.github/CONTRIBUTING_ja.md) | [ไทย](/.github/CONTRIBUTING_th.md) | [Bahasa Indonesia](/.github/CONTRIBUTING_id.md) | **한국어**

도와주셔서 감사합니다! 이 프로젝트에 참여할 때는 [행동 강령](/.github/i18n/CODE_OF_CONDUCT_ko.md)을 지켜 주세요.

README가 제공되는 언어(繁體中文, English, 日本語, ไทย, Bahasa Indonesia, 한국어) 중 어느 것으로든 issue나 PR을 열어도 됩니다. 답변은 번체 중국어나 영어로 드릴 수 있습니다.

> 이 프로젝트는 LY Corporation의 공식 프로젝트가 아닙니다. LINE 플랫폼 자체(LINE 앱, Messaging API, LIFF, LINE Login)의 문제는 LINE 공식 창구에 신고하세요.

## 도울 수 있는 일

| 하고 싶은 일 | 방법 |
|---|---|
| 설치나 사용에 관한 질문, 논의하고 싶은 아이디어 | [Discussions](https://github.com/Scorpio-meow/LINE-skill/discussions)에 질문 |
| LINE 스펙이 바뀜, 문서 링크가 깨짐, skill에 적힌 숫자가 오래됨 | "Outdated LINE info or broken link"(LINE 정보가 오래됨 또는 링크 깨짐) issue를 열고 공식 출처 첨부 |
| skill에 없는 함정을 겪음 | "Feature request or new gotcha"(새 기능 또는 새 함정) issue를 열거나, 바로 PR을 보내 `references/gotchas/`에 추가 |
| 스크립트 오류, AI가 skill대로 했는데 잘못됨 | "Bug report"(버그 신고) issue 열기 |
| 문서가 이해하기 어려움, 번역 오류, 접근성 문제 | 해당하는 issue를 열거나 바로 PR 보내기 |
| 보안 취약점 | **issue를 열지 마세요**. [SECURITY.md](/.github/SECURITY_ko.md)에 따라 비공개로 신고 |

큰 변경(새 스크립트 명령, `SKILL.md`의 흐름 조정, 새 함정 파일 추가)은 헛수고가 되지 않도록 먼저 issue를 열어 논의해 주세요.

## 이 skill의 원칙

변경하기 전에 [`skills/line-dev/SKILL.md`](/skills/line-dev/SKILL.md)를 먼저 읽어 주세요. PR은 다음 기준으로 리뷰합니다.

1. **공식 문서 사본을 넣지 않습니다.** skill에는 "주제 → 공식 URL" 색인과 조회 스크립트만 두고, 스펙은 항상 [LINE Developers](https://developers.line.biz/)에서 실시간으로 확인합니다. 공식 문서를 저장소에 길게 붙여 넣지 마세요. 인용하려면 URL을 적거나, `line_docs.py`로 찾을 수 있는 섹션 이름을 적으세요.
2. **함정 항목의 형식은 정해져 있습니다**: **증상 또는 규칙 → 원인 → 해결** 순서로 쓰고, `Re-check:`로 다시 확인할 공식 페이지를 붙입니다(경로는 `https://developers.line.biz/en/` 기준 상대 경로). 바뀔 수 있는 숫자에는 "(at the time of writing)"을 붙이고, 파일 맨 앞의 확인 연월을 갱신하세요.
3. **`SKILL.md`는 AI가 읽는 문서입니다**: 영어로 짧고 정확하게 쓰고, 세부 내용은 `references/`에 둡니다. 주제 하나에 파일 하나로 나눠 AI가 필요한 것만 읽게 합니다.
4. **스크립트는 Python 3.8 이상의 표준 라이브러리만 사용합니다.** 서드파티 패키지는 추가하지 않습니다.
5. **token과 secret 처리 규칙은 완화할 수 없습니다**: 환경 변수나 `--env-file`에서만 읽고, 출력하거나 파일에 쓰지 않습니다. `line_api.py`는 `api.line.me`, `api-data.line.me`에만, `line_docs.py`는 GitHub에만 접속하고, `webhook_tools.py`는 사용자가 지정한 URL로만 요청을 보내며 서명만 보냅니다.
6. **쓰기 작업은 기본적으로 dry-run입니다**: `--yes`가 없으면 실제로 전송하거나 설정을 바꿀 수 없습니다. 쓰기 명령을 새로 추가할 때도 이를 지켜야 하며, `SKILL.md`의 Safety tiers에도 추가해야 합니다.

## 개발 환경

```bash
git clone https://github.com/Scorpio-meow/LINE-skill.git
cd LINE-skill
```

수정 중인 버전을 AI 도구가 바로 읽게 하려면 skill 폴더를 도구의 skill 폴더에 링크하세요(이미 설치된 `line-dev`는 먼저 제거). 아래는 Claude Code 예시이며, 다른 도구의 폴더는 [README](/README_ko.md#도구별-skill-폴더)를 참고하세요.

macOS/Linux:

```bash
ln -s "$PWD/skills/line-dev" ~/.claude/skills/line-dev
```

Windows PowerShell(junction은 관리자 권한이 필요 없음):

```powershell
New-Item -ItemType Junction -Path "$HOME\.claude\skills\line-dev" -Target "$PWD\skills\line-dev"
```

## 변경 사항 확인

아직 자동화된 테스트가 없으므로 최소한 다음 명령은 실행해 주세요(Windows에서는 `python` 또는 `py -3`).

```bash
# 세 스크립트가 모두 실행되는지 확인(문법 오류가 있으면 여기서 드러남)
python3 skills/line-dev/scripts/line_api.py -h
python3 skills/line-dev/scripts/line_docs.py -h
python3 skills/line-dev/scripts/webhook_tools.py -h

# token 없이 할 수 있는 실제 동작
python3 skills/line-dev/scripts/webhook_tools.py sample text
python3 skills/line-dev/scripts/line_docs.py section "Send push message"
```

- **Python 3.8 호환**: 3.9 이후에 추가된 문법이나 함수(예: `list[str]` 타입 힌트, `str.removeprefix`, `match`)는 쓰지 마세요. [uv](https://docs.astral.sh/uv/)가 있다면 다음처럼 3.8로 실행할 수 있습니다: `uv run --no-project --python 3.8 python skills/line-dev/scripts/line_api.py -h`.
- **웹훅 관련 기능을 바꿨다면**: 로컬 웹훅에 대해 `webhook_tools.py selftest <url>`을 실행하세요.
- **`line_api.py`의 쓰기 명령을 바꿨다면**: `--yes` 없이는 요청만 출력하고 실제로 보내지 않는지 확인하세요. 실제 채널로 테스트할 때는 본인의 테스트 계정을 쓰세요.
- **`SKILL.md`나 함정 문서를 바꿔 AI의 동작이 달라질 수 있다면**: [`evals/evals.json`](/evals/evals.json)에서 관련 시나리오를 골라 변경 전후로 한 번씩 실행하고, 각 시나리오의 `expectations`에 따라 채점해 통과 수를 PR에 적어 주세요. 방법은 자유이며, AI 도구에 시나리오를 붙여 넣고 사람이 직접 대조해 채점해도 됩니다. 큰 주제를 새로 추가할 때는 테스트 시나리오도 함께 추가해 주시면 좋습니다.

## 문서

- [`README.md`](/README.md)(번체 중국어)가 기준 버전입니다. 그 내용을 바꿨다면 다른 언어 버전도 함께 업데이트해 주세요. 모르는 언어는 PR에 적어 두면 메인테이너가 채워 넣습니다.
- 주목할 만한 변경은 [`CHANGELOG.md`](/CHANGELOG.md)의 `[Unreleased]`에 기록해 주세요. 형식은 [Keep a Changelog](https://keepachangelog.com/ko/1.1.0/)를 따릅니다.

## Pull Request 보내기

- PR 하나에는 한 가지 일만 담아 주세요. 변경이 작을수록 리뷰하기 쉽습니다.
- commit 메시지는 [Conventional Commits](https://www.conventionalcommits.org/ko/v1.0.0/) 형식을 따르고, skill 자체를 고칠 때는 `line-dev` 범위(scope)를 붙입니다. 예: `fix(line-dev): 擋下 line_docs.py 的路徑穿越`, `docs: 更新評測結果`. 설명은 어떤 언어로 써도 됩니다.
- **실제 token, secret, userId, groupId는 절대 commit하지 마세요.** 예제와 테스트 소재에는 항상 가짜 값을 쓰세요(`evals/files/richmenu/fake-env.txt`처럼 무작위로 생성).
- PR 템플릿에 따라 무엇을 했고 어떻게 테스트했는지 적어 주세요.

## 라이선스

기여하신 내용은 이 프로젝트의 [MIT 라이선스](/LICENSE)로 배포됩니다.
