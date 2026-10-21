# 접근성 선언

[繁體中文](/.github/ACCESSIBILITY.md) | [English](/.github/ACCESSIBILITY.en.md) | [日本語](/.github/ACCESSIBILITY.ja.md) | [ไทย](/.github/ACCESSIBILITY.th.md) | [Bahasa Indonesia](/.github/ACCESSIBILITY.id.md) | **한국어**

## 우리의 약속

스크린 리더, 화면 확대, 키보드만 쓰는 방식이나 음성 입력을 사용하는 개발자, 그리고 다양한 언어를 쓰는 개발자 모두가 이 skill을 설치하고 읽고 사용할 수 있고, 기여에도 참여할 수 있기를 바랍니다.

## 프로젝트의 형태

이 프로젝트에는 웹페이지나 그래픽 인터페이스가 없으며, 구성은 다음과 같습니다.

- Markdown 문서: 6개 언어의 README, `SKILL.md`, `references/`
- 명령줄 Python 스크립트 3개
- 개발용 평가 소재

여러분은 자신의 AI 도구와 터미널을 통해 이 프로젝트를 사용하므로, 그 도구들 자체의 접근성도 사용 경험에 영향을 줍니다.

## 현재 지원하는 것

- 스크립트는 일반 텍스트만 출력하며, 색상, 커서 제어, 애니메이션으로 정보를 전달하지 않습니다. 모든 작업은 명령줄에서 키보드만으로 할 수 있습니다.
- 스크립트는 표준 출력을 UTF-8로 설정해, Windows 콘솔에서 중국어, 일본어, 태국어, 한국어를 표시할 때 글자가 깨지는 일을 줄입니다.
- 문서는 Markdown 제목으로 나뉘어 있어, 스크린 리더의 제목 탐색으로 필요한 부분에 바로 이동할 수 있습니다.
- README는 繁體中文, English, 日本語, ไทย, Bahasa Indonesia, 한국어의 6개 언어로 제공됩니다.
- LINE 봇 개발을 도울 때 skill은 Flex Message 같은 메시지에 `altText`를 쓰도록 안내합니다. 이 텍스트는 알림, 채팅 목록, 인용 미리보기에 표시됩니다.

## 알려진 제한 사항

- README의 "도구별 skill 폴더"는 5열 12행 표라서 스크린 리더나 좁은 화면에서는 읽기 어렵습니다.
- README의 "구성" 절은 선 그리기 문자(`├──`, `└──`)로 디렉터리 트리를 그리므로, 스크린 리더가 이 기호를 하나하나 읽을 수 있습니다.
- `SKILL.md`와 `references/`는 영어로만 되어 있습니다(주로 AI가 읽는 문서). 스크립트의 메시지와 `-h` 도움말도 영어뿐입니다.
- 번체 중국어 이외의 README는 번역본이라 업데이트가 늦을 수 있습니다. 내용이 다르면 [번체 중국어판](/README.md)을 기준으로 합니다.
- Claude, ChatGPT, Codex 같은 도구의 설치 화면은 각 업체가 제공하므로, 그 접근성은 이 프로젝트가 통제할 수 없습니다.
- 아직 특정 스크린 리더로 체계적인 테스트를 하지 않았습니다.

## 지원 환경

- macOS, Linux, Windows(PowerShell, Windows Terminal), Python 3.8 이상.
- UTF-8 텍스트를 표시할 수 있는 모든 터미널.
- 문서는 GitHub 웹페이지나 아무 Markdown 뷰어에서 읽을 수 있고, 일반 텍스트 편집기로 바로 열 수도 있습니다.

## 접근성 문제 신고

["Accessibility barrier"(접근성 장벽) issue를 열고](https://github.com/Scorpio-meow/LINE-skill/issues/new?template=accessibility.yml) 어디서 문제를 겪었는지, 사용하는 보조 기술과 환경, 어떤 어려움이 있었는지 알려 주세요. 공개하기 어렵다면 yao921024@gmail.com으로 이메일을 보내도 됩니다. 개인이 관리하는 프로젝트라 정해진 응답 기한은 없지만, 모든 신고를 꼼꼼히 읽겠습니다.

LINE 봇 개발을 도울 때 skill이 그 밖에 어떤 접근성 사항을 안내하면 좋을지 제안도 환영합니다.

마지막 업데이트: 2026-10-21
