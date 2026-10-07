import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import React from 'react';
import { TicketBadge } from '../../src/components/TicketBadge';

describe('TicketBadge 컴포넌트 테스트', () => {
  it('열차 번호와 확정 상태를 정상 렌더링한다', () => {
    render(<TicketBadge trainNumber="G101" status="CONFIRMED" />);

    expect(screen.getByTestId('train-num').textContent).toBe('G101');
    expect(screen.getByTestId('badge-status').textContent).toBe('CONFIRMED');
  });

  it('매진 상태(SOLD_OUT)일 때는 "매진" 텍스트를 출력한다', () => {
    render(<TicketBadge trainNumber="K505" status="SOLD_OUT" />);

    expect(screen.getByTestId('badge-status').textContent).toBe('매진');
  });
});
