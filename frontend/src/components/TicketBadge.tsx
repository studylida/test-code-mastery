import React from 'react';

interface TicketBadgeProps {
  status: 'CONFIRMED' | 'SOLD_OUT' | 'CANCELLED';
  trainNumber: string;
}

export const TicketBadge: React.FC<TicketBadgeProps> = ({ status, trainNumber }) => {
  const isSoldOut = status === 'SOLD_OUT';

  return (
    <div className={`ticket-badge ${status.toLowerCase()}`}>
      <span data-testid="train-num">{trainNumber}</span>
      <span data-testid="badge-status">{isSoldOut ? '매진' : status}</span>
    </div>
  );
};
