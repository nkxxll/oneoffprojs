import { useEffect } from 'react';

export function Toast({ message, duration = 3000, onClose }: { message: string; duration?: number; onClose: () => void }) {
  useEffect(() => {
    const timer = setTimeout(onClose, duration);
    return () => clearTimeout(timer);
  }, [duration, onClose]);

  return (
    <box
      border
      borderStyle="rounded"
      style={{
        position: 'absolute',
        bottom: 2,
        left: '50%',
        transform: 'translateX(-50%)',
        backgroundColor: 'black',
        color: 'white',
        zIndex: 10,
      }}
    >
      <text>{message}</text>
    </box>
  );
}
