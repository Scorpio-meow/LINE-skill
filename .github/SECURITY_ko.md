# 보안 정책

[繁體中文](https://github.com/Scorpio-meow/LINE-skill/blob/HEAD/.github/SECURITY.md) | [English](https://github.com/Scorpio-meow/LINE-skill/blob/HEAD/.github/SECURITY_en.md) | [日本語](https://github.com/Scorpio-meow/LINE-skill/blob/HEAD/.github/SECURITY_ja.md) | [ไทย](https://github.com/Scorpio-meow/LINE-skill/blob/HEAD/.github/SECURITY_th.md) | [Bahasa Indonesia](https://github.com/Scorpio-meow/LINE-skill/blob/HEAD/.github/SECURITY_id.md) | **한국어**

## 지원 버전

최신 버전, 즉 `main` 브랜치만 수정합니다. 이전 버전을 쓰고 있다면 먼저 업데이트하세요(업데이트 방법은 [README](https://github.com/Scorpio-meow/LINE-skill/blob/HEAD/README_ko.md#업데이트와-제거) 참고).

## 취약점 신고

**공개 issue, Pull Request, 토론에 취약점 세부 내용을 공개하지 마세요.**

다음 중 한 가지 방법으로 비공개 신고해 주세요.

1. **GitHub 비공개 신고(권장)**: 저장소의 **Security** 탭에서 **Report a vulnerability**를 누르거나, [비공개 신고 양식](https://github.com/Scorpio-meow/LINE-skill/security/advisories/new)을 바로 여세요. 신고 내용은 신고자와 메인테이너만 볼 수 있습니다.
2. **이메일**: GitHub를 쓸 수 없다면 [yao921024@gmail.com](mailto:yao921024@gmail.com)으로 보내고 제목 앞에 `[Security] LINE-skill`을 붙여 주세요. 이메일은 종단 간 암호화되지 않으므로, 먼저 문제를 간단히 요약해 보내고 세부 내용은 답장을 받은 뒤에 보내 주세요.

다음 내용을 가능한 한 포함해 주세요.

- 영향을 받는 파일과 버전(commit)
- 재현 단계와 그로 인한 영향
- 제안하는 수정 방법(선택)

재현할 때는 가짜 token과 secret을 쓰고, 신고에 실제 값을 넣지 마세요.

## 처리 절차와 기한

개인이 관리하는 프로젝트라 버그 바운티는 없지만, 다음 기한을 지킵니다.

| 단계 | 기한 |
|---|---|
| 접수 확인과 첫 답변 | 신고를 받은 뒤 14일 이내 |
| 취약점 세부 내용 공개 | 수정 배포 시점, 늦어도 신고 후 90일 |

1. **접수 확인**: 신고를 받았음을 알리고 초기 평가를 공유합니다.
2. **평가**: 취약점인지, 영향 범위와 심각도를 확인하고, 필요하면 세부 내용을 문의합니다. 취약점이 아니라고 판단하면 이유를 설명합니다.
3. **수정**: 비공개 GitHub Security Advisory에서 수정 방법을 함께 논의합니다. 그 안의 비공개 포크에서 수정을 제출하실 수도 있습니다.
4. **공개**: 수정을 `main`에 병합하고 Security Advisory를 공개합니다. 해당하는 경우 GitHub를 통해 CVE 번호를 신청하고, [CHANGELOG](https://github.com/Scorpio-meow/LINE-skill/blob/HEAD/CHANGELOG.md)의 Security 항목에 기록합니다.
5. **감사 인사**: 원하시면 Advisory에 감사 인사를 싣습니다.

수정이 배포되기 전에는 취약점의 세부 내용을 공개하지 마세요. 90일 안에 수정하기 어려우면 기한 전에 이유를 설명하고 새 공개 날짜를 함께 정합니다.

## 범위

### 범위에 포함되는 것

이 프로젝트의 취약점에 해당하는 예:

- 스크립트가 channel access token이나 channel secret을 출력하거나, 파일이나 캐시에 쓰거나, `api.line.me`, `api-data.line.me` 이외의 호스트로 보내는 경우.
- `webhook_tools.py`가 channel secret 자체를 보내는 경우(서명만 보내야 함).
- 쓰기 명령이 `--yes` 없이 실제로 실행되어 dry-run을 우회하는 경우.
- 경로 탐색(path traversal)이나 명령 주입. 예를 들어 `line_docs.py`의 페이지 경로와 캐시, 또는 `line_api.py`의 `--env-file`, `@file` 인자가 예상하지 못한 위치를 읽거나 쓰는 경우.
- `SKILL.md`나 `references/`의 지시 때문에 AI 어시스턴트가 사용자의 동의 없이 쓰기 작업을 실행하거나, token을 유출하거나, 조회한 문서 내용을 명령으로 받아들여 실행하는 경우.

### 범위가 아닌 것

- **LINE 플랫폼 자체**(LINE 앱, Messaging API, LIFF, LINE Login)의 취약점: LY Corporation의 [공식 창구](https://bugbounty.linecorp.com/)로 신고하세요.
- **AI 도구 자체**(Claude Code, Codex, Copilot 등)의 취약점: 해당 도구의 개발사에 신고하세요.
- **내 token이 유출된 경우**: 이 프로젝트의 취약점이 아닙니다. 즉시 [LINE Developers Console](https://developers.line.biz/console/)에서 token과 secret을 재발급하거나 폐기하세요.
- **함정 문서(gotchas)의 권장 사항이 오래되었거나 충분히 안전하지 않지만** 악용할 수 있는 취약점은 아닌 경우: 일반 issue를 열면 됩니다("Outdated LINE info or broken link" 템플릿).

## 사용할 때 내 token 보호하기

- token과 secret은 환경 변수나 `.env`에 두고 `--env-file`로 지정하세요. 명령줄에 직접 입력하지 마세요(셸 기록과 프로세스 목록에 남습니다).
- `.env`가 `.gitignore`에 들어 있는지 확인하세요. 일부 도구가 만든 프로젝트는 기본적으로 이를 무시하지 않습니다(예: `supabase init`).
- 쓰기 작업은 dry-run 출력을 먼저 확인한 뒤에 `--yes`를 붙이세요.
- 설치 전에 `SKILL.md`와 `scripts/`를 살펴볼 수 있습니다. skill은 내 컴퓨터나 AI 도구의 실행 환경에서 이 스크립트들을 실행합니다.
