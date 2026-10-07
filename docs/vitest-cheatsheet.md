# ⚡ Vitest & React Testing Library Cheatsheet

> 프론트엔드 테스트 코드 손코딩 시 유용한 핵심 문법 모음

---

## 1. 기본 테스트 선언 공식

```typescript
import { describe, it, expect } from 'vitest';

describe('컴포넌트 또는 유틸 이름', () => {
  it('기대하는 동작 설명', () => {
    // 1단계: 실행
    const result = add(1, 2);

    // 2단계: 검증
    expect(result).toBe(3);
  });
});
```

---

## 2. React 컴포넌트 렌더링 & 이벤트 검증 공식

```tsx
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { Counter } from './Counter';

it('버튼 클릭 시 숫자가 1 증가한다', async () => {
  const user = userEvent.setup();

  // 1단계: 컴포넌트 렌더링
  render(<Counter />);

  // 2단계: 화면 요소 찾기 (Role, Text 등)
  const button = screen.getByRole('button', { name: /증가/i });
  const countText = screen.getByText('현재 카운트: 0');

  // 3단계: 사용자 상호작용 (클릭)
  await user.click(button);

  // 4단계: 바뀐 화면 검증
  expect(screen.getByText('현재 카운트: 1')).toBeInTheDocument();
});
```

---

## 3. 자주 쓰는 Matcher 정리

- `expect(a).toBe(b)`: 원시값(primitive) 동일성 검사 (`===`)
- `expect(a).toEqual(b)`: 객체/배열 깊은 비교 (Deep equality)
- `expect(a).toBeNull()`: null 검사
- `expect(a).toBeDefined()`: undefined가 아님 검사
- `expect(element).toBeInTheDocument()`: DOM에 렌더링되어 있는지 검사
