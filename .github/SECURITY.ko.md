# 보안 정책

[繁體中文](/.github/SECURITY.md) | [English](/.github/SECURITY.en.md) | [日本語](/.github/SECURITY.ja.md) | [ไทย](/.github/SECURITY.th.md) | [Bahasa Indonesia](/.github/SECURITY.id.md) | **한국어**

## 지원 버전

최신 버전, 즉 `main` 브랜치만 수정합니다. 이전 버전을 쓰고 있다면 먼저 업데이트하세요(업데이트 방법은 [README](/README.ko.md#업데이트와-제거) 참고).

## 취약점 신고

**공개 issue를 열지 마세요.** GitHub의 비공개 신고 기능을 이용해 주세요. 저장소의 **Security** 탭에서 **Report a vulnerability**를 누르거나, [이 링크](https://github.com/Scorpio-meow/LINE-skill/security/advisories/new)를 바로 여세요. 이 방법을 쓸 수 없다면 yao921024@gmail.com으로 이메일을 보내고 제목에 `[LINE-skill security]`를 붙여 주세요.

다음 내용을 포함해 주세요.

- 영향을 받는 파일과 버전(commit)
- 재현 단계와 그로 인한 영향
- 제안하는 수정 방법(선택)

재현할 때는 가짜 token과 secret을 쓰고, 신고에 실제 값을 넣지 마세요.

## 범위

이 프로젝트의 취약점에 해당하는 예:

- 스크립트가 channel access token이나 channel secret을 출력하거나, 파일이나 캐시에 쓰거나, `api.line.me`, `api-data.line.me` 이외의 호스트로 보내는 경우.
- `webhook_tools.py`가 channel secret 자체를 보내는 경우(서명만 보내야 함).
- 쓰기 명령이 `--yes` 없이 실제로 실행되어 dry-run을 우회하는 경우.
- 경로 탐색(path traversal)이나 명령 주입. 예를 들어 `line_docs.py`의 페이지 경로와 캐시, 또는 `line_api.py`의 `--env-file`, `@file` 인자가 예상하지 못한 위치를 읽거나 쓰는 경우.
- `SKILL.md`나 `references/`의 지시 때문에 AI 어시스턴트가 사용자의 동의 없이 쓰기 작업을 실행하거나, token을 유출하거나, 조회한 문서 내용을 명령으로 받아들여 실행하는 경우.

이 프로젝트의 범위가 아닌 것:

- **LINE 플랫폼 자체**(LINE 앱, Messaging API, LIFF, LINE Login)의 취약점: LY Corporation의 [공식 창구](https://bugbounty.linecorp.com/)로 신고하세요.
- **AI 도구 자체**(Claude Code, Codex, Copilot 등)의 취약점: 해당 도구의 개발사에 신고하세요.
- **내 token이 유출된 경우**: 이 프로젝트의 취약점이 아닙니다. 즉시 [LINE Developers Console](https://developers.line.biz/console/)에서 token과 secret을 재발급하거나 폐기하세요.
- **함정 문서(gotchas)의 권장 사항이 오래되었거나 충분히 안전하지 않지만** 악용할 수 있는 취약점은 아닌 경우: 일반 issue를 열면 됩니다("Outdated LINE info or broken link" 템플릿).

## 처리 절차

개인이 관리하는 오픈 소스 프로젝트라 정해진 응답 기한은 없지만, 신고를 받으면 가능한 한 빨리 다음과 같이 처리합니다.

1. 접수를 확인합니다.
2. 문제와 영향 범위를 확인하고, 필요하면 세부 내용을 문의합니다.
3. 수정한 뒤 새 버전을 배포하고 CHANGELOG를 업데이트하며, GitHub Security Advisory로 공개합니다. 원하시면 공지에 감사 인사를 싣습니다.

수정이 배포되기 전에는 취약점의 세부 내용을 공개하지 마세요.

## 사용할 때 내 token 보호하기

- token과 secret은 환경 변수나 `.env`에 두고 `--env-file`로 지정하세요. 명령줄에 직접 입력하지 마세요(셸 기록과 프로세스 목록에 남습니다).
- `.env`가 `.gitignore`에 들어 있는지 확인하세요. 일부 도구가 만든 프로젝트는 기본적으로 이를 무시하지 않습니다(예: `supabase init`).
- 쓰기 작업은 dry-run 출력을 먼저 확인한 뒤에 `--yes`를 붙이세요.
- 설치 전에 `SKILL.md`와 `scripts/`를 살펴볼 수 있습니다. skill은 내 컴퓨터나 AI 도구의 실행 환경에서 이 스크립트들을 실행합니다.
