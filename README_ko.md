# LINE-skill

[繁體中文](README.md) | [English](README_en.md) | [日本語](README_ja.md) | [ไทย](README_th.md) | [Bahasa Indonesia](README_id.md) | **한국어**

AI 코딩 어시스턴트용 Agent Skill: **`line-dev`**. Claude, Codex, GitHub Copilot, Cursor, Gemini CLI 같은 도구가 LINE 플랫폼을 개발·디버깅·운영할 때 더 정확하게 동작하도록 돕습니다. Messaging API 웹훅, reply/push 메시지와 메시지 할당량, Flex Message, 리치 메뉴, 그룹 채팅 봇, LIFF, LINE Login을 다룹니다.

오픈 포맷인 [Agent Skills](https://agentskills.io) 형식(폴더 하나와 `SKILL.md`)을 따르므로, 이 형식을 지원하는 도구라면 어디서든 쓸 수 있습니다. 설치 방법은 [빠른 시작](#빠른-시작)을 참고하세요.

- **스펙은 항상 공식 문서에서 실시간으로 확인**: skill에는 문서 사본을 넣지 않고 "주제 → 공식 URL" 색인과 조회 스크립트만 포함합니다. 숫자·제한·요금이 필요할 때는 AI가 GitHub의 공식 원본 markdown(developers.line.biz가 동기화되는 원본)을 그 자리에서 확인하고 developers.line.biz 출처를 함께 제시합니다.
- **실전에서 겪은 함정 목록**: 서명 검증은 raw body로 해야 함, 웹훅은 약 2초 안에 응답해야 함, reply token은 한 번만 쓸 수 있고 금방 만료됨, 그룹에 push하면 인원수만큼 계산됨, 인증되지 않은 계정은 그룹 멤버 목록을 가져올 수 없음, textV2 멘션 작성법과 이스케이프, Flex 크기와 URI 제한, 리치 메뉴 이미지 제한과 우선순위, LIFF ID 토큰 만료와 백엔드 검증, provider가 다르면 userId가 달라지는 문제… 모두 "증상 → 원인 → 해결 → 공식 페이지" 형식으로 정리했습니다.
- **LINE API 직접 조작**: Python 표준 라이브러리만 쓰는 스크립트를 포함합니다. 쓰기 작업은 기본적으로 dry-run만 하고, 확인 후 `--yes`를 붙여야 실제로 실행됩니다. token/secret은 환경 변수나 `.env`에서만 읽으며 출력하지 않습니다.

> 이 프로젝트는 LY Corporation의 공식 프로젝트가 아닙니다. LINE은 LY Corporation의 상표입니다.

## 빠른 시작

[`skills`](https://github.com/vercel-labs/skills) 명령 한 줄로 설치할 수 있습니다. 컴퓨터에 있는 AI 도구를 감지해 각 도구에 맞는 폴더에 넣어 줍니다.

```bash
bunx skills add Scorpio-meow/LINE-skill --skill line-dev -g
```

- `-g`는 홈 디렉터리에 설치합니다(모든 프로젝트에서 사용 가능). `-g`를 빼면 현재 프로젝트에만 설치합니다.
- 특정 도구에만 설치하려면 `-a`를 추가합니다(예: `-a claude-code -a codex`). 도구별 값은 [다음 절의 표](#도구별-skill-폴더)를 참고하세요.
- [Bun](https://bun.sh)이 없다면 `bunx` 대신 `npx`를 써도 됩니다.

설치 후 LINE 개발에 관한 질문을 하면 자동으로 활성화됩니다. 예:

> LINE 봇의 reply token은 얼마 후에 만료되나요?

skill이 로드되어 있으면 답변이 먼저 공식 문서를 확인하고 developers.line.biz 링크를 함께 제시합니다. 스크립트를 처음 실행할 때 대부분의 도구는 명령 실행이나 네트워크 접속 허가를 먼저 요청합니다.

도구별 수동 설치와 그 밖의 설치 방법은 다음 절을 참고하세요.

## 설치

**Python 3.8 이상**이 필요합니다(스크립트가 표준 라이브러리만 쓰므로 패키지를 설치할 필요 없음). 공식 문서를 조회하려면 `raw.githubusercontent.com` 또는 `github.com`에, LINE API를 직접 조작하려면 `api.line.me`에 접속할 수 있어야 합니다.

### 도구별 skill 폴더

수동 설치는 `line-dev` 폴더를 도구가 읽는 skill 폴더에 복사해서 `SKILL.md`가 `<skill 폴더>/line-dev/SKILL.md`에 오도록 하는 것입니다. 개인 폴더는 이 컴퓨터의 모든 프로젝트에서 쓰이고, 프로젝트 폴더는 프로젝트 루트 아래에 두며 commit해서 팀과 공유할 수 있습니다.

| 도구 | `-a` 값 | 개인 폴더 | 프로젝트 폴더 | 수동 호출 |
|---|---|---|---|---|
| Claude Code | `claude-code` | `~/.claude/skills/` | `.claude/skills/` | `/line-dev` |
| OpenAI Codex(CLI, IDE 확장, ChatGPT 데스크톱 앱) | `codex` | `~/.agents/skills/` | `.agents/skills/` | `/skills` 또는 `$line-dev` |
| GitHub Copilot(VS Code, Copilot CLI, JetBrains) | `github-copilot` | `~/.copilot/skills/` | `.github/skills/` | `/line-dev` |
| Cursor | `cursor` | `~/.cursor/skills/` | `.cursor/skills/` | Agent 채팅에서 `/` 입력 후 선택 |
| Gemini CLI | `gemini-cli` | `~/.gemini/skills/` | `.gemini/skills/` | `/skills list`로 로드 여부 확인 |
| Google Antigravity | `antigravity` | `~/.gemini/config/skills/` | `.agents/skills/` | — |
| Devin Desktop(구 Windsurf) | `devin` | `~/.config/devin/skills/` | `.devin/skills/` | `@line-dev` |
| OpenCode | `opencode` | `~/.config/opencode/skills/` | `.opencode/skills/` | — |
| Cline | `cline` | `~/.cline/skills/` | `.cline/skills/` | `/line-dev` |
| Kiro | `kiro-cli` | `~/.kiro/skills/` | `.kiro/skills/` | `/` 입력 후 선택 |
| JetBrains Junie | `junie` | `~/.junie/skills/` | `.junie/skills/` | `/line-dev` 또는 `$line-dev` |
| Roo Code | `roo` | `~/.roo/skills/` | `.roo/skills/` | — |

Windows에서 `~`는 사용자 폴더(`%USERPROFILE%`)입니다. 모든 도구는 대화와 관련이 있으면 자동으로 skill을 사용하며, "수동 호출" 열은 명시적으로 지정하고 싶을 때의 방법일 뿐입니다.

- Codex, Copilot, Cursor, Gemini CLI, OpenCode, Devin Desktop, Junie, Roo Code는 `~/.agents/skills/`도 읽으므로, 여러 도구를 함께 쓴다면 여기에 하나만 두어도 모두 공유할 수 있습니다. Claude Code는 `~/.claude/skills/`만 읽습니다.
- `bunx skills`는 skill을 공용 `.agents/skills/`(`-g`를 붙이면 `~/.agents/skills/`)에 두고 다른 도구용 링크를 만듭니다. 설치 후 도구가 인식하지 못하면 아래의 수동 설치로 표에 있는 폴더에 넣으세요.
- 표에 없는 도구(Amp, Goose, Kilo Code, Trae, Qwen Code 등)도 `bunx skills`로 설치할 수 있습니다. `-a` 값은 [skills README](https://github.com/vercel-labs/skills)를 참고하세요.
- Devin Desktop은 Windsurf 시절의 `~/.codeium/windsurf/skills/`와 `.windsurf/skills/`도 계속 읽습니다.

아래는 `~/.agents/skills/`에 복사하는 예시입니다. 다른 도구라면 `TARGET`을 표의 경로로 바꾸세요.

macOS/Linux:

```bash
git clone --depth 1 https://github.com/Scorpio-meow/LINE-skill.git
TARGET=~/.agents/skills
mkdir -p "$TARGET"
cp -r LINE-skill/skills/line-dev "$TARGET/"
```

Windows PowerShell:

```powershell
git clone --depth 1 https://github.com/Scorpio-meow/LINE-skill.git
$TARGET = "$HOME\.agents\skills"
New-Item -ItemType Directory -Force $TARGET | Out-Null
Copy-Item -Recurse -Force LINE-skill\skills\line-dev "$TARGET\"
```

도구가 새 skill을 인식하지 못하면 한 번 다시 시작하세요.

### 기타 설치 방법

자체 설치 명령이 있는 도구도 있습니다.

- **GitHub CLI**(2.90 이상, `gh skill`은 현재 public preview): `--agent` 값은 표의 `-a`와 같습니다.

  ```bash
  gh skill install Scorpio-meow/LINE-skill line-dev --agent claude-code --scope user
  ```

- **OpenAI Codex**: Codex에서 다음을 입력합니다.

  ```text
  $skill-installer install https://github.com/Scorpio-meow/LINE-skill/tree/main/skills/line-dev
  ```

  Codex는 기본적으로 네트워크가 없는 샌드박스에서 명령을 실행하므로, 스크립트가 문서를 조회하거나 LINE API를 호출할 때 승인을 요청합니다. 항상 허용하려면 `~/.codex/config.toml`에 다음을 추가합니다.

  ```toml
  [sandbox_workspace_write]
  network_access = true
  ```

- **GitHub Copilot CLI**: clone한 뒤 `copilot skill add LINE-skill/skills/line-dev`를 실행합니다. 세션 도중에 추가했다면 `/skills reload`로 불러옵니다. 저장소의 `.github/skills/`에 두고 commit하면 클라우드에서 동작하는 Copilot cloud agent도 사용합니다.
- **Gemini CLI**: 기본적으로 사용자 범위에 설치됩니다. `--scope workspace`를 붙이면 현재 프로젝트에만 설치합니다.

  ```bash
  gemini skills install https://github.com/Scorpio-meow/LINE-skill.git --path skills/line-dev
  ```

- **Kiro**: Kiro 패널의 **Agent Steering & Skills** → **+** → **Import a skill** → **GitHub**를 선택합니다. URL은 skill이 있는 하위 폴더를 가리켜야 합니다: `https://github.com/Scorpio-meow/LINE-skill/tree/main/skills/line-dev`
- **Devin Desktop**: Cascade 패널 오른쪽 위의 **⋯** → **Skills**에서 skill을 관리할 수 있습니다.
- **Cline**: 새 skill은 기본으로 활성화되며, Cline 패널 아래쪽의 **Skills** 탭에서 켜고 끌 수 있습니다.

### Claude 앱(웹/데스크톱)

1. 코드 실행을 켭니다. Pro, Max 플랜은 **Settings > Capabilities**에서 "Code execution and file creation"을 켭니다. Team, Enterprise 플랜은 조직 소유자가 조직 설정에서 "Code execution and file creation"과 "Skills"를 켭니다.
2. `line-dev.zip`을 직접 만듭니다. ZIP의 최상위는 `line-dev/` 폴더여야 합니다. GitHub의 "Download ZIP"은 저장소 전체(최상위가 `LINE-skill-main/`)라서 그대로는 업로드할 수 없으니, 압축을 풀거나 저장소를 clone한 뒤 `line-dev` 폴더만 압축하세요.
   - macOS/Linux: `LINE-skill/skills` 폴더에서 `zip -r ../../line-dev.zip line-dev -x '*.DS_Store'`를 실행합니다.
   - Windows: 파일 탐색기에서 `skills\line-dev` 폴더를 마우스 오른쪽 버튼으로 클릭 → "ZIP 파일로 압축"(Windows 10은 "보내기 → 압축(ZIP) 폴더").
3. **Customize > Skills**에서 **+** → **Create skill** → **Upload a skill**을 눌러 ZIP을 업로드합니다. 화면이 **Settings > Capabilities**라면 Skills 섹션에서 **Upload skill**을 누릅니다.

업로드한 skill은 내 계정에서만 쓸 수 있으며, 조직 전체에서 쓰려면 조직 소유자가 배포(provisioning)해야 합니다. 앱의 코드 실행 환경은 보통 패키지 관리자, `github.com` 등 일부 도메인에만 접속할 수 있습니다. `line_docs.py`는 `raw.githubusercontent.com`에 접속할 수 없으면 자동으로 `github.com`에서 같은 문서를 가져오지만, `line_api.py`에 필요한 `api.line.me`는 기본적으로 접속할 수 없습니다. Team, Enterprise 플랜에서는 조직 소유자가 조직 설정의 Capabilities에서 허용 도메인을 추가할 수 있습니다. LINE API를 직접 조작하려면 내 컴퓨터에서 Claude Code 같은 도구를 쓰는 것을 권장합니다. 화면이 바뀌었다면 [공식 안내](https://support.claude.com/en/articles/12512180-using-skills-in-claude)를 따르세요.

### ChatGPT

[공식 도움말](https://help.openai.com/en/articles/20001066-skills-in-chatgpt)에 따르면 ChatGPT의 skill은 현재 Business, Enterprise, Healthcare, Edu 플랜의 자격을 갖춘 사용자에게 제공되며, 업로드 가능 여부는 워크스페이스 설정에 따라 정해집니다.

1. 앞 절의 방법으로 `line-dev.zip`을 준비합니다.
2. 사이드바의 **Plugins** → **Skills** 탭에서 **Create** → **Upload from your computer**를 눌러 ZIP을 업로드합니다.
3. 대화에서 `@`를 입력해 `line-dev`를 선택하거나, ChatGPT가 알아서 판단하게 둡니다.

ChatGPT와 Codex의 skill은 현재 동기화되지 않으므로, Codex를 쓴다면 따로 설치해야 합니다. LINE API를 직접 조작하려면 내 컴퓨터에서 Codex 같은 도구를 쓰는 것을 권장합니다.

### 업데이트와 제거

| 설치 방법 | 업데이트 | 제거 |
|---|---|---|
| `bunx skills` | `bunx skills update line-dev` | `bunx skills remove line-dev` |
| `gh skill` | `gh skill update` | `line-dev` 폴더 삭제 |
| Gemini CLI | 제거 후 다시 설치 | `gemini skills uninstall line-dev` |
| 수동 복사 | `LINE-skill` 폴더에서 `git pull`을 실행한 뒤 다시 복사 | `line-dev` 폴더 삭제 |
| Claude 앱, ChatGPT | 이전 것을 삭제하고 새 ZIP 업로드 | Skills 페이지에서 삭제 |

### 도구별 공식 문서

경로나 화면이 바뀌었다면 공식 문서를 따르세요: [Claude Code](https://code.claude.com/docs/en/skills) · [Claude 앱](https://support.claude.com/en/articles/12512180-using-skills-in-claude) · [ChatGPT](https://help.openai.com/en/articles/20001066-skills-in-chatgpt) · [OpenAI Codex](https://learn.chatgpt.com/docs/build-skills) · [GitHub Copilot](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-skills) · [VS Code](https://code.visualstudio.com/docs/agent-customization/agent-skills) · [Cursor](https://cursor.com/docs/skills) · [Gemini CLI](https://geminicli.com/docs/cli/skills/) · [Google Antigravity](https://antigravity.google/docs/skills) · [Devin Desktop](https://docs.devin.ai/desktop/cascade/skills) · [OpenCode](https://opencode.ai/docs/skills) · [Cline](https://docs.cline.bot/customization/skills) · [Kiro](https://kiro.dev/docs/skills/) · [JetBrains Junie](https://junie.jetbrains.com/docs/agent-skills.html) · [Roo Code](https://roocodeinc.github.io/Roo-Code/features/skills/) · [skills](https://github.com/vercel-labs/skills) · [gh skill](https://cli.github.com/manual/gh_skill_install)

## 스크립트 사용법

skill이 이 스크립트들을 알아서 호출하지만, 직접 실행할 수도 있습니다. Python 3.8 이상이 필요하며 패키지를 설치할 필요는 없습니다(Windows에서는 `python` 또는 `py -3`).

```bash
# 공식 문서 조회(실시간으로 가져와 하루 동안 캐시, git이 있으면 전문 검색 지원)
python3 skills/line-dev/scripts/line_docs.py search "loading animation"
python3 skills/line-dev/scripts/line_docs.py section "Send push message"
python3 skills/line-dev/scripts/line_docs.py page messaging-api/pricing --grep count

# Messaging API: token은 환경 변수에 넣거나 --env-file로 프로젝트의 .env를 지정
export LINE_CHANNEL_ACCESS_TOKEN=...
python3 skills/line-dev/scripts/line_api.py info                     # 봇 정보
python3 skills/line-dev/scripts/line_api.py quota                    # 이번 달 할당량과 사용량
python3 skills/line-dev/scripts/line_api.py validate push card.json  # 메시지 형식 검증(전송하지 않음)
python3 skills/line-dev/scripts/line_api.py push --to Uxxxx --text "테스트"        # dry-run: 보낼 내용만 표시
python3 skills/line-dev/scripts/line_api.py push --to Uxxxx --text "테스트" --yes  # 실제로 전송
python3 skills/line-dev/scripts/line_api.py richmenu-validate menu.json --image menu.png
python3 skills/line-dev/scripts/line_api.py richmenu-deploy menu.json menu.png --default        # dry-run
python3 skills/line-dev/scripts/line_api.py webhook-test

# 웹훅 디버깅: secret은 환경 변수에 넣기
export LINE_CHANNEL_SECRET=...
python3 skills/line-dev/scripts/webhook_tools.py selftest http://localhost:3000/webhook
python3 skills/line-dev/scripts/webhook_tools.py simulate http://localhost:3000/webhook postback --source group
python3 skills/line-dev/scripts/webhook_tools.py sample memberJoined
```

`selftest`는 요청 네 개를 차례로 보냅니다. Console의 Verify(빈 `events`), 올바른 서명의 이벤트, 잘못된 서명, 서명 없음 순이며, 응답이 LINE의 2초 타임아웃을 넘지 않는지도 확인합니다.

## 구성

```
skills/line-dev/
├── SKILL.md                      # 메인 설명(AI용, 영어)
├── references/
│   ├── doc-map.md                # 공식 문서 색인: URL 규칙, 페이지 목록, API reference 앵커, OpenAPI, 상태 페이지, 지원 종료 공지
│   └── gotchas/                  # 실전 함정과 설계 패턴. 주제별 파일로 나뉘며 AI는 필요한 것만 읽음
│       ├── webhooks-and-hosting.md
│       ├── messaging.md
│       ├── groups-and-mentions.md
│       ├── rich-menus.md
│       ├── liff-and-login.md
│       └── security-and-architecture.md
└── scripts/
    ├── line_docs.py              # 공식 문서 실시간 조회: 전문 검색, API reference 섹션, 가이드 페이지(인용 가능한 URL 포함)
    ├── line_api.py               # Messaging API 조작 CLI(dry-run 우선)
    └── webhook_tools.py          # 서명 계산/검증, LINE의 웹훅 호출 시뮬레이션, 명령 하나로 끝나는 selftest
evals/                            # 이 skill 개발에 쓴 테스트 시나리오
.github/                          # 커뮤니티 문서(기여 가이드, 행동 강령, 보안 정책, 접근성 선언)와 issue/PR 템플릿
```

## 안전 설계

- push/multicast/broadcast, 웹훅 설정, 리치 메뉴 게시·기본 설정·삭제, 봇의 그룹 나가기 같은 쓰기 작업은 `--yes`가 없으면 dry-run만 합니다. 먼저 검증한 뒤 전체 요청과 함께 수신 대상 유형, 그룹 인원수(그룹 push는 인원수만큼 계산), 이번 달 남은 할당량을 출력합니다.
- 메시지를 보낼 때 `X-Line-Retry-Key`를 자동으로 붙이므로, 타임아웃 후 재시도해도 중복 전송되지 않습니다.
- `line_api.py`는 `api.line.me`, `api-data.line.me`에만, `line_docs.py`는 문서를 가져오기 위해 GitHub에만 접속하고, `webhook_tools.py`는 지정한 URL로만 요청을 보냅니다(서명을 보내며 secret은 보내지 않음). token/secret은 출력에 나타나지 않습니다.
- skill은 내 컴퓨터(또는 AI 도구의 실행 환경)에서 스크립트를 실행합니다. 설치 전에 `SKILL.md`와 `scripts/`를 먼저 살펴볼 수 있습니다.

## 공식 문서

이 skill이 참조하는 공식 문서는 [LINE Developers](https://developers.line.biz/)와 그 markdown 원본인 [line/line-developers-docs-source](https://github.com/line/line-developers-docs-source)입니다(이 저장소의 README가 AI 도구의 사용을 명시적으로 허용함). 공식 문서는 계속 업데이트되므로 skill에는 색인만 두고 사본은 포함하지 않습니다.

## 테스트

`evals/evals.json`은 이 skill을 개발하며 사용한 5가지 테스트 시나리오입니다. 웹훅 401 디버깅, 그룹 봇 스펙 조회, 리치 메뉴 게시, LIFF 사용자 인증, 그룹 봇 코드 리뷰로 구성되며 평가 기준은 총 49개입니다. `evals/files/richmenu/`는 일부러 오류를 넣어 둔 리치 메뉴 소재입니다. `fake-env.txt`는 무작위로 생성한 가짜 token으로, 시나리오 3을 실행할 때 작업 폴더에 복사하고 이름을 `.env`로 바꾸세요(문제에서 token이 `.env`에 있다고 설명함).

최근 비교(Claude Opus 5.5, 시나리오마다 skill 있음/없음으로 한 번씩 실행, 블라인드 채점): skill 있음 47/49, skill 없음 44/49였고, skill이 있을 때 평균 16% 더 빨랐습니다. 차이가 가장 컸던 것은 LIFF(지원 중단된 LIFF SDK 버전에 대한 보안 경고, token이 만료됐을 때만 다시 로그인)와 리치 메뉴 게시(token을 명령줄에 올리지 않기, 게시 전에 확인)였습니다. 이후 통과하지 못한 2개 기준에 맞춰 skill을 수정하고 시나리오 1과 5를 다시 실행하자 모두 통과해, 다섯 시나리오 합계 skill 있음 49/49가 되었습니다. 트리거 테스트(사용해야 하는 문장 10개와 비슷하지만 사용하면 안 되는 문장 10개, 각 3회)는 모두 올바르게 판정되었습니다.

## 기여하기

오래된 LINE 사양 제보, 새로운 함정 추가, 스크립트와 문서 개선을 환영합니다.

- 진행 방식, skill의 원칙, 변경 사항 확인 방법: [기여 가이드](.github/CONTRIBUTING_ko.md)
- [행동 강령](.github/i18n/CODE_OF_CONDUCT_ko.md)
- 보안 취약점은 공개 issue로 올리지 말고 [보안 정책](.github/SECURITY_ko.md)에 따라 비공개로 신고해 주세요.
- 접근성 현황과 알려진 제한 사항: [접근성 선언](.github/ACCESSIBILITY_ko.md)

## 라이선스

[MIT](LICENSE)
