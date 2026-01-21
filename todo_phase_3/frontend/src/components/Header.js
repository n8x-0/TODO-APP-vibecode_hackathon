'use client';
import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { getCookie, deleteCookie } from '../utils/cookies';
import ChatInterface from './ChatInterface';

const Header = ({ user, chatHistory }) => {
  const [showProfileMenu, setShowProfileMenu] = useState(false);
  const router = useRouter();

  const handleSignOut = () => {
    // Remove the authentication token
    deleteCookie('access_token');
    // Redirect to login page
    router.push('/login');
  };

  // Get initials from user's name or email
  const getInitials = () => {
    if (!user) return 'U';
    if (user.email) {
      const emailParts = user.email.split('@')[0].split('.');
      return emailParts.map(part => part.charAt(0).toUpperCase()).join('').substring(0, 2);
    }
    return 'U';
  };

  return (
    <header className="bg-white shadow-sm border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo/Brand Section */}
          <div className="flex items-center">
            <h1 className="text-xl font-bold text-gray-900">
              n8x <span className="font-light">Todo App</span>
            </h1>
          </div>

          {/* User Profile Section */}
          <div className="flex items-center space-x-4">
            {/* Profile Dropdown */}
            <div className="relative">
              <button
                onClick={() => setShowProfileMenu(!showProfileMenu)}
                className="flex items-center text-sm rounded-full focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                id="user-menu"
                aria-haspopup="true"
                aria-expanded="false"
              >
                <div className="w-8 h-8 rounded-full bg-gradient-to-r from-blue-500 to-indigo-600 flex items-center justify-center text-white font-medium">
                  {getInitials()}
                </div>
              </button>

              {/* Profile Dropdown Menu */}
              {showProfileMenu && (
                <div
                  className="origin-top-right absolute right-0 mt-2 w-48 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5 z-50"
                  role="menu"
                  aria-orientation="vertical"
                  aria-labelledby="user-menu"
                >
                  <div className="py-1" role="none">
                    <div className="px-4 py-2 border-b border-gray-200">
                      <p className="text-sm font-medium text-gray-900 truncate">
                        {user?.email || 'User'}
                      </p>
                      <p className="text-xs text-gray-500 truncate">
                        {user?.email ? `Logged in as ${user.email}` : 'Not logged in'}
                      </p>
                    </div>
                    <button
                      onClick={handleSignOut}
                      className="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 hover:text-gray-900"
                      role="menuitem"
                    >
                      Sign out
                    </button>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Click outside to close menu */}
      {showProfileMenu && (
        <div
          className="fixed inset-0 z-40"
          aria-hidden="true"
          onClick={() => setShowProfileMenu(false)}
        />
      )}

      {/* Chat Interface */}
      <ChatInterface user={user} chatHistory={chatHistory} />
    </header>
  );
};

export default Header;