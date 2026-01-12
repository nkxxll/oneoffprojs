import React from 'react';
import { Button } from '@/components/ui/button';
import { useAuth } from './AuthContext';

export const Login: React.FC = () => {
  const { isAuthenticated, login, logout } = useAuth();

  if (isAuthenticated) {
    return (
      <div className="flex items-center gap-4">
        <span>Welcome! You are logged in.</span>
        <Button onClick={logout} variant="outline">
          Logout
        </Button>
      </div>
    );
  }

  return (
    <Button onClick={login}>
      Login with GitHub
    </Button>
  );
};
